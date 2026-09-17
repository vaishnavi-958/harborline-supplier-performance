# Power BI dashboard design

Rebuild these pages on the star schema. The Harborline web desk is the interactive twin for portfolio review; Power BI is the documented enterprise surface.

Independent Procurement Analytics Project using a synthetic procurement dataset.

## Page 1 — Procurement executive overview

KPI cards: suppliers, POs, spend, OTIF %, fill rate %, defect rate %, SLA compliance %, cost variance, high-risk suppliers.

Visuals: monthly OTIF, score distribution, top risk, spend by supplier, problem-category breakdown.

## Page 2 — Supplier scorecard

Table with tier, OTIF, fill, defect, lead-time variance, cost variance, quality/delivery/cost scores, weighted score, rank, risk. Sortable.

## Page 3 — OTIF & delivery

OTIF by month / supplier / category / region, late trend, delay histogram, SLA breach rate. Drill: Region → Supplier → Category → Material.

## Page 4 — Quality

Defect trend, by supplier, by category, top materials, quality ranking.

## Page 5 — Cost & procurement

Spend, variance, variance %, by supplier and category, monthly cost, unfavorable variance.

## Page 6 — Supplier risk

Risk matrix, critical/high lists, SLA / OTIF / quality failures, cost exposure.

## Page 7 — Pareto / root cause

Pareto curve, problem type, drill-through to supplier detail.

## Page 8 — Supplier detail

All KPIs, trends, recommended action (MONITOR, SUPPLIER REVIEW, CORRECTIVE ACTION, EXPEDITED FOLLOW-UP, NEGOTIATE, QUALIFY ALTERNATE SUPPLIER).
