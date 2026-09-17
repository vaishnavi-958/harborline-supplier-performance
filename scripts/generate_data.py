"""Generate synthetic procurement data only."""

from src.data.generate_synthetic_data import generate_all, save_generation
from src.utils.helpers import load_config


if __name__ == "__main__":
    cfg = load_config()
    result = generate_all(cfg)
    save_generation(result, cfg)
    print(f"Generated {len(result.fact_purchase_orders)} PO lines for {result.dim_supplier.supplier_id.nunique()} suppliers")
