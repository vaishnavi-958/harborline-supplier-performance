# KPI definitions

Independent Procurement Analytics Project using a synthetic procurement dataset.

## OTIF

Default: `OTIF = 1` iff `actual_delivery_date <= promised_delivery_date + delivery_tolerance_days` **and** `received_quantity >= ordered_quantity * (1 - quantity_tolerance_pct)`.

Failure split:

- Late-only: late and in-full
- Quantity-short-only: on time and short
- Late-and-short: both

Supplier / month / category / region / plant OTIF % = average of `otif_flag`.

## Fill rate

`SUM(received_quantity) / SUM(ordered_quantity)`. Zero denominator returns 0.

## Lead time

- Actual = actual delivery − order date
- Promised = promised delivery − order date
- Variance = actual − promised

Also: average, median, standard deviation, 90th percentile (SQL uses an NTILE approximation in SQLite).

## SLA

SLA days is the maximum allowable actual lead time. Breach flag = actual lead time > SLA days. Status bands (configurable): COMPLIANT / WATCH / BREACH from supplier breach rate.

## Quality

Defect rate = defective quantity / received quantity. Quality failure rate counts REJECTED and DEVIATION lines.

## Cost variance

`unit_price - standard_price`. Standard price is a **simulated analytical input**, not an actual company cost. Spend variance = actual spend − expected spend.

## PO turnaround

`po_approval_date - po_creation_date` (synthetic workflow dates).
