"use client";

import { TooltipProvider } from "@/components/ui/tooltip";
import { DashboardProvider } from "@/components/dashboard-context";
import { AppShell } from "@/components/app-shell";
import type { DashboardData } from "@/lib/types";

export function AppProviders({
  children,
  initialData,
}: {
  children: React.ReactNode;
  initialData: DashboardData;
}) {
  return (
    <TooltipProvider>
      <DashboardProvider initialData={initialData}>
        <AppShell>{children}</AppShell>
      </DashboardProvider>
    </TooltipProvider>
  );
}
