import type { AppSettings, Supplier } from "@/lib/types";

export const defaultSettings: AppSettings = {
  qualityWeight: 40,
  deliveryWeight: 40,
  costWeight: 20,
  otifAlert: 90,
  compact: false,
  showBanner: true,
  inkTheme: false,
};

export function applyWeights(suppliers: Supplier[], settings: AppSettings): Supplier[] {
  const q = settings.qualityWeight / 100;
  const d = settings.deliveryWeight / 100;
  const c = settings.costWeight / 100;
  const scored = suppliers.map((row) => {
    const weighted_score = row.quality_score * q + row.delivery_score * d + row.cost_score * c;
    let performance_tier: string = "D";
    if (weighted_score >= 85) performance_tier = "A";
    else if (weighted_score >= 70) performance_tier = "B";
    else if (weighted_score >= 55) performance_tier = "C";
    return { ...row, weighted_score, performance_tier };
  });
  const ranked = [...scored].sort((a, b) => b.weighted_score - a.weighted_score);
  return ranked.map((row, index) => ({ ...row, supplier_rank: index + 1 }));
}

export function actionFor(row: Supplier, otifAlert: number): string {
  if (row.otif_pct < otifAlert / 100) {
    if (row.performance_tier === "D") return "QUALIFY ALTERNATE SUPPLIER";
    return "EXPEDITED FOLLOW-UP";
  }
  if (row.cost_variance_pct > 0.05 && ["B", "C", "D"].includes(row.performance_tier)) {
    return "NEGOTIATE";
  }
  if (row.performance_tier === "A") return "MONITOR";
  if (row.performance_tier === "B") return "SUPPLIER REVIEW";
  if (row.performance_tier === "C") return "CORRECTIVE ACTION";
  return "QUALIFY ALTERNATE SUPPLIER";
}
