export function pct(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return `${(value * 100).toFixed(digits)}%`;
}

export function num(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toLocaleString("en-US", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

export function usd(value: number | null | undefined, compact = false) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    notation: compact ? "compact" : "standard",
    maximumFractionDigits: compact ? 1 : 0,
  });
}

export function days(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)} d`;
}

export function score(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toFixed(1);
}

export function riskTone(band: string) {
  if (band === "CRITICAL") return "text-rust";
  if (band === "HIGH") return "text-copper";
  if (band === "MEDIUM") return "text-navy";
  return "text-sea";
}

export function tierTone(tier: string) {
  if (tier === "A") return "bg-sea/15 text-sea";
  if (tier === "B") return "bg-navy/10 text-navy";
  if (tier === "C") return "bg-copper/15 text-copper";
  return "bg-rust/15 text-rust";
}
