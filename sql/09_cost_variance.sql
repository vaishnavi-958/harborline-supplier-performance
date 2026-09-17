DROP VIEW IF EXISTS vw_cost_variance;
CREATE VIEW vw_cost_variance AS
SELECT
    supplier_id,
    supplier_name,
    category,
    material_id,
    year_month,
    SUM(actual_spend) AS actual_spend,
    SUM(expected_spend) AS expected_spend,
    SUM(actual_spend) - SUM(expected_spend) AS cost_variance,
    CASE
        WHEN SUM(expected_spend) = 0 THEN 0
        ELSE (SUM(actual_spend) - SUM(expected_spend)) * 1.0 / SUM(expected_spend)
    END AS cost_variance_pct
FROM fact_purchase_orders
GROUP BY supplier_id, supplier_name, category, material_id, year_month;
