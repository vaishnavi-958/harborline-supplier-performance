# DAX measures

```dax
Total POs = DISTINCTCOUNT ( fact_purchase_orders[po_id] )

Total Spend = SUM ( fact_purchase_orders[actual_spend] )

Total Ordered Quantity = SUM ( fact_purchase_orders[ordered_quantity] )

Total Received Quantity = SUM ( fact_purchase_orders[received_quantity] )

OTIF % =
DIVIDE (
    SUM ( fact_purchase_orders[otif_flag] ),
    COUNTROWS ( fact_purchase_orders )
)

Fill Rate % =
DIVIDE (
    [Total Received Quantity],
    [Total Ordered Quantity]
)

Defect Rate % =
DIVIDE (
    SUM ( fact_purchase_orders[defective_quantity] ),
    [Total Received Quantity]
)

Average Lead Time = AVERAGE ( fact_purchase_orders[actual_lead_time_days] )

Lead-Time Variance = AVERAGE ( fact_purchase_orders[lead_time_variance_days] )

SLA Breach % = AVERAGE ( fact_purchase_orders[sla_breach_flag] )

SLA Compliance % = 1 - [SLA Breach %]

Cost Variance =
SUM ( fact_purchase_orders[actual_spend] )
    - SUM ( fact_purchase_orders[expected_spend] )

Cost Variance % =
DIVIDE (
    [Cost Variance],
    SUM ( fact_purchase_orders[expected_spend] )
)

Supplier Score = AVERAGE ( supplier_scorecard[weighted_score] )

Supplier Rank = MIN ( supplier_scorecard[supplier_rank] )

High Risk Supplier Count =
CALCULATE (
    DISTINCTCOUNT ( supplier_scorecard[supplier_id] ),
    supplier_scorecard[risk_band] IN { "HIGH", "CRITICAL" }
)

Problem Supplier Count =
CALCULATE (
    DISTINCTCOUNT ( supplier_scorecard[supplier_id] ),
    supplier_scorecard[performance_tier] IN { "C", "D" }
)

Supplier Spend % =
DIVIDE (
    [Total Spend],
    CALCULATE ( [Total Spend], ALL ( dim_supplier ) )
)

Cumulative Problem % =
VAR CurrentProblems = SUM ( supplier_pareto[problem_count] )
VAR AllProblems =
    CALCULATE ( SUM ( supplier_pareto[problem_count] ), ALL ( supplier_pareto ) )
RETURN
    DIVIDE ( CurrentProblems, AllProblems )

Pareto % = MAX ( supplier_pareto[cumulative_pct] )
```
