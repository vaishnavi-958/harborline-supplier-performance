"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Boxes } from "lucide-react";
import { useDashboard } from "@/components/dashboard-context";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { cn } from "@/lib/utils";
import { Logo, MenuLines } from "@/components/logo";
import { SettingsForm } from "@/components/settings-form";

const NAV = [
  { href: "/", label: "Executive" },
  { href: "/scorecard", label: "Scorecard" },
  { href: "/otif", label: "OTIF & delivery" },
  { href: "/quality", label: "Quality" },
  { href: "/cost", label: "Cost" },
  { href: "/risk", label: "Risk" },
  { href: "/pareto", label: "Pareto & RCA" },
  { href: "/alerts", label: "OTIF alerts" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { data, loading, error, settings, region, setRegion, query, setQuery } = useDashboard();
  const regions = ["All", ...(data?.by_region.map((row) => String(row.region)) ?? [])];

  return (
    <div className={cn("min-h-screen bg-[#f3f3f3]", settings.compact ? "text-[13px]" : "text-sm")}>
      <header className="sticky top-0 z-40 bg-[#1f4e79] text-white">
        <div className="flex items-center gap-4 px-3 py-2 md:px-4">
          <Logo light />
          <p className="hidden flex-1 text-[13px] text-[#d6e3f0] lg:block">
            OTIF, SLA, quality, lead time and cost
          </p>
          <div className="ml-auto flex items-center gap-2">
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Find a supplier"
              className="h-8 w-[160px] rounded-none border-[#8aa4bf] bg-white text-[#222] sm:w-[220px]"
            />
            <Select value={region} onValueChange={(v) => setRegion(String(v ?? "All"))}>
              <SelectTrigger className="h-8 w-[140px] rounded-none border-[#8aa4bf] bg-white text-[#222]">
                <SelectValue placeholder="Region" />
              </SelectTrigger>
              <SelectContent>
                {regions.map((item) => (
                  <SelectItem key={item} value={item}>
                    {item === "All" ? "All regions" : item}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Sheet>
              <SheetTrigger
                className="inline-flex h-8 w-8 items-center justify-center border border-[#8aa4bf] bg-[#1f4e79] text-white hover:bg-[#163a5c]"
                aria-label="Open settings"
              >
                <MenuLines />
              </SheetTrigger>
              <SheetContent side="right" className="w-full max-w-md rounded-none bg-white p-0">
                <SheetHeader className="border-b border-[#c8c8c8]">
                  <SheetTitle className="text-[16px] font-bold text-[#1f4e79]">Settings</SheetTitle>
                </SheetHeader>
                <div className="overflow-y-auto p-4">
                  <SettingsForm />
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
        {settings.showBanner && (
          <div className="border-t border-[#163a5c] bg-[#163a5c] px-4 py-1.5 text-[12px] text-[#d6e3f0]">
            Independent Procurement Analytics Project using a synthetic procurement dataset. Standard prices and supplier names are simulated.
          </div>
        )}
      </header>

      <div className="flex min-h-[calc(100vh-48px)]">
        <aside className="hidden w-[200px] shrink-0 border-r border-[#c8c8c8] bg-white md:block">
          <nav className="py-2">
            {NAV.map((item) => {
              const active = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "block border-l-4 px-3 py-2 text-[13px]",
                    active
                      ? "border-[#1f4e79] bg-[#deebf7] font-semibold text-[#1f4e79]"
                      : "border-transparent text-[#222] hover:bg-[#f3f3f3]"
                  )}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <p className="border-t border-[#c8c8c8] px-3 py-3 text-[11px] leading-snug text-[#666]">
            Independent project. Synthetic purchase-order history — not an employer dataset.
          </p>
        </aside>

        <div className="min-w-0 flex-1">
          <div className="flex gap-1 overflow-x-auto border-b border-[#c8c8c8] bg-white px-2 py-1 md:hidden">
            {NAV.map((item) => (
              <Link key={item.href} href={item.href} className="shrink-0 px-2 py-1 text-[12px] text-[#1f4e79]">
                {item.label}
              </Link>
            ))}
          </div>
          <main className="p-4 lg:p-5">
            {loading && <p className="text-[#555]">Loading procurement extract…</p>}
            {error && (
              <div className="max-w-xl border border-[#c00000] bg-white p-4">
                <Boxes className="mb-2 size-4 text-[#c00000]" />
                <p className="font-semibold">The dashboard extract is not available yet.</p>
                <p className="mt-2 text-[#555]">{error}</p>
              </div>
            )}
            {!loading && !error && children}
          </main>
        </div>
      </div>
    </div>
  );
}
