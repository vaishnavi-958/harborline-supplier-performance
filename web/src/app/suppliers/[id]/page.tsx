"use client";

import { useParams } from "next/navigation";
import { KpiStat, Panel } from "@/components/kpi-stat";
import { TrendChart } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import { days, pct, score, usd } from "@/lib/format";
import Link from "next/link";

export default function SupplierDetailPage() {
  const params = useParams<{ id: string }>();
  const { data, suppliers } = useDashboard();
  if (!data) return null;
  const supplier = suppliers.find((s) => s.supplier_id === params.id) ?? data.suppliers.find((s) => s.supplier_id === params.id);
  if (!supplier) {
    return <p className="text-muted-foreground">Supplier not in the current extract.</p>;
  }
  const monthly = data.supplier_monthly.filter((row) => row.supplier_id === supplier.supplier_id);
  return (
    <div className="space-y-5">
      <div>
        <p className="text-[12px] text-[#555]">
          {supplier.supplier_id} · {supplier.supplier_tier} · {supplier.supplier_region}
        </p>
        <h2 className="text-2xl font-bold text-[#1f4e79]">{supplier.supplier_name}</h2>
        <p className="mt-1 text-muted-foreground">
          {supplier.supplier_category} · {supplier.payment_terms} · SLA {supplier.sla_days} days · Rank {supplier.supplier_rank}
        </p>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <KpiStat label="OTIF" value={pct(supplier.otif_pct)} tone={supplier.otif_pct >= 0.9 ? "sea" : "rust"} />
        <KpiStat label="Fill rate" value={pct(supplier.fill_rate)} />
        <KpiStat label="Defect rate" value={pct(supplier.defect_rate, 2)} />
        <KpiStat label="SLA status" value={supplier.sla_status} />
        <KpiStat label="Lead time" value={`${supplier.avg_lead_time.toFixed(1)} d`} />
        <KpiStat label="Lead-time variance" value={days(supplier.avg_lead_time_variance)} />
        <KpiStat label="Cost variance" value={pct(supplier.cost_variance_pct, 2)} hint={usd(supplier.cost_variance, true)} />
        <KpiStat label="Weighted score" value={score(supplier.weighted_score)} hint={`Risk ${supplier.risk_band}`} />
      </div>
      <Panel title="Recommended procurement action">
        <p className="font-[family-name:var(--font-ibm-mono)] text-lg tracking-wide text-navy">{supplier.recommended_action}</p>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Late-only {pct(supplier.late_only_pct)} · quantity-short-only {pct(supplier.qty_short_only_pct)} · late-and-short {pct(supplier.late_and_short_pct)}.
          Quality {score(supplier.quality_score)} · delivery {score(supplier.delivery_score)} · cost {score(supplier.cost_score)}.
        </p>
      </Panel>
      <Panel title="Monthly trend">
        <TrendChart data={monthly} x="year_month" y="otif_pct" y2="fill_rate" />
      </Panel>
      <Link href="/scorecard" className="text-navy underline">
        Back to scorecard
      </Link>
    </div>
  );
}
