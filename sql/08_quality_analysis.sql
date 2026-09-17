DROP VIEW IF EXISTS vw_quality;
CREATE VIEW vw_quality AS
SELECT
    supplier_id,
    supplier_name,
    category,
    material_id,
    material_description,
    region,
    SUM(defective_quantity) AS defective_quantity,
    SUM(received_quantity) AS received_quantity,
    CASE
        WHEN SUM(received_quantity) = 0 THEN 0
        ELSE SUM(defective_quantity) * 1.0 / SUM(received_quantity)
    END AS defect_rate,
    AVG(CASE WHEN quality_status IN ('REJECTED', 'DEVIATION') THEN 1.0 ELSE 0 END) AS quality_failure_rate
FROM fact_purchase_orders
GROUP BY supplier_id, supplier_name, category, material_id, material_description, region;
