"""Cost variance vs simulated standard price (analytical input, not actual cost)."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import safe_div


def cost_variance_by(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col, dropna=False).agg(
        actual_spend=("actual_spend", "sum"),
        expected_spend=("expected_spend", "sum"),
        ordered_spend=("ordered_spend", "sum"),
        po_lines=("po_line_id", "size"),
    ).reset_index()
    grouped["cost_variance"] = grouped["actual_spend"] - grouped["expected_spend"]
    grouped["cost_variance_pct"] = grouped.apply(
        lambda row: safe_div(row["cost_variance"], row["expected_spend"]), axis=1
    )
    return grouped
