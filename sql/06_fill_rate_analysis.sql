DROP VIEW IF EXISTS vw_fill_rate;
CREATE VIEW vw_fill_rate AS
SELECT
    supplier_id,
    supplier_name,
    category,
    region,
    plant_name,
    year_month,
    SUM(ordered_quantity) AS ordered_quantity,
    SUM(received_quantity) AS received_quantity,
    CASE
        WHEN SUM(ordered_quantity) = 0 THEN 0
        ELSE SUM(received_quantity) * 1.0 / SUM(ordered_quantity)
    END AS fill_rate
FROM fact_purchase_orders
GROUP BY supplier_id, supplier_name, category, region, plant_name, year_month;
