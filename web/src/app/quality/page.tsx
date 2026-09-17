"use client";

import { KpiStat, Panel } from "@/components/kpi-stat";
import { SpendBars, TrendChart } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import { SupplierTable } from "@/components/supplier-table";
import { num, pct } from "@/lib/format";

export default function QualityPage() {
  const { data, suppliers } = useDashboard();
  if (!data) return null;
  const worst = [...suppliers].sort((a, b) => b.defect_rate - a.defect_rate).slice(0, 10);
  const materials = data.materials.slice(0, 8);
  return (
    <div className="space-y-5">
      <div className="grid gap-3 sm:grid-cols-3">
        <KpiStat label="Defect rate" value={pct(data.kpis.defect_rate, 2)} tone="copper" />
        <KpiStat label="Quality rejects" value={num(data.problem_mix.quality_rejected)} />
        <KpiStat label="Persistent quality names" value={num(suppliers.filter((s) => s.defect_rate > 0.04).length)} />
      </div>
      <Panel title="Defect rate trend">
        <TrendChart data={data.monthly} x="year_month" y="defect_rate" />
      </Panel>
      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title="Defects by category">
          <SpendBars data={data.by_category.map((r) => ({ name: String(r.category), defect: Number(r.defect_rate) }))} x="name" y="defect" />
        </Panel>
        <Panel title="Highest-defect materials">
          <ul className="space-y-2">
            {materials.map((m) => (
              <li key={String(m.material_id)} className="flex justify-between gap-4 border-b border-border/70 py-1.5">
                <span>
                  {String(m.material_description)}
                  <span className="block text-[11px] text-muted-foreground">{String(m.category)}</span>
                </span>
                <span className="font-[family-name:var(--font-ibm-mono)] tabular">{pct(Number(m.defect_rate), 2)}</span>
              </li>
            ))}
          </ul>
        </Panel>
      </div>
      <Panel title="Supplier quality ranking">
        <SupplierTable rows={worst} extra="quality" />
      </Panel>
    </div>
  );
}
