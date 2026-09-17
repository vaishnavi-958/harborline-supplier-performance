import pandas as pd

from src.data.validation import run_checks
from src.data.cleaning import clean_purchase_orders


def test_quality_report_flags_known_issues():
    df = pd.DataFrame(
        {
            "po_line_id": ["1", "1", "2"],
            "supplier_id": [None, "S", "S"],
            "order_date": [None, "2025-01-01", "2025-01-01"],
            "promised_delivery_date": ["2025-01-10", "2025-01-10", "2025-01-10"],
            "actual_delivery_date": ["2025-01-10", "2025-01-10", "2025-01-10"],
            "ordered_quantity": [-2, 10, 10],
            "received_quantity": [0, 10, 12],
            "defective_quantity": [0, 11, 0],
            "unit_price": [-1, 5, 5],
            "standard_price": [5, 5, 5],
            "actual_lead_time_days": [-1, 9, 9],
            "sla_days": [0, 12, 12],
            "category": [None, "Metals", "Metals"],
            "region": [None, "South", "South"],
        }
    )
    report = run_checks(df).set_index("check_id")
    assert report.loc["duplicate_po_lines", "status"] == "FAIL"
    assert report.loc["missing_supplier", "status"] == "FAIL"
    assert report.loc["negative_prices", "status"] == "FAIL"


def test_cleaning_drops_invalid_rows():
    raw = pd.DataFrame(
        {
            "po_line_id": ["a", "b"],
            "supplier_id": [None, "S"],
            "order_date": ["2025-01-01", "2025-01-01"],
            "promised_delivery_date": ["2025-01-10", "2025-01-10"],
            "actual_delivery_date": ["2025-01-10", "2025-01-10"],
            "ordered_quantity": [10, 10],
            "received_quantity": [10, 10],
            "defective_quantity": [0, 0],
            "unit_price": [5, 5],
            "standard_price": [5, 5],
            "actual_lead_time_days": [9, 9],
            "sla_days": [12, 12],
            "category": ["Metals", "Metals"],
            "region": ["South", "South"],
        }
    )
    cleaned = clean_purchase_orders(raw)
    assert len(cleaned) == 1
