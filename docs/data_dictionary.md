# Data dictionary

All entities are synthetic.

## dim_supplier

| Column | Meaning |
| --- | --- |
| supplier_id | Synthetic key, `SUP-10xx` |
| supplier_name | Fabricated trading name |
| supplier_region | Midwest, West, Northeast, South |
| supplier_category | Primary commodity family |
| supplier_tier | Analytical: Strategic, Preferred, Approved, Transactional |
| contract_start_date / contract_end_date | Simulated contract window |
| sla_days | Maximum allowable actual lead time |
| payment_terms | Net 15 / 30 / 45 / 60 |
| primary_contact_role | Role only — no personal names or emails |

Behavioral columns (`base_otif_rate`, `base_defect_rate`, …) stay in the generator profile and the processed supplier file for transparency. They are not Power BI facts.

## fact_purchase_orders

PO line grain. One row is one purchase-order line.

Key fields: `po_id`, `po_line_id`, supplier, material, plant, `order_date`, `requested_delivery_date`, `promised_delivery_date`, `actual_delivery_date`, quantities, `unit_price`, `standard_price` (simulated), `sla_days`, carrier, statuses.

Derived: `delivery_days_late`, `delivery_days_early`, `quantity_shortfall`, `defect_rate`, `cost_variance`, `cost_variance_pct`, `otif_flag`, `fill_rate`, `sla_breach_flag`, OTIF failure split flags, `po_turnaround_days`, spend measures.

`po_creation_date` and `po_approval_date` are synthetic workflow timestamps used only to compute PO processing time.
