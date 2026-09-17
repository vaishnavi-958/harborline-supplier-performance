-- Power BI / Harborline dashboard views.

DROP VIEW IF EXISTS vw_pbi_exec_kpis;
CREATE VIEW vw_pbi_exec_kpis AS
SELECT
    COUNT(DISTINCT supplier_id) AS total_suppliers,
    COUNT(DISTINCT po_id) AS total_pos,
    COUNT(*) AS total_lines,
    SUM(actual_spend) AS total_spend,
    AVG(otif_flag) AS otif_pct,
    CASE WHEN SUM(ordered_quantity) = 0 THEN 0 ELSE SUM(received_quantity) * 1.0 / SUM(ordered_quantity) END AS fill_rate,
    CASE WHEN SUM(received_quantity) = 0 THEN 0 ELSE SUM(defective_quantity) * 1.0 / SUM(received_quantity) END AS defect_rate,
    1 - AVG(sla_breach_flag) AS sla_compliance,
    SUM(actual_spend) - SUM(expected_spend) AS cost_variance
FROM fact_purchase_orders;

DROP VIEW IF EXISTS vw_pbi_pareto;
CREATE VIEW vw_pbi_pareto AS
SELECT
    supplier_id,
    supplier_name,
    problem_count,
    problem_pct,
    cumulative_pct
FROM supplier_pareto;

DROP VIEW IF EXISTS vw_pbi_region_performance;
CREATE VIEW vw_pbi_region_performance AS
SELECT
    region,
    COUNT(DISTINCT supplier_id) AS suppliers,
    AVG(otif_flag) AS otif_pct,
    CASE WHEN SUM(ordered_quantity) = 0 THEN 0 ELSE SUM(received_quantity) * 1.0 / SUM(ordered_quantity) END AS fill_rate,
    SUM(actual_spend) AS actual_spend
FROM fact_purchase_orders
GROUP BY region;

DROP VIEW IF EXISTS vw_pbi_category_performance;
CREATE VIEW vw_pbi_category_performance AS
SELECT
    category,
    COUNT(DISTINCT supplier_id) AS suppliers,
    AVG(otif_flag) AS otif_pct,
    CASE WHEN SUM(received_quantity) = 0 THEN 0 ELSE SUM(defective_quantity) * 1.0 / SUM(received_quantity) END AS defect_rate,
    SUM(actual_spend) AS actual_spend
FROM fact_purchase_orders
GROUP BY category;

DROP VIEW IF EXISTS vw_pbi_worst_suppliers;
CREATE VIEW vw_pbi_worst_suppliers AS
SELECT *
FROM supplier_scorecard
ORDER BY weighted_score ASC
LIMIT 10;

DROP VIEW IF EXISTS vw_pbi_spend_by_supplier;
CREATE VIEW vw_pbi_spend_by_supplier AS
SELECT
    supplier_id,
    supplier_name,
    SUM(actual_spend) AS actual_spend,
    SUM(actual_spend) * 1.0 / (SELECT SUM(actual_spend) FROM fact_purchase_orders) AS spend_share
FROM fact_purchase_orders
GROUP BY supplier_id, supplier_name;
