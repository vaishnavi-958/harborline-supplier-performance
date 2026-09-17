export type Supplier = {
  supplier_id: string;
  supplier_name: string;
  supplier_region: string;
  supplier_category: string;
  supplier_tier: string;
  archetype: string;
  sla_days: number;
  payment_terms: string;
  otif_pct: number;
  late_only_pct: number;
  qty_short_only_pct: number;
  late_and_short_pct: number;
  fill_rate: number;
  defect_rate: number;
  quality_failure_rate: number;
  actual_spend: number;
  expected_spend: number;
  cost_variance: number;
  cost_variance_pct: number;
  avg_lead_time: number;
  median_lead_time: number;
  stdev_lead_time: number;
  p90_lead_time: number;
  avg_lead_time_variance: number;
  sla_breach_rate: number;
  sla_status: string;
  total_spend: number;
  total_pos: number;
  po_lines: number;
  avg_turnaround: number;
  quality_score: number;
  delivery_score: number;
  cost_score: number;
  weighted_score: number;
  supplier_rank: number;
  performance_tier: "A" | "B" | "C" | "D" | string;
  performance_tier_label: string;
  spend_share: number;
  risk_score: number;
  risk_band: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | string;
  recommended_action: string;
  problem_count: number;
};

export type MonthlyPoint = {
  year_month: string;
  po_lines: number;
  otif_pct: number;
  fill_rate: number;
  defect_rate: number;
  sla_compliance: number;
  actual_spend: number;
  cost_variance: number;
  cost_variance_pct: number;
  avg_lead_time: number;
  avg_lead_time_variance: number;
  late_pct: number;
};

export type GroupKpi = {
  [key: string]: string | number;
  po_lines: number;
  otif_pct: number;
  fill_rate: number;
  defect_rate: number;
  sla_compliance: number;
  actual_spend: number;
  cost_variance: number;
};

export type DashboardData = {
  disclaimer: string;
  generated_at: string;
  project: { name: string; subtitle: string; disclaimer: string };
  otif_definition: {
    rule: string;
    delivery_tolerance_days: number;
    quantity_tolerance_pct: number;
  };
  scoring: {
    weights: { quality: number; delivery: number; cost: number };
    otif_alert_threshold: number;
    performance_tiers: Record<string, { min_score: number; label: string }>;
    recommended_action: Record<string, string>;
  };
  kpis: {
    total_suppliers: number;
    total_pos: number;
    total_lines: number;
    total_spend: number;
    otif_pct: number;
    fill_rate: number;
    defect_rate: number;
    sla_compliance: number;
    cost_variance: number;
    cost_variance_pct: number;
    high_risk_suppliers: number;
    avg_lead_time: number;
    avg_lead_time_variance: number;
    avg_turnaround: number;
  };
  problem_mix: Record<string, number>;
  monthly: MonthlyPoint[];
  suppliers: Supplier[];
  pareto: {
    supplier_id: string;
    supplier_name: string;
    problem_count: number;
    problem_pct: number;
    cumulative_pct: number;
    risk_band: string;
    weighted_score: number;
  }[];
  by_category: Record<string, string | number>[];
  by_region: Record<string, string | number>[];
  by_plant: Record<string, string | number>[];
  materials: Record<string, string | number>[];
  delay_histogram: { bucket: number; lines: number }[];
  supplier_monthly: {
    supplier_id: string;
    supplier_name: string;
    year_month: string;
    otif_pct: number;
    fill_rate: number;
    defect_rate: number;
    sla_breach_rate: number;
    actual_spend: number;
    avg_lead_time: number;
    avg_lead_time_variance: number;
    po_lines: number;
  }[];
  rca: {
    supplier: Supplier;
    five_why: { level: string; statement: string }[];
    fishbone: Record<string, string[]>;
    problem_mix: Record<string, number>;
    monthly: Record<string, string | number>[];
    corrective_actions: { action: string; owner: string; due: string }[];
  };
  quality_report: {
    check_id: string;
    description: string;
    failed_rows: number;
    total_rows: number;
    fail_rate: number;
    status: string;
  }[];
};

export type AppSettings = {
  qualityWeight: number;
  deliveryWeight: number;
  costWeight: number;
  otifAlert: number;
  compact: boolean;
  showBanner: boolean;
  inkTheme: boolean;
};
