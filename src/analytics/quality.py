"""Quality / defect-rate analytics."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import safe_div


def defect_rate(defective: pd.Series, received: pd.Series) -> float:
    return float(safe_div(float(defective.sum()), float(received.sum())))


def quality_by(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col, dropna=False).agg(
        defective_quantity=("defective_quantity", "sum"),
        received_quantity=("received_quantity", "sum"),
        quality_failures=("quality_status", lambda s: int((s.isin(["REJECTED", "DEVIATION"])).sum())),
        po_lines=("po_line_id", "size"),
    ).reset_index()
    grouped["defect_rate"] = grouped.apply(
        lambda row: safe_div(row["defective_quantity"], row["received_quantity"]), axis=1
    )
    grouped["quality_failure_rate"] = grouped["quality_failures"] / grouped["po_lines"]
    return grouped
