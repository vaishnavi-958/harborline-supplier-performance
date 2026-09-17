-- Supplier OTIF, monthly trend, and failure decomposition.

DROP VIEW IF EXISTS vw_supplier_otif;
CREATE VIEW vw_supplier_otif AS
WITH line AS (
    SELECT
        supplier_id,
        supplier_name,
        year_month,
        category,
        region,
        plant_name,
        otif_flag,
        late_only_flag,
        qty_short_only_flag,
        late_and_short_flag
    FROM fact_purchase_orders
)
SELECT
    supplier_id,
    supplier_name,
    COUNT(*) AS po_lines,
    AVG(otif_flag) AS otif_pct,
    AVG(late_only_flag) AS late_only_pct,
    AVG(qty_short_only_flag) AS qty_short_only_pct,
    AVG(late_and_short_flag) AS late_and_short_pct,
    1 - AVG(otif_flag) AS otif_failure_pct
FROM line
GROUP BY supplier_id, supplier_name;

DROP VIEW IF EXISTS vw_monthly_otif;
CREATE VIEW vw_monthly_otif AS
SELECT
    year_month,
    category,
    region,
    plant_name,
    COUNT(*) AS po_lines,
    AVG(otif_flag) AS otif_pct,
    AVG(late_only_flag) AS late_only_pct
FROM fact_purchase_orders
GROUP BY year_month, category, region, plant_name;
