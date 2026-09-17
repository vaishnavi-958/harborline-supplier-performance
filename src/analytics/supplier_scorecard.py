"""Weighted supplier scorecard and analytical risk model.

Scores are derived from calculated KPIs. This is not a real procurement policy.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.analytics.cost_variance import cost_variance_by
from src.analytics.fill_rate import fill_rate_by
from src.analytics.lead_time import lead_time_by, sla_status
from src.analytics.otif import otif_by
from src.analytics.quality import quality_by
from src.utils.helpers import clip, load_scoring_config, safe_div


def _minmax(series: pd.Series, lower_is_better: bool, cap: float | None = None) -> pd.Series:
    values = series.astype(float).copy()
    if cap is not None:
        values = values.clip(upper=cap)
    vmin, vmax = values.min(), values.max()
    if pd.isna(vmin) or pd.isna(vmax) or vmax == vmin:
        scaled = pd.Series(np.ones(len(values)) * 80.0, index=values.index)
    else:
        scaled = (values - vmin) / (vmax - vmin)
        scaled = 1 - scaled if lower_is_better else scaled
        scaled = 40 + scaled * 60  # keep a readable 40–100 band
    return scaled


def recommended_action(row: pd.Series, scoring: dict[str, Any]) -> str:
    actions = scoring["recommended_action"]
    if row["otif_pct"] < scoring["otif_alert_threshold"]:
        if row["performance_tier"] == "D":
            return actions["D"]
        return actions["otif_below_threshold"]
    if row["cost_variance_pct"] > 0.05 and row["performance_tier"] in {"B", "C", "D"}:
        return actions["high_cost_variance"]
    return actions.get(row["performance_tier"], actions["B"])


def build_supplier_scorecard(
    fact: pd.DataFrame,
    dim_supplier: pd.DataFrame,
    scoring: dict[str, Any] | None = None,
) -> pd.DataFrame:
    scoring = scoring or load_scoring_config()
    weights = scoring["weights"]
    caps = scoring["normalization"]
    sla_cfg = scoring.get("risk", {})

    otif = otif_by(fact, "supplier_id").drop(columns=["po_lines"], errors="ignore")
    fill = fill_rate_by(fact, "supplier_id").drop(columns=["po_lines"], errors="ignore")
    quality = quality_by(fact, "supplier_id").drop(
        columns=["po_lines", "received_quantity"], errors="ignore"
    )
    cost = cost_variance_by(fact, "supplier_id").drop(columns=["po_lines"], errors="ignore")
    lead = lead_time_by(fact, "supplier_id").drop(columns=["po_lines"], errors="ignore")

    spend = fact.groupby("supplier_id", dropna=False).agg(
        total_spend=("actual_spend", "sum"),
        total_pos=("po_id", "nunique"),
        po_lines=("po_line_id", "size"),
        avg_turnaround=("po_turnaround_days", "mean"),
    ).reset_index()

    card = (
        otif.merge(fill, on="supplier_id")
        .merge(quality, on="supplier_id")
        .merge(cost, on="supplier_id")
        .merge(lead, on="supplier_id")
        .merge(spend, on="supplier_id")
        .merge(
            dim_supplier[
                [
                    "supplier_id",
                    "supplier_name",
                    "supplier_region",
                    "supplier_category",
                    "supplier_tier",
                    "archetype",
                    "sla_days",
                    "payment_terms",
                ]
            ],
            on="supplier_id",
        )
    )

    card["quality_score"] = _minmax(card["defect_rate"], True, caps["defect_rate_cap"])
    card["delivery_score"] = 40 + card["otif_pct"].clip(0, 1) * 60
    card["cost_score"] = _minmax(card["cost_variance_pct"], True, caps["cost_variance_pct_cap"])
    card["weighted_score"] = (
        card["quality_score"] * weights["quality"]
        + card["delivery_score"] * weights["delivery"]
        + card["cost_score"] * weights["cost"]
    )
    card["supplier_rank"] = card["weighted_score"].rank(ascending=False, method="min").astype(int)

    tiers = scoring["performance_tiers"]
    def tier_for(score: float) -> str:
        if score >= tiers["A"]["min_score"]:
            return "A"
        if score >= tiers["B"]["min_score"]:
            return "B"
        if score >= tiers["C"]["min_score"]:
            return "C"
        return "D"

    card["performance_tier"] = card["weighted_score"].map(tier_for)
    card["performance_tier_label"] = card["performance_tier"].map(
        lambda t: tiers[t]["label"]
    )

    watch = 0.08
    breach = 0.15
    try:
        from src.utils.helpers import load_config

        sla_thresholds = load_config().get("sla", {})
        watch = float(sla_thresholds.get("watch_breach_rate", watch))
        breach = float(sla_thresholds.get("breach_rate", breach))
    except Exception:
        pass
    card["sla_status"] = card["sla_breach_rate"].map(lambda r: sla_status(float(r), watch, breach))

    total_spend = card["total_spend"].sum()
    card["spend_share"] = card["total_spend"] / total_spend if total_spend else 0

    risk_w = scoring["risk"]["weights"]
    otif_gap = (1 - card["otif_pct"]).clip(0, 1)
    defect_n = (card["defect_rate"] / caps["defect_rate_cap"]).clip(0, 1)
    sla_n = (card["sla_breach_rate"] / caps["sla_breach_rate_cap"]).clip(0, 1)
    ltv_n = (card["avg_lead_time_variance"].clip(lower=0) / caps["lead_time_variance_days_cap"]).clip(0, 1)
    cost_n = (card["cost_variance_pct"].clip(lower=0) / caps["cost_variance_pct_cap"]).clip(0, 1)
    spend_n = (card["spend_share"] / card["spend_share"].max()) if card["spend_share"].max() else 0

    card["risk_score"] = 100 * (
        otif_gap * risk_w["otif_gap"]
        + defect_n * risk_w["defect_rate"]
        + sla_n * risk_w["sla_breach_rate"]
        + ltv_n * risk_w["lead_time_variance"]
        + cost_n * risk_w["unfavorable_cost_variance"]
        + spend_n * risk_w["spend_exposure"]
    )
    bands = scoring["risk"]["bands"]

    def risk_band(score: float) -> str:
        if score <= bands["LOW"]["max_score"]:
            return "LOW"
        if score <= bands["MEDIUM"]["max_score"]:
            return "MEDIUM"
        if score <= bands["HIGH"]["max_score"]:
            return "HIGH"
        return "CRITICAL"

    card["risk_band"] = card["risk_score"].map(risk_band)
    card["recommended_action"] = card.apply(lambda row: recommended_action(row, scoring), axis=1)

    problem_count = (
        fact.assign(problem=lambda d: ((d["otif_flag"] == 0) | (d["quality_status"] == "REJECTED") | (d["sla_breach_flag"] == 1) | (d["cost_variance"] > 0)).astype(int))
        .groupby("supplier_id")["problem"]
        .sum()
        .rename("problem_count")
        .reset_index()
    )
    card = card.merge(problem_count, on="supplier_id", how="left")
    card["problem_count"] = card["problem_count"].fillna(0).astype(int)
    card = card.sort_values("supplier_rank").reset_index(drop=True)
    return card


def build_pareto(card: pd.DataFrame) -> pd.DataFrame:
    pareto = card.sort_values("problem_count", ascending=False).copy()
    total = pareto["problem_count"].sum()
    pareto["problem_pct"] = pareto["problem_count"] / total if total else 0
    pareto["cumulative_pct"] = pareto["problem_pct"].cumsum()
    return pareto[
        [
            "supplier_id",
            "supplier_name",
            "problem_count",
            "problem_pct",
            "cumulative_pct",
            "risk_band",
            "weighted_score",
        ]
    ].reset_index(drop=True)


def monthly_kpis(fact: pd.DataFrame) -> pd.DataFrame:
    g = fact.groupby("year_month")
    out = g.agg(
        po_lines=("po_line_id", "size"),
        otif_pct=("otif_flag", "mean"),
        fill_rate=("fill_rate", "mean"),
        defect_qty=("defective_quantity", "sum"),
        received_qty=("received_quantity", "sum"),
        sla_compliance=("sla_breach_flag", lambda s: 1 - s.mean()),
        actual_spend=("actual_spend", "sum"),
        expected_spend=("expected_spend", "sum"),
        avg_lead_time=("actual_lead_time_days", "mean"),
        avg_lead_time_variance=("lead_time_variance_days", "mean"),
        late_pct=("late_only_flag", "mean"),
    ).reset_index()
    out["defect_rate"] = [
        safe_div(d, r) for d, r in zip(out["defect_qty"], out["received_qty"])
    ]
    out["cost_variance"] = out["actual_spend"] - out["expected_spend"]
    out["cost_variance_pct"] = [
        safe_div(c, e) for c, e in zip(out["cost_variance"], out["expected_spend"])
    ]
    return out


def group_kpis(fact: pd.DataFrame, group_col: str) -> pd.DataFrame:
    g = fact.groupby(group_col)
    out = g.agg(
        po_lines=("po_line_id", "size"),
        otif_pct=("otif_flag", "mean"),
        fill_rate=("fill_rate", "mean"),
        defect_qty=("defective_quantity", "sum"),
        received_qty=("received_quantity", "sum"),
        sla_compliance=("sla_breach_flag", lambda s: 1 - s.mean()),
        actual_spend=("actual_spend", "sum"),
        expected_spend=("expected_spend", "sum"),
        avg_lead_time=("actual_lead_time_days", "mean"),
        suppliers=("supplier_id", "nunique"),
    ).reset_index()
    out["defect_rate"] = [
        safe_div(d, r) for d, r in zip(out["defect_qty"], out["received_qty"])
    ]
    out["cost_variance"] = out["actual_spend"] - out["expected_spend"]
    return out


def clip_score(value: float) -> float:
    return clip(value, 0, 100)
