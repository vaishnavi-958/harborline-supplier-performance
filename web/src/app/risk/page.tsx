"use client";

import { KpiStat, Panel } from "@/components/kpi-stat";
import { RiskScatter } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import { SupplierTable } from "@/components/supplier-table";
import { num } from "@/lib/format";

export default function RiskPage() {
  const { data, suppliers } = useDashboard();
  if (!data) return null;
  const critical = suppliers.filter((s) => s.risk_band === "CRITICAL" || s.risk_band === "HIGH");
  return (
    <div className="space-y-5">
      <div className="grid gap-3 sm:grid-cols-4">
        <KpiStat label="Low" value={num(suppliers.filter((s) => s.risk_band === "LOW").length)} tone="sea" />
        <KpiStat label="Medium" value={num(suppliers.filter((s) => s.risk_band === "MEDIUM").length)} />
        <KpiStat label="High" value={num(suppliers.filter((s) => s.risk_band === "HIGH").length)} tone="copper" />
        <KpiStat label="Critical" value={num(suppliers.filter((s) => s.risk_band === "CRITICAL").length)} tone="rust" />
      </div>
      <Panel title="Analytical risk matrix · OTIF vs defect rate">
        <RiskScatter data={suppliers} />
        <p className="mt-3 text-[12px] text-muted-foreground">Analytical supplier risk model — not a real-world procurement policy. Size of operational exposure is in the scorecard spend column.</p>
      </Panel>
      <Panel title="High and critical suppliers">
        <SupplierTable rows={critical} />
      </Panel>
    </div>
  );
}
