import pandas as pd

from src.analytics.quality import defect_rate, quality_by


def test_defect_rate_zero_received():
    assert defect_rate(pd.Series([0]), pd.Series([0])) == 0


def test_quality_by_supplier():
    df = pd.DataFrame(
        {
            "po_line_id": [1, 2],
            "supplier_id": ["Q", "Q"],
            "defective_quantity": [5, 0],
            "received_quantity": [100, 50],
            "quality_status": ["REJECTED", "ACCEPTED"],
        }
    )
    by = quality_by(df, "supplier_id").iloc[0]
    assert by["defect_rate"] == 5 / 150
    assert by["quality_failure_rate"] == 0.5
