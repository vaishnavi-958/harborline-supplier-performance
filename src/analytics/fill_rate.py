"""Fill rate = total received quantity / total ordered quantity."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import safe_div


def fill_rate(ordered: pd.Series, received: pd.Series) -> float:
    return float(safe_div(float(received.sum()), float(ordered.sum())))


def fill_rate_by(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col, dropna=False).agg(
        ordered_quantity=("ordered_quantity", "sum"),
        received_quantity=("received_quantity", "sum"),
        po_lines=("po_line_id", "size"),
    ).reset_index()
    grouped["fill_rate"] = grouped.apply(
        lambda row: safe_div(row["received_quantity"], row["ordered_quantity"]), axis=1
    )
    return grouped
