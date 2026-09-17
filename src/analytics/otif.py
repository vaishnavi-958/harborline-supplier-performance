"""OTIF calculations. Default definition is documented in docs/kpi_definitions.md."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import safe_div


def otif_rate(flags: pd.Series) -> float:
    return float(safe_div(float(flags.sum()), float(len(flags))))


def otif_by(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col, dropna=False)
    out = grouped.agg(
        po_lines=("otif_flag", "size"),
        otif_hits=("otif_flag", "sum"),
        late_only=("late_only_flag", "sum"),
        qty_short_only=("qty_short_only_flag", "sum"),
        late_and_short=("late_and_short_flag", "sum"),
    ).reset_index()
    out["otif_pct"] = out["otif_hits"] / out["po_lines"]
    out["late_only_pct"] = out["late_only"] / out["po_lines"]
    out["qty_short_only_pct"] = out["qty_short_only"] / out["po_lines"]
    out["late_and_short_pct"] = out["late_and_short"] / out["po_lines"]
    out["otif_failure_pct"] = 1 - out["otif_pct"]
    return out
