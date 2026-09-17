import pandas as pd

from src.analytics.lead_time import lead_time_by, sla_status


def test_sla_status_bands():
    assert sla_status(0.02, 0.08, 0.15) == "COMPLIANT"
    assert sla_status(0.10, 0.08, 0.15) == "WATCH"
    assert sla_status(0.20, 0.08, 0.15) == "BREACH"


def test_lead_time_variance():
    df = pd.DataFrame(
        {
            "supplier_id": ["S", "S"],
            "actual_lead_time_days": [12, 18],
            "lead_time_variance_days": [0, 6],
            "sla_breach_flag": [0, 1],
        }
    )
    out = lead_time_by(df, "supplier_id").iloc[0]
    assert out["avg_lead_time"] == 15
    assert out["avg_lead_time_variance"] == 3
    assert out["sla_breach_rate"] == 0.5
