"""Structured 5-Why helper for supplier performance issues."""

from __future__ import annotations

from typing import Any


def build_five_why(supplier: dict[str, Any]) -> list[dict[str, str]]:
    """Build a data-driven 5-Why chain from scorecard KPIs.

    This is a facilitated RCA template seeded by metrics, not an automated
    root-cause verdict.
    """
    name = supplier["supplier_name"]
    otif = supplier["otif_pct"]
    late = supplier.get("late_only_pct", 0)
    short = supplier.get("qty_short_only_pct", 0)
    defect = supplier["defect_rate"]
    sla = supplier["sla_breach_rate"]
    ltv = supplier.get("avg_lead_time_variance", 0)
    archetype = supplier.get("archetype", "")

    problem = (
        f"{name} sits in performance tier {supplier['performance_tier']} with "
        f"OTIF {otif:.1%}, defect rate {defect:.2%}, and SLA breach rate {sla:.1%}."
    )

    if late >= short and ltv > 1:
        why1 = f"OTIF is dragged by late deliveries ({late:.1%} late-only lines), not primarily by quantity shortfalls."
        why2 = f"Actual lead time exceeds promise by {ltv:.1f} days on average, pushing many lines past the {int(supplier.get('sla_days', 0))}-day SLA."
        if archetype == "seasonal":
            why3 = "Delay concentrates in the supplier's peak months, which is consistent with seasonal capacity strain rather than a year-round process failure."
            why4 = "Peak-season capacity and carrier allocation were not locked against the buying plant's Q4 demand pulse."
            why5 = "The replenishment calendar and supplier capacity plan are not jointly constrained during the seasonal window."
        elif archetype == "late_delivery":
            why3 = "Promise dates appear optimistic relative to demonstrated cycle time — the supplier is committing inside a lead time it does not hold."
            why4 = "There is no gated ATP / capacity check before a promise date is sent back on the PO."
            why5 = "Promise-date discipline and production-slot reservation are not part of the operational SLA review."
        else:
            why3 = "Lead-time variance is wide enough that mean performance still produces frequent SLA misses."
            why4 = "The buying plant has no buffer policy tied to this supplier's demonstrated P90 lead time."
            why5 = "Planning still uses promised lead time instead of statistically observed lead time."
    elif short > late:
        why1 = f"OTIF failures are quantity-driven ({short:.1%} on-time-but-short), pointing to fill-rate / capacity rather than transit time."
        why2 = "Received quantity is systematically below ordered quantity, which is consistent with a capacity-factor constraint in the supplier profile."
        why3 = "Split shipments and partials are being received without a formal allocation rule for this account."
        why4 = "The PO quantity is not being confirmed against available-to-promise before release."
        why5 = "Capacity collaboration (forecast share + freeze fence) is missing for this supplier."
    else:
        why1 = "OTIF is failing from a mix of lateness and short fills, so a single-cause story would be incomplete."
        why2 = "Both cycle-time control and quantity confirmation are drifting at the same time."
        why3 = "The supplier's planning signal from the plant is either late, unstable, or not frozen."
        why4 = "S&OP / IBP handoff into procurement is not translating into a reliable supplier schedule."
        why5 = "There is no joint recovery plan with dated actions, owners, and a re-promise calendar."

    if defect > 0.04:
        why1 += f" Quality is a second independent failure mode (defect rate {defect:.2%})."

    return [
        {"level": "Problem", "statement": problem},
        {"level": "Why 1", "statement": why1},
        {"level": "Why 2", "statement": why2},
        {"level": "Why 3", "statement": why3},
        {"level": "Why 4", "statement": why4},
        {"level": "Why 5", "statement": why5},
    ]
