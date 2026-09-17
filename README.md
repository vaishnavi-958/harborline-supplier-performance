# Harborline · Supplier Performance & Procurement Analytics Platform

**OTIF, SLA, Quality, Lead-Time & Cost Variance Analytics with Power BI and Power Automate**

Independent Procurement Analytics Project using a synthetic procurement dataset.

This is **Project 2** in a two-project supply-chain portfolio:

| Project | Flow |
| --- | --- |
| 1 · Demand Forecasting & Inventory Optimization | Demand → Forecast → Inventory → Replenishment |
| **2 · Harborline Supplier Performance** | **Supplier → Purchase Order → Delivery → Quality → Cost → Procurement Action** |

It is designed for a Supply Chain Analyst, Procurement Analyst, Supplier Performance Analyst, Purchasing Analyst, or Supply Chain BI Analyst. It is **not** an employer case study. Supplier names, plants, carriers, and standard prices are fabricated. Do not treat them as real companies or actual procurement costs.

## What you can run

The Python pipeline builds a 36-supplier, two-year purchase-order history (~22,000 lines), validates it, scores suppliers, writes SQL views into SQLite, and feeds a Harborline procurement desk (Next.js). The same star schema is documented for Power BI and a Power Automate OTIF alert.

```
PO data → data quality → SQL / Python KPIs → weighted scorecard
        → Harborline desk / Power BI → OTIF alert → RCA → action
```

## Quick start

```bash
python3 -m pip install -r requirements.txt
PYTHONPATH=. python3 scripts/run_pipeline.py
cd web && npm install && npm run dev -- --port 43147 --hostname 127.0.0.1
```

Open [http://127.0.0.1:43147](http://127.0.0.1:43147).

```bash
PYTHONPATH=. python3 -m pytest -q
```

## OTIF definition (default)

OTIF = 1 when **actual delivery date ≤ promised delivery date** *and* **received quantity ≥ ordered quantity**. Otherwise 0. Delivery tolerance (days) and quantity tolerance live in `config/config.yaml`.

## Scorecard (default)

Quality 40% · Delivery (OTIF) 40% · Cost 20%. Weights are configurable in `config/scoring_config.yaml` and in the desk **Settings** page. Scores are computed from KPIs — they are never assigned at random.

Supplier tiers (Strategic / Preferred / Approved / Transactional) are **analytical segmentation**, not a live procurement policy. Risk bands are an **analytical supplier risk model**.

## Repository

Python analytics live in `src/`. SQL is in `sql/`. The interactive desk is `web/`. Power BI measures, the star schema, and the Power Automate flow are documented under `dashboard/` and `automation/`. Capture Power Automate screenshots from your own tenant — this repo does not fabricate them.

## Stack

Python, pandas, SQL (SQLite locally; scripts are portable to PostgreSQL / SQL Server), Next.js, Power BI (documented model + DAX), Power Automate (documented flow).
