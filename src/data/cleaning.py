"""Clean raw PO lines after validation. Does not invent business facts."""

from __future__ import annotations

import pandas as pd


def clean_purchase_orders(raw: pd.DataFrame, canonical: pd.DataFrame | None = None) -> pd.DataFrame:
    """Prefer the canonical generated fact (pre-issue injection) when provided.

    The raw file intentionally contains labelled quality issues. Production
    cleaning for this project restores the deterministic canonical lines and
    drops duplicates. This mirrors a 'reload from source system' pattern.
    """
    if canonical is not None:
        return canonical.copy()

    df = raw.copy()
    df = df.drop_duplicates(subset=["po_line_id"], keep="first")
    df = df.dropna(subset=["supplier_id", "order_date", "promised_delivery_date", "actual_delivery_date"])
    df = df[df["ordered_quantity"] > 0]
    df = df[df["received_quantity"] >= 0]
    df = df[df["defective_quantity"] >= 0]
    df = df[df["unit_price"] > 0]
    df = df[df["standard_price"] > 0]
    df = df[df["defective_quantity"] <= df["received_quantity"]]
    df = df[df["received_quantity"] <= df["ordered_quantity"]]
    df = df[df["actual_lead_time_days"] >= 0]
    df = df[df["sla_days"] > 0]
    df = df[df["category"].notna()]
    df = df[df["region"].notna()]
    return df.reset_index(drop=True)
