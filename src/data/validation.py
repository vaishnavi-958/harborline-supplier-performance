"""Data-quality checks for synthetic purchase-order lines."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import project_path, load_config


CHECKS = [
    ("duplicate_po_lines", "Duplicate PO line identifiers"),
    ("missing_supplier", "Missing supplier identifier"),
    ("missing_dates", "Missing order, promised, or actual dates"),
    ("invalid_dates", "Actual delivery before order date"),
    ("negative_quantities", "Negative ordered, received, or defective quantity"),
    ("zero_quantities", "Zero ordered quantity"),
    ("invalid_prices", "Missing unit or standard price"),
    ("negative_prices", "Negative unit or standard price"),
    ("defect_gt_received", "Defective quantity greater than received quantity"),
    ("received_gt_ordered", "Received quantity greater than ordered quantity"),
    ("invalid_lead_time", "Negative or missing lead time"),
    ("invalid_sla", "Missing or non-positive SLA days"),
    ("missing_category", "Missing category"),
    ("missing_region", "Missing region"),
]


def _to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def run_checks(df: pd.DataFrame) -> pd.DataFrame:
    order_dt = _to_datetime(df.get("order_date"))
    promised_dt = _to_datetime(df.get("promised_delivery_date"))
    actual_dt = _to_datetime(df.get("actual_delivery_date"))

    masks: dict[str, pd.Series] = {
        "duplicate_po_lines": df["po_line_id"].duplicated(keep=False) if "po_line_id" in df else pd.Series(False, index=df.index),
        "missing_supplier": df["supplier_id"].isna() | (df["supplier_id"].astype(str).str.strip() == ""),
        "missing_dates": order_dt.isna() | promised_dt.isna() | actual_dt.isna(),
        "invalid_dates": actual_dt.notna() & order_dt.notna() & (actual_dt < order_dt),
        "negative_quantities": (df["ordered_quantity"] < 0)
        | (df["received_quantity"] < 0)
        | (df["defective_quantity"] < 0),
        "zero_quantities": df["ordered_quantity"] == 0,
        "invalid_prices": df["unit_price"].isna() | df["standard_price"].isna(),
        "negative_prices": (df["unit_price"] < 0) | (df["standard_price"] < 0),
        "defect_gt_received": df["defective_quantity"] > df["received_quantity"],
        "received_gt_ordered": df["received_quantity"] > df["ordered_quantity"],
        "invalid_lead_time": df["actual_lead_time_days"].isna() | (df["actual_lead_time_days"] < 0),
        "invalid_sla": df["sla_days"].isna() | (df["sla_days"] <= 0),
        "missing_category": df["category"].isna() | (df["category"].astype(str).str.strip() == ""),
        "missing_region": df["region"].isna() | (df["region"].astype(str).str.strip() == ""),
    }

    rows = []
    total = len(df)
    for check_id, description in CHECKS:
        mask = masks[check_id].fillna(False)
        failed = int(mask.sum())
        rows.append(
            {
                "check_id": check_id,
                "description": description,
                "failed_rows": failed,
                "total_rows": total,
                "fail_rate": round(failed / total, 6) if total else 0,
                "status": "FAIL" if failed else "PASS",
            }
        )
    return pd.DataFrame(rows)


def write_quality_report(df: pd.DataFrame, output_path: str | None = None) -> pd.DataFrame:
    report = run_checks(df)
    config = load_config()
    path = project_path(output_path or config["paths"]["quality_report"])
    path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(path, index=False)
    return report
