from datetime import date, timedelta

import pandas as pd

from src.analytics.otif import otif_rate
from src.data.generate_synthetic_data import generate_all
from src.utils.helpers import load_config


def test_generation_is_deterministic():
    cfg = load_config()
    cfg = {
        **cfg,
        "generation": {**cfg["generation"], "num_po_lines": 400, "num_suppliers": 8},
    }
    a = generate_all(cfg).fact_purchase_orders
    b = generate_all(cfg).fact_purchase_orders
    pd.testing.assert_frame_equal(a, b)


def test_supplier_behavior_is_not_noise():
    cfg = load_config()
    cfg = {
        **cfg,
        "generation": {**cfg["generation"], "num_po_lines": 2500, "num_suppliers": 12},
    }
    fact = generate_all(cfg).fact_purchase_orders
    excellent = fact.loc[fact["supplier_id"] == "SUP-1001", "otif_flag"]
    late = fact.loc[fact["supplier_id"] == "SUP-1004", "otif_flag"]
    assert otif_rate(excellent) > otif_rate(late) + 0.12


def test_po_volume_and_date_window():
    cfg = load_config()
    cfg = {
        **cfg,
        "generation": {**cfg["generation"], "num_po_lines": 300, "num_suppliers": 6},
    }
    result = generate_all(cfg)
    assert len(result.fact_purchase_orders) == 300
    assert result.dim_supplier["supplier_id"].nunique() == 6
    start = date.fromisoformat(cfg["generation"]["start_date"])
    end = date.fromisoformat(cfg["generation"]["end_date"]) + timedelta(days=90)
    actual = pd.to_datetime(result.fact_purchase_orders["actual_delivery_date"])
    assert actual.min().date() >= start
    assert actual.max().date() <= end
