import type { Metadata } from "next";
import "./globals.css";
import { AppProviders } from "@/components/app-providers";
import dashboardJson from "../../public/data/dashboard.json";
import type { DashboardData } from "@/lib/types";

export const metadata: Metadata = {
  title: "Harborline · Supplier Performance",
  description:
    "Independent Procurement Analytics Project using a synthetic procurement dataset. OTIF, SLA, quality, lead-time and cost variance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AppProviders initialData={dashboardJson as unknown as DashboardData}>{children}</AppProviders>
      </body>
    </html>
  );
}
