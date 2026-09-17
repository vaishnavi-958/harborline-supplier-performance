# Email / Teams template

Do not put sample numbers in the deployed template. Bind every token to the current supplier record.

**Subject**

`Supplier Performance Alert — OTIF Below Threshold`

**Body**

```
Supplier: @{items('Apply_to_each')?['supplier_name']}
Current OTIF: @{formatNumber(mul(items('Apply_to_each')?['otif_pct'], 100), 'N1')}%
Threshold: @{parameters('OtifThreshold')}
Orders evaluated: @{items('Apply_to_each')?['po_lines']}
Late orders (late-only share): @{formatNumber(mul(items('Apply_to_each')?['late_only_pct'], 100), 'N1')}%
Fill rate: @{formatNumber(mul(items('Apply_to_each')?['fill_rate'], 100), 'N1')}%
Defect rate: @{formatNumber(mul(items('Apply_to_each')?['defect_rate'], 100), 'N2')}%
Lead-time variance: @{formatNumber(items('Apply_to_each')?['avg_lead_time_variance'], 'N1')} days
Risk level: @{items('Apply_to_each')?['risk_band']}
Recommended action: @{items('Apply_to_each')?['recommended_action']}

This alert is generated from the Harborline supplier scorecard (synthetic independent project in non-production).
```
