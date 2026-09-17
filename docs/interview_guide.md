# Interview guide

Use this project to talk like a buyer-side analyst, not a dashboard decorator.

## 60-second story

"I built an independent procurement analytics project on a synthetic PO book. The question is not 'pretty OTIF'. It is which suppliers are late versus short versus defective, how that concentrates in a Pareto, and what action the desk should take this week — including a Power Automate alert when OTIF drops below 90%."

## Likely questions

**How do you define OTIF?**  
Line-level, on or before promise *and* received ≥ ordered. I split failures so a quality issue is not hidden inside a late truck.

**Why synthetic data?**  
Public datasets rarely have promise date, GR date, defect quantity, SLA, and standard vs PO price on the same grain.

**How do you stop a scorecard from being politics?**  
Weights in config, scores from KPIs, same definition in SQL, Python, and DAX.

**How does this sit next to inventory work?**  
Forecast and safety stock tell you what to buy. This tells you whether the source you chose is eating that plan.

**What would you do with SAP?**  
Map EKKO/EKPO/EKET/EKBE, keep Harborline as the semantic layer, do not copy vendor PII.

**What would you not claim?**  
That these suppliers are real, that the risk model is a corporate policy, or that this was delivered for an employer.
