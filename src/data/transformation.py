"""Recompute derived KPI flags from cleaned PO lines."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import load_config


def transform_purchase_orders(df: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    config = config or load_config()
    out = df.copy()
    order_dt = pd.to_datetime(out["order_date"])
    promised_dt = pd.to_datetime(out["promised_delivery_date"])
    actual_dt = pd.to_datetime(out["actual_delivery_date"])
    approval_dt = pd.to_datetime(out["po_approval_date"])
    creation_dt = pd.to_datetime(out["po_creation_date"])

    out["actual_lead_time_days"] = (actual_dt - order_dt).dt.days
    out["lead_time_days"] = (promised_dt - order_dt).dt.days
    out["lead_time_variance_days"] = out["actual_lead_time_days"] - out["lead_time_days"]
    out["delivery_days_late"] = (actual_dt - promised_dt).dt.days.clip(lower=0)
    out["delivery_days_early"] = (promised_dt - actual_dt).dt.days.clip(lower=0)
    out["quantity_shortfall"] = (out["ordered_quantity"] - out["received_quantity"]).clip(lower=0)
    out["defect_rate"] = out["defective_quantity"] / out["received_quantity"].replace(0, pd.NA)
    out["defect_rate"] = out["defect_rate"].fillna(0)
    out["cost_variance"] = out["unit_price"] - out["standard_price"]
    out["cost_variance_pct"] = out["cost_variance"] / out["standard_price"].replace(0, pd.NA)
    out["cost_variance_pct"] = out["cost_variance_pct"].fillna(0)
    out["fill_rate"] = out["received_quantity"] / out["ordered_quantity"].replace(0, pd.NA)
    out["fill_rate"] = out["fill_rate"].fillna(0)

    tol_days = int(config["otif"]["delivery_tolerance_days"])
    tol_qty = float(config["otif"]["quantity_tolerance_pct"])
    on_time = actual_dt <= (promised_dt + pd.to_timedelta(tol_days, unit="D"))
    in_full = out["received_quantity"] >= out["ordered_quantity"] * (1 - tol_qty)
    out["otif_flag"] = (on_time & in_full).astype(int)
    out["late_only_flag"] = ((~on_time) & in_full).astype(int)
    out["qty_short_only_flag"] = (on_time & (~in_full)).astype(int)
    out["late_and_short_flag"] = ((~on_time) & (~in_full)).astype(int)
    out["sla_breach_flag"] = (out["actual_lead_time_days"] > out["sla_days"]).astype(int)
    out["po_turnaround_days"] = (approval_dt - creation_dt).dt.days.clip(lower=0)
    out["actual_spend"] = (out["received_quantity"] * out["unit_price"]).round(2)
    out["expected_spend"] = (out["received_quantity"] * out["standard_price"]).round(2)
    out["ordered_spend"] = (out["ordered_quantity"] * out["unit_price"]).round(2)
    out["year_month"] = order_dt.dt.strftime("%Y-%m")
    return out
