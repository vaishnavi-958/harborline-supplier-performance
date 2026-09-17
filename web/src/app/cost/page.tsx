"use client";

import { KpiStat, Panel } from "@/components/kpi-stat";
import { SpendBars, TrendChart } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import { SupplierTable } from "@/components/supplier-table";
import { pct, usd } from "@/lib/format";

export default function CostPage() {
  const { data, suppliers } = useDashboard();
  if (!data) return null;
  const worst = [...suppliers].sort((a, b) => b.cost_variance_pct - a.cost_variance_pct).slice(0, 10);
  return (
    <div className="space-y-5">
      <div className="grid gap-3 sm:grid-cols-3">
        <KpiStat label="Simulated spend" value={usd(data.kpis.total_spend, true)} />
        <KpiStat label="Cost variance" value={usd(data.kpis.cost_variance, true)} tone="copper" />
        <KpiStat label="Cost variance %" value={pct(data.kpis.cost_variance_pct, 2)} />
      </div>
      <p className="text-[12px] text-muted-foreground">Standard prices are simulated analytical inputs, not actual company procurement costs.</p>
      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="Monthly spend">
          <TrendChart data={data.monthly.map((m) => ({ ...m, spend_idx: m.actual_spend / (data.monthly[0]?.actual_spend || 1) }))} x="year_month" y="cost_variance_pct" />
        </Panel>
        <Panel title="Spend by category">
          <SpendBars data={data.by_category.map((r) => ({ name: String(r.category), spend: Number(r.actual_spend) }))} x="name" y="spend" />
        </Panel>
      </div>
      <Panel title="Unfavorable unit-price variance">
        <SupplierTable rows={worst} extra="cost" />
      </Panel>
    </div>
  );
}
