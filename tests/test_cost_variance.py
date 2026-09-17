import pandas as pd

from src.analytics.cost_variance import cost_variance_by


def test_cost_variance_formula():
    df = pd.DataFrame(
        {
            "supplier_id": ["C", "C"],
            "actual_spend": [120, 80],
            "expected_spend": [100, 80],
            "ordered_spend": [120, 80],
            "po_line_id": [1, 2],
        }
    )
    row = cost_variance_by(df, "supplier_id").iloc[0]
    assert row["cost_variance"] == 20
    assert row["cost_variance_pct"] == 20 / 180
