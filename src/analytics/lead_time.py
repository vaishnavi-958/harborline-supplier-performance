"""Lead-time and SLA analytics."""

from __future__ import annotations

import pandas as pd


def lead_time_by(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col, dropna=False)["actual_lead_time_days"]
    variance = df.groupby(group_col, dropna=False)["lead_time_variance_days"]
    sla = df.groupby(group_col, dropna=False)["sla_breach_flag"]
    out = pd.DataFrame(
        {
            "avg_lead_time": grouped.mean(),
            "median_lead_time": grouped.median(),
            "stdev_lead_time": grouped.std(ddof=0),
            "p90_lead_time": grouped.quantile(0.90),
            "avg_lead_time_variance": variance.mean(),
            "sla_breach_rate": sla.mean(),
            "po_lines": grouped.size(),
        }
    ).reset_index()
    return out


def sla_status(breach_rate: float, watch: float, breach: float) -> str:
    if breach_rate >= breach:
        return "BREACH"
    if breach_rate >= watch:
        return "WATCH"
    return "COMPLIANT"
