"use client";

import { KpiStat, Panel } from "@/components/kpi-stat";
import { SpendBars, TrendChart } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import { SupplierTable } from "@/components/supplier-table";
import { num, pct, usd } from "@/lib/format";

export default function ExecutivePage() {
  const { data, suppliers, settings } = useDashboard();
  if (!data) return null;
  const alerts = suppliers.filter((s) => s.otif_pct < settings.otifAlert / 100);
  const topSpend = [...suppliers].sort((a, b) => b.total_spend - a.total_spend).slice(0, 8);
  const mix = Object.entries(data.problem_mix).map(([name, value]) => ({ name, value }));

  return (
    <div className="space-y-5">
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <KpiStat label="Suppliers" value={num(data.kpis.total_suppliers)} hint={`${num(data.kpis.total_lines)} PO lines`} />
        <KpiStat label="Total spend" value={usd(data.kpis.total_spend, true)} hint="Simulated actual spend" />
        <KpiStat label="OTIF" value={pct(data.kpis.otif_pct)} tone={data.kpis.otif_pct >= 0.9 ? "sea" : "rust"} hint="On time and in full" />
        <KpiStat label="Fill rate" value={pct(data.kpis.fill_rate)} />
        <KpiStat label="Defect rate" value={pct(data.kpis.defect_rate, 2)} tone="copper" />
        <KpiStat label="SLA compliance" value={pct(data.kpis.sla_compliance)} />
        <KpiStat label="Cost variance" value={usd(data.kpis.cost_variance, true)} hint={pct(data.kpis.cost_variance_pct, 2)} />
        <KpiStat label="High-risk suppliers" value={num(data.kpis.high_risk_suppliers)} tone="rust" />
        <KpiStat label="Avg lead time" value={`${data.kpis.avg_lead_time.toFixed(1)} d`} />
        <KpiStat label="PO turnaround" value={`${data.kpis.avg_turnaround.toFixed(1)} d`} hint="Creation to approval" />
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="Monthly OTIF">
          <TrendChart data={data.monthly} x="year_month" y="otif_pct" y2="sla_compliance" />
        </Panel>
        <Panel title="Spend by supplier">
          <SpendBars data={topSpend.map((s) => ({ name: s.supplier_name.replace(/ .*/, ""), spend: Math.round(s.total_spend) }))} x="name" y="spend" />
        </Panel>
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        <Panel title="Problem mix" className="xl:col-span-1">
          <ul className="space-y-2">
            {mix.map((row) => (
              <li key={row.name} className="flex justify-between border-b border-border/70 py-1.5">
                <span className="capitalize text-muted-foreground">{row.name.replaceAll("_", " ")}</span>
                <span className="font-[family-name:var(--font-ibm-mono)] tabular">{num(row.value)}</span>
              </li>
            ))}
          </ul>
        </Panel>
        <Panel title={`OTIF alerts below ${settings.otifAlert}%`} className="xl:col-span-2">
          {alerts.length === 0 ? (
            <p className="text-muted-foreground">No suppliers under the current alert threshold.</p>
          ) : (
            <SupplierTable rows={alerts.slice(0, 8)} />
          )}
        </Panel>
      </div>
    </div>
  );
}
