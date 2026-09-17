import { cn } from "@/lib/utils";

export function KpiStat({
  label,
  value,
  hint,
  tone = "navy",
}: {
  label: string;
  value: string;
  hint?: string;
  tone?: "navy" | "sea" | "copper" | "rust";
}) {
  const color = {
    navy: "text-[#1f4e79]",
    sea: "text-[#548235]",
    copper: "text-[#bf8f00]",
    rust: "text-[#c00000]",
  }[tone];
  return (
    <div className="border border-[#c8c8c8] bg-white px-3 py-2">
      <p className="text-[12px] text-[#555]">{label}</p>
      <p className={cn("mt-1 text-[22px] font-bold tabular leading-none", color)}>{value}</p>
      {hint ? <p className="mt-1 text-[11px] text-[#666]">{hint}</p> : null}
    </div>
  );
}

export function Panel({
  title,
  children,
  action,
  className,
}: {
  title: string;
  children: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("border border-[#c8c8c8] bg-white", className)}>
      <div className="flex items-center justify-between border-b border-[#c8c8c8] bg-[#f3f3f3] px-3 py-2">
        <h2 className="text-[13px] font-bold text-[#1f4e79]">{title}</h2>
        {action}
      </div>
      <div className="p-3">{children}</div>
    </section>
  );
}
