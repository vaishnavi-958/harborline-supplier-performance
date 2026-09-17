DROP VIEW IF EXISTS vw_lead_time;
CREATE VIEW vw_lead_time AS
SELECT
    supplier_id,
    supplier_name,
    AVG(actual_lead_time_days) AS avg_lead_time,
    AVG(lead_time_days) AS promised_lead_time,
    AVG(actual_lead_time_days - lead_time_days) AS avg_lead_time_variance,
    AVG(delivery_days_late) AS avg_days_late,
    -- SQLite percentile approximation via NTILE
    COUNT(*) AS po_lines
FROM fact_purchase_orders
GROUP BY supplier_id, supplier_name;

DROP VIEW IF EXISTS vw_lead_time_percentile;
CREATE VIEW vw_lead_time_percentile AS
WITH ordered AS (
    SELECT
        supplier_id,
        actual_lead_time_days,
        NTILE(10) OVER (PARTITION BY supplier_id ORDER BY actual_lead_time_days) AS decile
    FROM fact_purchase_orders
)
SELECT
    supplier_id,
    AVG(CASE WHEN decile = 9 THEN actual_lead_time_days END) AS approx_p90_lead_time
FROM ordered
GROUP BY supplier_id;
