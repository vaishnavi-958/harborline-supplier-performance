import pandas as pd

from src.analytics.fill_rate import fill_rate, fill_rate_by


def test_fill_rate_handles_zero_ordered():
    assert fill_rate(pd.Series([0, 0]), pd.Series([0, 0])) == 0


def test_fill_rate_by_supplier():
    df = pd.DataFrame(
        {
            "po_line_id": [1, 2, 3],
            "supplier_id": ["A", "A", "B"],
            "ordered_quantity": [100, 50, 20],
            "received_quantity": [90, 50, 20],
        }
    )
    by = fill_rate_by(df, "supplier_id").set_index("supplier_id")
    assert by.loc["A", "fill_rate"] == 140 / 150
    assert by.loc["B", "fill_rate"] == 1
