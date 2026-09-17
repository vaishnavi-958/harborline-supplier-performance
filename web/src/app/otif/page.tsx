"use client";

import { KpiStat, Panel } from "@/components/kpi-stat";
import { SpendBars, TrendChart } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import { SupplierTable } from "@/components/supplier-table";
import { pct } from "@/lib/format";

export default function OtifPage() {
  const { data, suppliers } = useDashboard();
  if (!data) return null;
  const late = [...suppliers].sort((a, b) => a.otif_pct - b.otif_pct).slice(0, 10);
  return (
    <div className="space-y-5">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <KpiStat label="Network OTIF" value={pct(data.kpis.otif_pct)} />
        <KpiStat label="Fill rate" value={pct(data.kpis.fill_rate)} />
        <KpiStat label="SLA compliance" value={pct(data.kpis.sla_compliance)} />
        <KpiStat label="Lead-time variance" value={`${data.kpis.avg_lead_time_variance.toFixed(1)} d`} />
      </div>
      <Panel title="OTIF definition">
        <p className="max-w-3xl leading-relaxed text-muted-foreground">{data.otif_definition.rule}. Delivery tolerance is {data.otif_definition.delivery_tolerance_days} day(s).</p>
      </Panel>
      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="OTIF vs SLA by month">
          <TrendChart data={data.monthly} x="year_month" y="otif_pct" y2="sla_compliance" />
        </Panel>
        <Panel title="Delay distribution (days late)">
          <SpendBars data={data.delay_histogram.map((d) => ({ name: String(d.bucket), lines: d.lines }))} x="name" y="lines" />
        </Panel>
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="OTIF by region">
          <SpendBars data={data.by_region.map((r) => ({ name: String(r.region), otif: Number(r.otif_pct) }))} x="name" y="otif" />
        </Panel>
        <Panel title="OTIF by category">
          <SpendBars data={data.by_category.map((r) => ({ name: String(r.category), otif: Number(r.otif_pct) }))} x="name" y="otif" />
        </Panel>
      </div>
      <Panel title="Lowest OTIF suppliers">
        <SupplierTable rows={late} />
      </Panel>
    </div>
  );
}
