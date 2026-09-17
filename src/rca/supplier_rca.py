"""Select the worst-performing supplier from the scorecard and seed RCA."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.rca.five_why import build_five_why


FISHBONE = {
    "Man": [
        "Promise dates entered without a capacity check",
        "Quality hold release waiting on a single inspector",
        "Customer-service backlog on ASN / POD confirmation",
    ],
    "Machine": [
        "Bottleneck work center running above demonstrated capacity",
        "Test equipment downtime extending quality release",
        "Pack line changeovers during peak mix weeks",
    ],
    "Method": [
        "No ATP gate before PO acknowledgement",
        "SLA measured on ship date rather than dock date",
        "Partial receipts closed without a remainder PO",
    ],
    "Material": [
        "Incoming sub-component shortages at the supplier",
        "Lot-to-lot variation on a high-defect material family",
        "Substitution without a documented deviation",
    ],
    "Measurement": [
        "Promise date and requested date used interchangeably in reports",
        "OTIF calculated at shipment header instead of PO line",
        "Defects recorded after receipt, so in-transit damage is mixed in",
    ],
    "Environment": [
        "Peak-season carrier capacity in the supplier region",
        "Weather / port congestion overlay on long-lead lanes",
        "Plant receiving-dock calendar not shared with the supplier",
    ],
}


def select_worst_supplier(scorecard: pd.DataFrame) -> dict[str, Any]:
    ranked = scorecard.sort_values(
        ["weighted_score", "risk_score"], ascending=[True, False]
    )
    row = ranked.iloc[0]
    return row.to_dict()


def build_rca_package(scorecard: pd.DataFrame, fact: pd.DataFrame) -> dict[str, Any]:
    supplier = select_worst_supplier(scorecard)
    sid = supplier["supplier_id"]
    lines = fact[fact["supplier_id"] == sid]
    monthly = (
        lines.groupby("year_month")
        .agg(
            otif_pct=("otif_flag", "mean"),
            defect_rate=("defect_rate", "mean"),
            sla_breach_rate=("sla_breach_flag", "mean"),
            avg_lead_time_variance=("lead_time_variance_days", "mean"),
            spend=("actual_spend", "sum"),
        )
        .reset_index()
        .to_dict(orient="records")
    )
    problem_mix = {
        "late_only": int(lines["late_only_flag"].sum()),
        "qty_short_only": int(lines["qty_short_only_flag"].sum()),
        "late_and_short": int(lines["late_and_short_flag"].sum()),
        "quality_rejected": int((lines["quality_status"] == "REJECTED").sum()),
        "sla_breaches": int(lines["sla_breach_flag"].sum()),
    }
    return {
        "supplier": {k: (v.item() if hasattr(v, "item") else v) for k, v in supplier.items() if k != "seasonal_delay_months"},
        "five_why": build_five_why(supplier),
        "fishbone": FISHBONE,
        "problem_mix": problem_mix,
        "monthly": monthly,
        "corrective_actions": [
            {
                "action": "Re-promise remaining open POs using demonstrated P90 lead time",
                "owner": "Buyer + supplier planner",
                "due": "10 business days",
            },
            {
                "action": "Stand up a weekly OTIF huddle with late-line aged list",
                "owner": "Supplier performance analyst",
                "due": "Next Monday",
            },
            {
                "action": "Qualify an alternate source for the top defective material family",
                "owner": "Category manager",
                "due": "45 days",
            },
            {
                "action": "Freeze a 4-week forecast fence and share it via the procurement schedule",
                "owner": "Supply planner",
                "due": "15 days",
            },
        ],
    }
