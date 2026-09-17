# Power BI data model

Star schema. Avoid many-to-many.

## Relationships (single direction, one-to-many)

| From | To | Key |
| --- | --- | --- |
| dim_date | fact_purchase_orders | dim_date[date] → fact[order_date] |
| dim_supplier | fact_purchase_orders | supplier_id |
| dim_material | fact_purchase_orders | material_id |
| dim_category | fact_purchase_orders | category |
| dim_region | fact_purchase_orders | region |
| dim_plant | fact_purchase_orders | plant |
| dim_carrier | fact_purchase_orders | carrier_id |

Inactive relationship option: dim_date to `actual_delivery_date` for delivery-dated views (USERELATIONSHIP).

## Analytical tables (imported, not related many-to-many)

- supplier_scorecard (1:1 with dim_supplier)
- supplier_monthly_kpi
- supplier_risk (subset/view of scorecard)
- supplier_pareto

Hide fact keys that are not used on visuals. Do not relate pareto to fact on problem_count.
