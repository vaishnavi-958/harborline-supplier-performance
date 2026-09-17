# Business requirements

**Project:** Harborline Supplier Performance & Procurement Analytics Platform  
**Label:** Independent Procurement Analytics Project using a synthetic procurement dataset.

## Problem

Procurement managers lack a single view of supplier OTIF, delays, lead-time variance, fill rate, defects, PO turnaround, cost variance, and SLA compliance. Reviews happen in spreadsheets after the month closes.

## Outcomes

1. Identify strong vs repeatedly late, quality-impaired, or high-variance suppliers.
2. Flag SLA breaches and operational risk, weighted by spend exposure.
3. Push OTIF alerts to the buyer desk without waiting for a monthly pack.
4. Seed root-cause analysis and a dated corrective-action list.

## Users

Supply Chain Analyst, Procurement Analyst, Supplier Performance Analyst, Purchasing Analyst, Supply Chain BI Analyst.

## In scope

Synthetic PO history, data-quality report, star schema, SQL + Python KPIs, weighted scorecard, Harborline desk, Power BI documentation, Power Automate OTIF alert design, RCA pack.

## Out of scope

Live SAP connectivity, real supplier master data, legally binding scorecards, production Power Automate tenant deployment.

## Success measures on the synthetic set

- OTIF decomposable into late-only, short-only, and late-and-short.
- Scorecard rank matches generated supplier behavior (excellent names outrank chronic late names).
- Alert list uses the same OTIF definition as the scorecard.
