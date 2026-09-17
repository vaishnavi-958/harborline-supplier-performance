"use client";

import { Panel } from "@/components/kpi-stat";
import { ParetoChart } from "@/components/charts";
import { useDashboard } from "@/components/dashboard-context";
import Link from "next/link";
import { pct } from "@/lib/format";

export default function ParetoPage() {
  const { data } = useDashboard();
  if (!data) return null;
  const rca = data.rca;
  return (
    <div className="space-y-5">
      <Panel title="Pareto of problem suppliers">
        <ParetoChart data={data.pareto} />
      </Panel>
      <div className="grid gap-4 xl:grid-cols-2">
        <Panel title={`5-Why · ${rca.supplier.supplier_name}`}>
          <p className="mb-3 text-[12px] text-muted-foreground">
            Selected supplier for RCA based on lowest composite scorecard performance.{" "}
            <Link className="text-navy underline" href={`/suppliers/${rca.supplier.supplier_id}`}>
              Open supplier desk
            </Link>
          </p>
          <p className="mb-3 text-[11px] text-muted-foreground">Analytical hypothesis: causes are inferred from supplier KPI patterns and should be validated with supplier, procurement, and operational evidence before corrective action.</p>
          <ol className="space-y-3">
            {rca.five_why.map((step) => (
              <li key={step.level}>
                <p className="text-[12px] font-bold text-[#1f4e79]">{step.level}</p>
                <p className="mt-1 leading-relaxed">{step.statement}</p>
              </li>
            ))}
          </ol>
        </Panel>
        <Panel title="Fishbone · process, not people">
          <div className="grid gap-3 sm:grid-cols-2">
            {Object.entries(rca.fishbone).map(([bone, items]) => (
              <div key={bone}>
                <p className="text-[12px] font-medium text-navy">{bone}</p>
                <ul className="mt-1 list-disc space-y-1 pl-4 text-[12px] text-muted-foreground">
                  {items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </Panel>
      </div>
      <Panel title="Corrective action plan">
        <table className="w-full text-left">
          <thead className="text-[11px] uppercase tracking-wider text-muted-foreground">
            <tr>
              <th className="py-2">Action</th>
              <th>Owner</th>
              <th>Due</th>
            </tr>
          </thead>
          <tbody>
            {rca.corrective_actions.map((row) => (
              <tr key={row.action} className="border-t border-border">
                <td className="py-2 pr-4">{row.action}</td>
                <td className="pr-4">{row.owner}</td>
                <td>{row.due}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="mt-4 text-[12px] text-muted-foreground">
          Top problem share: {data.pareto.slice(0, 10).reduce((s, r) => s + r.problem_pct, 0) ? pct(data.pareto.slice(0, 10).reduce((s, r) => s + r.problem_pct, 0)) : "—"}.
        </p>
      </Panel>
    </div>
  );
}


