# Scoring methodology

This is an **analytical supplier scorecard and risk model**, not a real procurement policy. Scores are derived from KPIs.

## Component scores

- **Delivery** = `40 + 60 * OTIF%` (0–100).
- **Quality** = min-max of defect rate (lower is better), capped at `defect_rate_cap`.
- **Cost** = min-max of cost variance % (lower is better), capped at `cost_variance_pct_cap`.

Weighted score = 0.40 Quality + 0.40 Delivery + 0.20 Cost (configurable).

## Performance tiers

| Tier | Min score | Label |
| --- | --- | --- |
| A | 85 | Excellent |
| B | 70 | Good |
| C | 55 | Watch |
| D | 0 | Corrective Action |

## Risk index (0–100)

`100 * (OTIF gap * 0.25 + defect * 0.20 + SLA breach * 0.20 + lead-time variance * 0.15 + unfavorable cost * 0.10 + spend exposure * 0.10)` after each input is capped/normalized.

Bands: LOW ≤ 25, MEDIUM ≤ 45, HIGH ≤ 70, else CRITICAL.

## Recommended action

MONITOR, SUPPLIER REVIEW, CORRECTIVE ACTION, EXPEDITED FOLLOW-UP, NEGOTIATE, QUALIFY ALTERNATE SUPPLIER — driven by tier, OTIF vs alert threshold, and cost variance. See `config/scoring_config.yaml`.
