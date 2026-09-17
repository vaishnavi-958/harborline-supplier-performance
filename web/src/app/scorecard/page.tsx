"use client";

import { Panel } from "@/components/kpi-stat";
import { useDashboard } from "@/components/dashboard-context";
import { SupplierTable, EmptyNote } from "@/components/supplier-table";

export default function ScorecardPage() {
  const { suppliers } = useDashboard();
  return (
    <Panel title="Weighted supplier scorecard">
      {suppliers.length ? <SupplierTable rows={suppliers} /> : <EmptyNote text="No suppliers match the current filters." />}
      <p className="mt-4 text-[12px] text-muted-foreground">
        Quality, delivery and cost scores are computed from KPIs. Weights can be changed in Settings. Analytical segmentation into Strategic / Preferred / Approved / Transactional is not a live procurement policy.
      </p>
    </Panel>
  );
}
