import pandas as pd

from src.analytics.supplier_scorecard import build_pareto, build_supplier_scorecard
from src.data.transformation import transform_purchase_orders


def _dim():
    return pd.DataFrame(
        {
            "supplier_id": ["GOOD", "BAD"],
            "supplier_name": ["Northridge Precision Components", "Driftline Metals"],
            "supplier_region": ["Midwest", "South"],
            "supplier_category": ["Mechanical Components", "Metals"],
            "supplier_tier": ["Strategic", "Approved"],
            "archetype": ["excellent", "late_delivery"],
            "sla_days": [21, 26],
            "payment_terms": ["Net 45", "Net 30"],
        }
    )


def _fact():
    rows = []
    for i in range(20):
        rows.append(
            {
                "po_id": f"P-G-{i}",
                "po_line_id": f"G-{i}",
                "supplier_id": "GOOD",
                "supplier_name": "Northridge Precision Components",
                "order_date": "2025-01-01",
                "promised_delivery_date": "2025-01-20",
                "actual_delivery_date": "2025-01-19",
                "ordered_quantity": 100,
                "received_quantity": 100,
                "defective_quantity": 0,
                "unit_price": 10.0,
                "standard_price": 10.0,
                "sla_days": 21,
                "po_creation_date": "2024-12-20",
                "po_approval_date": "2024-12-22",
                "quality_status": "ACCEPTED",
            }
        )
    for i in range(20):
        rows.append(
            {
                "po_id": f"P-B-{i}",
                "po_line_id": f"B-{i}",
                "supplier_id": "BAD",
                "supplier_name": "Driftline Metals",
                "order_date": "2025-01-01",
                "promised_delivery_date": "2025-01-20",
                "actual_delivery_date": "2025-02-05",
                "ordered_quantity": 100,
                "received_quantity": 70,
                "defective_quantity": 8,
                "unit_price": 12.0,
                "standard_price": 10.0,
                "sla_days": 21,
                "po_creation_date": "2024-12-20",
                "po_approval_date": "2024-12-28",
                "quality_status": "REJECTED",
            }
        )
    return pd.DataFrame(rows)


def test_scorecard_is_derived_from_kpis():
    fact = transform_purchase_orders(_fact())
    card = build_supplier_scorecard(fact, _dim())
    ranked = card.set_index("supplier_id")
    assert ranked.loc["GOOD", "weighted_score"] > ranked.loc["BAD", "weighted_score"]
    assert ranked.loc["GOOD", "supplier_rank"] < ranked.loc["BAD", "supplier_rank"]
    assert ranked.loc["BAD", "risk_band"] in {"HIGH", "CRITICAL"}
    assert ranked.loc["GOOD", "otif_pct"] == 1
    assert ranked.loc["BAD", "otif_pct"] == 0


def test_pareto_cumulative_reaches_one():
    fact = transform_purchase_orders(_fact())
    card = build_supplier_scorecard(fact, _dim())
    pareto = build_pareto(card)
    assert abs(pareto["cumulative_pct"].iloc[-1] - 1) < 1e-9
    assert pareto.iloc[0]["supplier_id"] == "BAD"
