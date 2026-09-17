"use client";

import Link from "next/link";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { Supplier } from "@/lib/types";
import { days, num, pct, score, usd } from "@/lib/format";
import { cn } from "@/lib/utils";

export function SupplierTable({
  rows,
  extra,
}: {
  rows: Supplier[];
  extra?: "risk" | "cost" | "quality";
}) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-10">#</TableHead>
          <TableHead>Supplier</TableHead>
          <TableHead>Tier</TableHead>
          <TableHead className="text-right">OTIF</TableHead>
          <TableHead className="text-right">Fill</TableHead>
          <TableHead className="text-right">Defect</TableHead>
          {extra === "cost" ? <TableHead className="text-right">Cost var.</TableHead> : null}
          {extra !== "cost" ? <TableHead className="text-right">LT var.</TableHead> : null}
          <TableHead className="text-right">Score</TableHead>
          <TableHead>Risk</TableHead>
          <TableHead>Action</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((row) => (
          <TableRow key={row.supplier_id}>
            <TableCell className="tabular text-[#555]">{row.supplier_rank}</TableCell>
            <TableCell>
              <Link href={`/suppliers/${row.supplier_id}`} className="text-[#0563c1] underline">
                {row.supplier_name}
              </Link>
              <div className="text-[11px] text-[#666]">
                {row.supplier_id} · {row.supplier_region} · {row.supplier_tier}
              </div>
            </TableCell>
            <TableCell>
              <span className={cn("px-1 text-[11px]", row.performance_tier === "A" ? "bg-[#e2efda] text-[#548235]" : row.performance_tier === "D" ? "bg-[#fce4d6] text-[#c00000]" : "bg-[#deebf7] text-[#1f4e79]")}>
                {row.performance_tier}
              </span>
            </TableCell>
            <TableCell className="text-right tabular">{pct(row.otif_pct)}</TableCell>
            <TableCell className="text-right tabular">{pct(row.fill_rate)}</TableCell>
            <TableCell className="text-right tabular">{pct(row.defect_rate, 2)}</TableCell>
            {extra === "cost" ? (
              <TableCell className="text-right tabular">{pct(row.cost_variance_pct, 2)}</TableCell>
            ) : (
              <TableCell className="text-right tabular">{days(row.avg_lead_time_variance)}</TableCell>
            )}
            <TableCell className="text-right tabular">{score(row.weighted_score)}</TableCell>
            <TableCell className="text-[12px]">{row.risk_band}</TableCell>
            <TableCell className="text-[11px] text-[#555]">{row.recommended_action}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

export function EmptyNote({ text }: { text: string }) {
  return <p className="py-8 text-center text-muted-foreground">{text}</p>;
}

export { num, usd };
