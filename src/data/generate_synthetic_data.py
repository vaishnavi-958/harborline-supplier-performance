"""Generate a synthetic procurement dataset with supplier-level behavior.

Independent Procurement Analytics Project using a synthetic procurement dataset.
Supplier names, plants, and prices are fabricated analytical inputs — not
real companies or actual procurement costs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
from faker import Faker

from src.utils.helpers import load_config, load_supplier_profiles, project_path
from src.utils.logging_config import configure_logging

LOGGER = configure_logging()

MATERIALS: list[tuple[str, str, str]] = [
    ("MAT-4101", "Stainless hex bolt M8", "Fasteners"),
    ("MAT-4102", "Lock washer 8mm", "Fasteners"),
    ("MAT-4103", "Grade 8 flange nut", "Fasteners"),
    ("MAT-4201", "Cold-rolled steel sheet 16ga", "Metals"),
    ("MAT-4202", "Aluminum extrusion 6063", "Metals"),
    ("MAT-4203", "Copper bus bar 1/4 in", "Metals"),
    ("MAT-4204", "Cast iron housing blank", "Metals"),
    ("MAT-4301", "ABS resin pellet natural", "Plastics"),
    ("MAT-4302", "Nylon 6/6 rod 20mm", "Plastics"),
    ("MAT-4303", "HDPE drum liner", "Plastics"),
    ("MAT-4401", "Corrugated RSC 24x18x12", "Packaging"),
    ("MAT-4402", "Stretch wrap 18 in", "Packaging"),
    ("MAT-4403", "Label stock 4x6 thermal", "Packaging"),
    ("MAT-4404", "Chipboard divider pack", "Packaging"),
    ("MAT-4501", "PCB assembly 24V I/O", "Electronics"),
    ("MAT-4502", "Proximity sensor M12", "Electronics"),
    ("MAT-4503", "Relay module 8-channel", "Electronics"),
    ("MAT-4504", "Power supply 24V 10A", "Electronics"),
    ("MAT-4601", "Hydraulic hose 1/2 in", "Fluid Handling"),
    ("MAT-4602", "Ball valve 2 in SS", "Fluid Handling"),
    ("MAT-4603", "Centrifugal pump 5HP", "Fluid Handling"),
    ("MAT-4604", "Gasket kit Buna-N", "Fluid Handling"),
    ("MAT-4701", "Nitrile gloves L", "MRO"),
    ("MAT-4702", "HEPA filter 24x24", "MRO"),
    ("MAT-4703", "Safety glasses clear", "MRO"),
    ("MAT-4704", "Threadlocker 50ml", "MRO"),
    ("MAT-4801", "Epoxy adhesive 400ml", "Chemicals"),
    ("MAT-4802", "Industrial coating grey", "Chemicals"),
    ("MAT-4803", "ISO 46 hydraulic oil", "Chemicals"),
    ("MAT-4804", "Solvent wipe canister", "Chemicals"),
    ("MAT-4901", "THHN 12 AWG black", "Electrical"),
    ("MAT-4902", "LED high-bay 150W", "Electrical"),
    ("MAT-4903", "Contactor 40A", "Electrical"),
    ("MAT-5001", "Ceramic fiber blanket", "Building Materials"),
    ("MAT-5002", "Firebrick 9x4.5x2.5", "Building Materials"),
    ("MAT-5003", "Mineral wool batt", "Building Materials"),
    ("MAT-5101", "Deep groove bearing 6205", "Mechanical Components"),
    ("MAT-5102", "Timing belt 8M 25mm", "Mechanical Components"),
    ("MAT-5103", "Shaft seal 35x52x7", "Mechanical Components"),
    ("MAT-5104", "Helical gear 20T", "Mechanical Components"),
    ("MAT-5105", "AC motor 3HP 1760rpm", "Mechanical Components"),
]

PLANTS = [
    ("PLT-HOU", "Houston DC", "South"),
    ("PLT-CHI", "Chicago Plant", "Midwest"),
    ("PLT-EWR", "Newark Hub", "Northeast"),
    ("PLT-PHX", "Phoenix DC", "West"),
    ("PLT-ATL", "Atlanta Plant", "South"),
    ("PLT-MSP", "Minneapolis Plant", "Midwest"),
]

CARRIERS = [
    ("CAR-11", "Northhaul Freight"),
    ("CAR-12", "Ridgeway LTL"),
    ("CAR-13", "Coastal Parcel"),
    ("CAR-14", "Inland Dedicated"),
    ("CAR-15", "Supplier-managed"),
]

CONTACT_ROLES = [
    "Account manager",
    "Customer service lead",
    "Plant scheduler",
    "Quality engineer",
    "Logistics coordinator",
]


@dataclass
class GenerationResult:
    dim_supplier: pd.DataFrame
    dim_material: pd.DataFrame
    dim_category: pd.DataFrame
    dim_region: pd.DataFrame
    dim_plant: pd.DataFrame
    dim_date: pd.DataFrame
    dim_carrier: pd.DataFrame
    fact_purchase_orders: pd.DataFrame
    fact_raw: pd.DataFrame


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def _assign_tier(importance: float, annual_weight: float) -> str:
    """Analytical segmentation, not a real procurement policy."""
    score = 0.6 * importance + 0.4 * annual_weight
    if score >= 0.78:
        return "Strategic"
    if score >= 0.58:
        return "Preferred"
    if score >= 0.40:
        return "Approved"
    return "Transactional"


def _trend_multiplier(trend: str, progress: float) -> float:
    """progress is 0 at start date, 1 at end date."""
    if trend == "improving":
        return 0.82 + 0.28 * progress
    if trend == "worsening":
        return 1.12 - 0.30 * progress
    return 1.0


def build_dimensions(profiles: list[dict[str, Any]], rng: np.random.Generator) -> dict[str, pd.DataFrame]:
    fake = Faker()
    Faker.seed(42)

    importance = np.array([float(p["importance"]) for p in profiles])
    weights = importance / importance.sum()
    suppliers = []
    for profile, weight in zip(profiles, weights):
        start = datetime(2021, 1, 1) + timedelta(days=int(rng.integers(0, 600)))
        end = datetime(2027, 12, 31)
        suppliers.append(
            {
                "supplier_id": profile["supplier_id"],
                "supplier_name": profile["supplier_name"],
                "supplier_region": profile["region"],
                "supplier_category": profile["category"],
                "supplier_tier": _assign_tier(float(profile["importance"]), float(weight * 12)),
                "contract_start_date": start.date().isoformat(),
                "contract_end_date": end.date().isoformat(),
                "sla_days": int(profile["sla_days"]),
                "payment_terms": profile["payment_terms"],
                "primary_contact_role": rng.choice(CONTACT_ROLES),
                "archetype": profile["archetype"],
                "base_otif_rate": profile["base_otif_rate"],
                "base_defect_rate": profile["base_defect_rate"],
                "base_lead_time": profile["base_lead_time"],
                "lead_time_variability": profile["lead_time_variability"],
                "cost_variance_rate": profile["cost_variance_rate"],
                "capacity_factor": profile["capacity_factor"],
                "fill_rate_base": profile["fill_rate_base"],
                "importance": profile["importance"],
                "trend": profile.get("trend", "stable"),
                "seasonal_delay_months": ",".join(
                    str(m) for m in profile.get("seasonal_delay_months", [])
                ),
            }
        )
    dim_supplier = pd.DataFrame(suppliers)

    dim_material = pd.DataFrame(
        [
            {
                "material_id": mid,
                "material_description": desc,
                "category": cat,
                "standard_price": round(float(rng.uniform(4.5, 420.0)), 2),
            }
            for mid, desc, cat in MATERIALS
        ]
    )
    dim_category = pd.DataFrame(
        {"category": sorted({row[2] for row in MATERIALS})}
    ).assign(category_id=lambda d: [f"CAT-{i:02d}" for i in range(1, len(d) + 1)])
    dim_region = pd.DataFrame(
        {"region": ["Midwest", "West", "Northeast", "South"], "region_id": ["RG-MW", "RG-WE", "RG-NE", "RG-SO"]}
    )
    dim_plant = pd.DataFrame(
        [{"plant_id": pid, "plant_name": name, "region": region} for pid, name, region in PLANTS]
    )
    dim_carrier = pd.DataFrame(
        [{"carrier_id": cid, "carrier": name} for cid, name in CARRIERS]
    )

    start = pd.Timestamp("2024-01-01")
    end = pd.Timestamp("2026-02-28")
    dates = pd.date_range(start, end, freq="D")
    dim_date = pd.DataFrame(
        {
            "date_key": dates.strftime("%Y%m%d").astype(int),
            "date": dates.strftime("%Y-%m-%d"),
            "year": dates.year,
            "quarter": dates.quarter,
            "month": dates.month,
            "month_name": dates.strftime("%b"),
            "year_month": dates.strftime("%Y-%m"),
            "week": dates.isocalendar().week.astype(int),
            "day_of_week": dates.day_name(),
            "is_weekend": dates.dayofweek >= 5,
        }
    )
    _ = fake  # reserved for optional descriptive fields
    return {
        "dim_supplier": dim_supplier,
        "dim_material": dim_material,
        "dim_category": dim_category,
        "dim_region": dim_region,
        "dim_plant": dim_plant,
        "dim_carrier": dim_carrier,
        "dim_date": dim_date,
    }


def generate_purchase_orders(
    config: dict[str, Any],
    profiles: list[dict[str, Any]],
    dims: dict[str, pd.DataFrame],
    rng: np.random.Generator,
) -> pd.DataFrame:
    n = int(config["generation"]["num_po_lines"])
    start = pd.Timestamp(config["generation"]["start_date"])
    end = pd.Timestamp(config["generation"]["end_date"])
    span_days = (end - start).days

    suppliers = dims["dim_supplier"]
    materials = dims["dim_material"]
    plants = dims["dim_plant"]
    carriers = dims["dim_carrier"]

    importance = suppliers["importance"].to_numpy(dtype=float)
    weights = importance / importance.sum()
    supplier_idx = rng.choice(len(suppliers), size=n, p=weights)

    material_idx = rng.integers(0, len(materials), size=n)
    plant_idx = rng.integers(0, len(plants), size=n)
    carrier_idx = rng.integers(0, len(carriers), size=n)

    order_offsets = rng.integers(0, span_days + 1, size=n)
    order_dates = start + pd.to_timedelta(order_offsets, unit="D")
    # Skip weekends for order dates
    order_dates = order_dates + pd.to_timedelta(
        np.where(order_dates.dayofweek == 5, 2, np.where(order_dates.dayofweek == 6, 1, 0)),
        unit="D",
    )

    selected = suppliers.iloc[supplier_idx].reset_index(drop=True)
    mat = materials.iloc[material_idx].reset_index(drop=True)
    plt = plants.iloc[plant_idx].reset_index(drop=True)
    car = carriers.iloc[carrier_idx].reset_index(drop=True)

    progress = order_offsets / max(span_days, 1)
    trend = selected["trend"].to_numpy()
    trend_mult = np.ones(n)
    trend_mult = np.where(trend == "improving", 0.82 + 0.28 * progress, trend_mult)
    trend_mult = np.where(trend == "worsening", 1.12 - 0.30 * progress, trend_mult)

    base_lead = selected["base_lead_time"].to_numpy(dtype=float)
    variability = selected["lead_time_variability"].to_numpy(dtype=float)
    promised_lead = np.clip(
        np.round(base_lead + rng.normal(0, 0.35, n)), 3, None
    ).astype(int)

    otif_rate = np.clip(selected["base_otif_rate"].to_numpy(dtype=float) * trend_mult, 0.35, 0.995)
    months = order_dates.month.to_numpy() if hasattr(order_dates.month, "to_numpy") else np.asarray(order_dates.month)
    seasonal_mask = np.zeros(n, dtype=bool)
    for i, months_csv in enumerate(selected["seasonal_delay_months"].to_numpy()):
        if not months_csv:
            continue
        allowed = {int(x) for x in str(months_csv).split(",") if x}
        if int(months[i]) in allowed:
            seasonal_mask[i] = True
    otif_rate = np.where(seasonal_mask, otif_rate * 0.58, otif_rate)
    on_time = rng.random(n) < otif_rate

    delay = np.zeros(n)
    late_mask = ~on_time
    delay[late_mask] = np.clip(
        rng.gamma(1.6, variability[late_mask] * 0.9) + 1, 1, 28
    )
    delay = np.where(seasonal_mask & late_mask, delay + rng.integers(2, 8, n), delay)

    early = np.where(on_time & (rng.random(n) < 0.22), rng.integers(0, 3, n), 0)
    actual_lead = promised_lead + delay.astype(int) - early.astype(int)
    actual_lead = np.clip(actual_lead, 2, None)

    requested_lead = np.clip(promised_lead + rng.integers(-1, 2, n), 3, None)
    promised_dates = order_dates + pd.to_timedelta(promised_lead, unit="D")
    requested_dates = order_dates + pd.to_timedelta(requested_lead, unit="D")
    actual_dates = order_dates + pd.to_timedelta(actual_lead, unit="D")

    ordered_qty = rng.choice(
        [10, 12, 20, 24, 25, 48, 50, 100, 120, 200, 250, 500, 1000],
        size=n,
        p=[0.06, 0.05, 0.08, 0.07, 0.08, 0.08, 0.10, 0.14, 0.08, 0.10, 0.06, 0.06, 0.04],
    ).astype(float)
    ordered_qty = np.round(ordered_qty * rng.uniform(0.8, 1.35, n), 0)

    fill_base = np.clip(
        selected["fill_rate_base"].to_numpy(dtype=float)
        * selected["capacity_factor"].to_numpy(dtype=float),
        0.55,
        0.999,
    )
    in_full = rng.random(n) < fill_base
    partial_frac = rng.uniform(0.62, 0.94, n)
    received_qty = np.where(in_full, ordered_qty, np.round(ordered_qty * partial_frac, 0))
    received_qty = np.minimum(np.maximum(received_qty, 0), ordered_qty)

    defect_rate = np.clip(
        selected["base_defect_rate"].to_numpy(dtype=float) / np.clip(trend_mult, 0.7, 1.3),
        0.0,
        0.25,
    )
    defect_draw = np.clip(rng.normal(defect_rate, defect_rate * 0.35 + 0.002, n), 0, 0.4)
    defective_qty = np.round(received_qty * defect_draw, 0)
    defective_qty = np.minimum(defective_qty, received_qty)

    std_price = mat["standard_price"].to_numpy(dtype=float)
    cv = selected["cost_variance_rate"].to_numpy(dtype=float)
    unit_price = np.round(std_price * (1 + rng.normal(cv * 0.35, cv * 0.55, n)), 2)
    unit_price = np.clip(unit_price, 0.5, None)

    approval_days = np.clip(np.round(rng.gamma(2.8, 1.6, n)), 1, 21).astype(int)
    approval_dates = order_dates - pd.to_timedelta(rng.integers(0, 2, n), unit="D")
    creation_dates = approval_dates - pd.to_timedelta(approval_days, unit="D")

    sla_days = selected["sla_days"].to_numpy(dtype=int)
    delivery_days_late = np.maximum((actual_dates - promised_dates).days, 0)
    delivery_days_early = np.maximum((promised_dates - actual_dates).days, 0)
    qty_shortfall = np.maximum(ordered_qty - received_qty, 0)
    line_defect_rate = np.where(received_qty > 0, defective_qty / received_qty, 0.0)
    cost_var = unit_price - std_price
    cost_var_pct = np.where(std_price > 0, cost_var / std_price, 0.0)
    fill_rate = np.where(ordered_qty > 0, received_qty / ordered_qty, 0.0)

    tol_days = int(config["otif"]["delivery_tolerance_days"])
    tol_qty = float(config["otif"]["quantity_tolerance_pct"])
    on_time_flag = actual_dates <= (promised_dates + pd.to_timedelta(tol_days, unit="D"))
    in_full_flag = received_qty >= ordered_qty * (1 - tol_qty)
    otif_flag = (on_time_flag & in_full_flag).astype(int)

    sla_breach = (actual_lead > sla_days).astype(int)
    quality_status = np.where(
        received_qty == 0,
        "NO RECEIPT",
        np.where(defective_qty == 0, "ACCEPTED", np.where(line_defect_rate > 0.05, "REJECTED", "DEVIATION")),
    )
    delivery_status = np.where(
        ~on_time_flag & ~in_full_flag,
        "LATE_SHORT",
        np.where(~on_time_flag, "LATE", np.where(~in_full_flag, "SHORT", np.where(delivery_days_early > 0, "EARLY", "ON_TIME"))),
    )

    po_ids = [f"45{1000000 + i // 2:07d}" for i in range(n)]
    po_line_ids = [f"{po_ids[i]}-{1 if i % 2 == 0 else 2:05d}" for i in range(n)]

    fact = pd.DataFrame(
        {
            "po_id": po_ids,
            "po_line_id": po_line_ids,
            "supplier_id": selected["supplier_id"].to_numpy(),
            "supplier_name": selected["supplier_name"].to_numpy(),
            "material_id": mat["material_id"].to_numpy(),
            "material_description": mat["material_description"].to_numpy(),
            "category": mat["category"].to_numpy(),
            "region": plt["region"].to_numpy(),
            "plant": plt["plant_id"].to_numpy(),
            "plant_name": plt["plant_name"].to_numpy(),
            "order_date": order_dates.strftime("%Y-%m-%d"),
            "po_creation_date": creation_dates.strftime("%Y-%m-%d"),
            "po_approval_date": approval_dates.strftime("%Y-%m-%d"),
            "requested_delivery_date": requested_dates.strftime("%Y-%m-%d"),
            "promised_delivery_date": promised_dates.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_dates.strftime("%Y-%m-%d"),
            "ordered_quantity": ordered_qty,
            "received_quantity": received_qty,
            "defective_quantity": defective_qty,
            "unit_price": unit_price,
            "standard_price": std_price,
            "currency": config["generation"]["currency"],
            "payment_terms": selected["payment_terms"].to_numpy(),
            "lead_time_days": promised_lead,
            "actual_lead_time_days": actual_lead,
            "lead_time_variance_days": actual_lead - promised_lead,
            "sla_days": sla_days,
            "carrier": car["carrier"].to_numpy(),
            "carrier_id": car["carrier_id"].to_numpy(),
            "delivery_status": delivery_status,
            "quality_status": quality_status,
            "delivery_days_late": delivery_days_late,
            "delivery_days_early": delivery_days_early,
            "quantity_shortfall": qty_shortfall,
            "defect_rate": np.round(line_defect_rate, 6),
            "cost_variance": np.round(cost_var, 4),
            "cost_variance_pct": np.round(cost_var_pct, 6),
            "otif_flag": otif_flag,
            "fill_rate": np.round(fill_rate, 6),
            "sla_breach_flag": sla_breach,
            "late_only_flag": ((~on_time_flag) & in_full_flag).astype(int),
            "qty_short_only_flag": (on_time_flag & (~in_full_flag)).astype(int),
            "late_and_short_flag": ((~on_time_flag) & (~in_full_flag)).astype(int),
            "po_turnaround_days": approval_days,
            "actual_spend": np.round(received_qty * unit_price, 2),
            "expected_spend": np.round(received_qty * std_price, 2),
            "ordered_spend": np.round(ordered_qty * unit_price, 2),
            "year_month": order_dates.strftime("%Y-%m"),
        }
    )
    return fact.sort_values(["order_date", "po_line_id"]).reset_index(drop=True)


def inject_raw_issues(fact: pd.DataFrame, rng: np.random.Generator, rate: float) -> pd.DataFrame:
    """Labelled synthetic defects for the data-quality report only."""
    raw = fact.copy()
    n = len(raw)
    k = max(8, int(n * rate))
    idx = rng.choice(n, size=k, replace=False)
    slices = np.array_split(idx, 8)
    if len(slices[0]):
        raw.loc[slices[0], "supplier_id"] = None
    if len(slices[1]):
        raw.loc[slices[1], "order_date"] = None
    if len(slices[2]):
        raw.loc[slices[2], "ordered_quantity"] = -5
    if len(slices[3]):
        raw.loc[slices[3], "unit_price"] = -1.0
    if len(slices[4]):
        raw.loc[slices[4], "defective_quantity"] = raw.loc[slices[4], "received_quantity"] + 12
    if len(slices[5]):
        raw.loc[slices[5], "actual_lead_time_days"] = -3
    if len(slices[6]):
        raw.loc[slices[6], "category"] = None
    if len(slices[7]):
        raw.loc[slices[7], "region"] = None
    # Duplicate a handful of clean lines
    dup = raw.iloc[rng.choice(n, size=6, replace=False)]
    raw = pd.concat([raw, dup], ignore_index=True)
    return raw


def generate_all(config: dict[str, Any] | None = None) -> GenerationResult:
    config = config or load_config()
    profiles = load_supplier_profiles()["suppliers"]
    n_suppliers = int(config["generation"]["num_suppliers"])
    profiles = profiles[:n_suppliers]
    seed = int(config["random_seed"])
    rng = _rng(seed)

    LOGGER.info("Generating dimensions for %s suppliers", len(profiles))
    dims = build_dimensions(profiles, rng)
    LOGGER.info("Generating %s purchase-order lines", config["generation"]["num_po_lines"])
    fact = generate_purchase_orders(config, profiles, dims, rng)
    raw = inject_raw_issues(fact, rng, float(config["generation"]["raw_issue_rate"]))
    return GenerationResult(
        dim_supplier=dims["dim_supplier"],
        dim_material=dims["dim_material"],
        dim_category=dims["dim_category"],
        dim_region=dims["dim_region"],
        dim_plant=dims["dim_plant"],
        dim_date=dims["dim_date"],
        dim_carrier=dims["dim_carrier"],
        fact_purchase_orders=fact,
        fact_raw=raw,
    )


def save_generation(result: GenerationResult, config: dict[str, Any] | None = None) -> None:
    config = config or load_config()
    raw_dir = project_path(config["paths"]["raw_dir"])
    proc_dir = project_path(config["paths"]["processed_dir"])
    raw_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)

    result.fact_raw.to_csv(raw_dir / "fact_purchase_orders_raw.csv", index=False)
    result.fact_purchase_orders.to_csv(proc_dir / "fact_purchase_orders.csv", index=False)
    for name in [
        "dim_supplier",
        "dim_material",
        "dim_category",
        "dim_region",
        "dim_plant",
        "dim_date",
        "dim_carrier",
    ]:
        getattr(result, name).to_csv(proc_dir / f"{name}.csv", index=False)
        getattr(result, name).to_csv(raw_dir / f"{name}.csv", index=False)
    LOGGER.info("Wrote raw and processed CSV files")


if __name__ == "__main__":
    cfg = load_config()
    generated = generate_all(cfg)
    save_generation(generated, cfg)
