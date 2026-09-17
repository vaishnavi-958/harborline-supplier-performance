import pandas as pd

from src.analytics.otif import otif_by, otif_rate
from src.data.transformation import transform_purchase_orders


def _lines():
    return pd.DataFrame(
        {
            "po_line_id": ["A-1", "A-2", "A-3", "A-4"],
            "supplier_id": ["S1", "S1", "S1", "S2"],
            "order_date": ["2025-01-01"] * 4,
            "promised_delivery_date": ["2025-01-10"] * 4,
            "actual_delivery_date": ["2025-01-10", "2025-01-12", "2025-01-09", "2025-01-10"],
            "ordered_quantity": [100, 100, 100, 50],
            "received_quantity": [100, 100, 80, 50],
            "defective_quantity": [0, 0, 0, 0],
            "unit_price": [10, 10, 10, 10],
            "standard_price": [10, 10, 10, 10],
            "sla_days": [12, 12, 12, 12],
            "po_creation_date": ["2024-12-28"] * 4,
            "po_approval_date": ["2024-12-30"] * 4,
            "quality_status": ["ACCEPTED"] * 4,
        }
    )


def test_otif_definition():
    fact = transform_purchase_orders(_lines())
    # line 1 on time in full, line 2 late, line 3 short, line 4 on time in full
    assert list(fact["otif_flag"]) == [1, 0, 0, 1]
    assert list(fact["late_only_flag"]) == [0, 1, 0, 0]
    assert list(fact["qty_short_only_flag"]) == [0, 0, 1, 0]
    assert otif_rate(fact["otif_flag"]) == 0.5


def test_otif_by_supplier():
    fact = transform_purchase_orders(_lines())
    by = otif_by(fact, "supplier_id").set_index("supplier_id")
    assert round(by.loc["S1", "otif_pct"], 4) == round(1 / 3, 4)
    assert by.loc["S2", "otif_pct"] == 1
