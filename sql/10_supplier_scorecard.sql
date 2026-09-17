DROP VIEW IF EXISTS vw_supplier_scorecard;
CREATE VIEW vw_supplier_scorecard AS
SELECT
    s.*,
    RANK() OVER (ORDER BY s.weighted_score DESC) AS sql_rank
FROM supplier_scorecard s;
