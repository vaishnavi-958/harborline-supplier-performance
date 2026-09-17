"""End-to-end Harborline procurement analytics pipeline."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from src.analytics.otif import otif_by, otif_rate
from src.analytics.supplier_scorecard import (
    build_pareto,
    build_supplier_scorecard,
    group_kpis,
    monthly_kpis,
)
from src.data.cleaning import clean_purchase_orders
from src.data.generate_synthetic_data import generate_all, save_generation
from src.data.transformation import transform_purchase_orders
from src.data.validation import write_quality_report
from src.database.loaders import apply_analytics_sql, load_star_schema
from src.rca.supplier_rca import build_rca_package
from src.utils.helpers import load_config, load_scoring_config, project_path, safe_div
from src.utils.logging_config import configure_logging

LOGGER = configure_logging()


def _json_ready(value):
    if isinstance(value, dict):
        return {str(k): _json_ready(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_ready(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if value is pd.NA or value is None:
        return None
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def records(df: pd.DataFrame) -> list[dict]:
    return _json_ready(df.to_dict(orient="records"))


def export_excel(tables: dict[str, pd.DataFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in tables.items():
            df.head(5000).to_excel(writer, sheet_name=name[:31], index=False)


def run_pipeline() -> dict:
    config = load_config()
    scoring = load_scoring_config()
    LOGGER.info("Generating synthetic procurement dataset")
    generated = generate_all(config)
    save_generation(generated, config)

    LOGGER.info("Running data-quality checks on raw lines")
    quality_report = write_quality_report(generated.fact_raw)

    cleaned = clean_purchase_orders(generated.fact_raw, generated.fact_purchase_orders)
    fact = transform_purchase_orders(cleaned, config)
    proc = project_path(config["paths"]["processed_dir"])
    exp = project_path(config["paths"]["exports_dir"])
    proc.mkdir(parents=True, exist_ok=True)
    exp.mkdir(parents=True, exist_ok=True)
    fact.to_csv(proc / "fact_purchase_orders.csv", index=False)

    scorecard = build_supplier_scorecard(fact, generated.dim_supplier, scoring)
    pareto = build_pareto(scorecard)
    monthly = monthly_kpis(fact)
    monthly_supplier = (
        fact.groupby(["supplier_id", "supplier_name", "year_month"], dropna=False)
        .agg(
            otif_pct=("otif_flag", "mean"),
            fill_rate=("fill_rate", "mean"),
            defect_rate=("defect_rate", "mean"),
            sla_breach_rate=("sla_breach_flag", "mean"),
            actual_spend=("actual_spend", "sum"),
            avg_lead_time=("actual_lead_time_days", "mean"),
            avg_lead_time_variance=("lead_time_variance_days", "mean"),
            po_lines=("po_line_id", "size"),
        )
        .reset_index()
    )
    rca = build_rca_package(scorecard, fact)

    scorecard.to_csv(exp / "supplier_scorecard.csv", index=False)
    pareto.to_csv(exp / "supplier_pareto.csv", index=False)
    monthly.to_csv(exp / "monthly_kpis.csv", index=False)
    monthly_supplier.to_csv(exp / "supplier_monthly_kpi.csv", index=False)
    quality_report.to_csv(exp / "data_quality_report.csv", index=False)

    tables = {
        "dim_supplier": generated.dim_supplier,
        "dim_material": generated.dim_material,
        "dim_category": generated.dim_category,
        "dim_region": generated.dim_region,
        "dim_plant": generated.dim_plant,
        "dim_date": generated.dim_date,
        "dim_carrier": generated.dim_carrier,
        "fact_purchase_orders": fact,
        "supplier_scorecard": scorecard,
        "supplier_monthly_kpi": monthly_supplier,
        "supplier_pareto": pareto,
        "supplier_risk": scorecard[
            [
                "supplier_id",
                "supplier_name",
                "risk_score",
                "risk_band",
                "otif_pct",
                "defect_rate",
                "sla_breach_rate",
                "avg_lead_time_variance",
                "cost_variance_pct",
                "total_spend",
                "spend_share",
            ]
        ],
    }
    LOGGER.info("Loading SQLite star schema")
    load_star_schema(tables)
    apply_analytics_sql()

    export_excel(
        {
            "scorecard": scorecard,
            "pareto": pareto,
            "monthly": monthly,
            "quality_report": quality_report,
            "suppliers": generated.dim_supplier,
        },
        exp / "harborline_procurement_pack.xlsx",
    )

    problem_mix = {
        "late_only": int(fact["late_only_flag"].sum()),
        "qty_short_only": int(fact["qty_short_only_flag"].sum()),
        "late_and_short": int(fact["late_and_short_flag"].sum()),
        "quality_rejected": int((fact["quality_status"] == "REJECTED").sum()),
        "sla_breaches": int(fact["sla_breach_flag"].sum()),
        "unfavorable_cost": int((fact["cost_variance"] > 0).sum()),
    }

    material_quality = (
        fact.groupby(["material_id", "material_description", "category"], dropna=False)
        .agg(
            defect_qty=("defective_quantity", "sum"),
            received_qty=("received_quantity", "sum"),
            actual_spend=("actual_spend", "sum"),
            otif_pct=("otif_flag", "mean"),
        )
        .reset_index()
    )
    material_quality["defect_rate"] = [
        safe_div(d, r) for d, r in zip(material_quality["defect_qty"], material_quality["received_qty"])
    ]
    material_quality = material_quality.sort_values("defect_qty", ascending=False)

    delay_hist = (
        fact.assign(bucket=lambda d: np.clip(d["delivery_days_late"], 0, 15))
        .groupby("bucket")
        .size()
        .reset_index(name="lines")
    )

    dashboard = {
        "disclaimer": config["project"]["disclaimer"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": config["project"],
        "otif_definition": {
            "rule": "OTIF = 1 when actual_delivery_date <= promised_delivery_date + delivery_tolerance_days AND received_quantity >= ordered_quantity * (1 - quantity_tolerance_pct)",
            "delivery_tolerance_days": config["otif"]["delivery_tolerance_days"],
            "quantity_tolerance_pct": config["otif"]["quantity_tolerance_pct"],
        },
        "scoring": scoring,
        "kpis": {
            "total_suppliers": int(fact["supplier_id"].nunique()),
            "total_pos": int(fact["po_id"].nunique()),
            "total_lines": int(len(fact)),
            "total_spend": float(fact["actual_spend"].sum()),
            "otif_pct": otif_rate(fact["otif_flag"]),
            "fill_rate": float(safe_div(fact["received_quantity"].sum(), fact["ordered_quantity"].sum())),
            "defect_rate": float(safe_div(fact["defective_quantity"].sum(), fact["received_quantity"].sum())),
            "sla_compliance": float(1 - fact["sla_breach_flag"].mean()),
            "cost_variance": float(fact["actual_spend"].sum() - fact["expected_spend"].sum()),
            "cost_variance_pct": float(
                safe_div(
                    fact["actual_spend"].sum() - fact["expected_spend"].sum(),
                    fact["expected_spend"].sum(),
                )
            ),
            "high_risk_suppliers": int(scorecard["risk_band"].isin(["HIGH", "CRITICAL"]).sum()),
            "avg_lead_time": float(fact["actual_lead_time_days"].mean()),
            "avg_lead_time_variance": float(fact["lead_time_variance_days"].mean()),
            "avg_turnaround": float(fact["po_turnaround_days"].mean()),
        },
        "problem_mix": problem_mix,
        "monthly": records(monthly),
        "suppliers": records(scorecard),
        "pareto": records(pareto),
        "by_category": records(group_kpis(fact, "category")),
        "by_region": records(group_kpis(fact, "region")),
        "by_plant": records(group_kpis(fact, "plant_name")),
        "materials": records(material_quality.head(40)),
        "delay_histogram": records(delay_hist),
        "supplier_monthly": records(monthly_supplier),
        "otif_by_supplier": records(otif_by(fact, "supplier_id")),
        "rca": _json_ready(rca),
        "quality_report": records(quality_report),
        "dimensions": {
            "plants": records(generated.dim_plant),
            "regions": records(generated.dim_region),
            "categories": records(generated.dim_category),
            "carriers": records(generated.dim_carrier),
        },
    }

    json_path = project_path(config["paths"]["dashboard_json"])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(dashboard, indent=2), encoding="utf-8")
    (exp / "dashboard.json").write_text(json.dumps(dashboard, indent=2), encoding="utf-8")
    LOGGER.info("Dashboard JSON written to %s", json_path)
    return dashboard


if __name__ == "__main__":
    run_pipeline()
