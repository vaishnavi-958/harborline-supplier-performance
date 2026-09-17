"use client";

import { Panel } from "@/components/kpi-stat";
import { useDashboard } from "@/components/dashboard-context";
import { pct } from "@/lib/format";
import Link from "next/link";

export default function AlertsPage() {
  const { suppliers, settings } = useDashboard();
  const hits = suppliers.filter((s) => s.otif_pct < settings.otifAlert / 100);
  return (
    <div className="space-y-5">
      <div>
        <p className="text-[12px] text-[#555]">Power Automate · Supplier OTIF Alert</p>
        <h2 className="text-2xl font-bold text-[#1f4e79]">Alert draft</h2>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          This page previews the message a scheduled flow would send when OTIF falls below {settings.otifAlert}%. Recipients and connectors are documented in automation/power_automate_flow.md.
        </p>
      </div>
      {hits.length === 0 ? (
        <Panel title="Queue">
          <p>No suppliers currently breach the threshold.</p>
        </Panel>
      ) : (
        hits.map((s) => (
          <Panel key={s.supplier_id} title={`Supplier Performance Alert — OTIF Below Threshold`}>
            <dl className="grid gap-2 sm:grid-cols-2">
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Supplier</dt>
                <dd>
                  <Link className="text-navy underline" href={`/suppliers/${s.supplier_id}`}>
                    {s.supplier_name}
                  </Link>
                </dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Current OTIF</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{pct(s.otif_pct)}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Threshold</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{settings.otifAlert}%</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Orders evaluated</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{s.po_lines}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Late-only share</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{pct(s.late_only_pct)}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Fill rate</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{pct(s.fill_rate)}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Defect rate</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{pct(s.defect_rate, 2)}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Lead-time variance</dt>
                <dd className="font-[family-name:var(--font-ibm-mono)]">{s.avg_lead_time_variance.toFixed(1)} d</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Risk level</dt>
                <dd>{s.risk_band}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">Recommended action</dt>
                <dd>{s.recommended_action}</dd>
              </div>
            </dl>
          </Panel>
        ))
      )}
    </div>
  );
}
