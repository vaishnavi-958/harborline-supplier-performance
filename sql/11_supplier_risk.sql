DROP VIEW IF EXISTS vw_supplier_risk;
CREATE VIEW vw_supplier_risk AS
SELECT
    supplier_id,
    supplier_name,
    risk_band,
    risk_score,
    otif_pct,
    defect_rate,
    sla_breach_rate,
    avg_lead_time_variance,
    cost_variance_pct,
    total_spend,
    spend_share,
    CASE
        WHEN risk_band IN ('HIGH', 'CRITICAL') THEN 1
        ELSE 0
    END AS high_risk_flag
FROM supplier_scorecard;

DROP VIEW IF EXISTS vw_corrective_action_candidates;
CREATE VIEW vw_corrective_action_candidates AS
SELECT *
FROM supplier_scorecard
WHERE performance_tier IN ('C', 'D')
   OR risk_band IN ('HIGH', 'CRITICAL')
   OR otif_pct < 0.90
ORDER BY risk_score DESC;
