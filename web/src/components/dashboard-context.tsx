"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { AppSettings, DashboardData, Supplier } from "@/lib/types";
import { actionFor, applyWeights, defaultSettings } from "@/lib/scoring";

type DashboardContextValue = {
  data: DashboardData | null;
  error: string | null;
  loading: boolean;
  settings: AppSettings;
  setSettings: (next: Partial<AppSettings>) => void;
  resetSettings: () => void;
  suppliers: Supplier[];
  region: string;
  setRegion: (value: string) => void;
  query: string;
  setQuery: (value: string) => void;
};

const DashboardContext = createContext<DashboardContextValue | null>(null);
const STORAGE_KEY = "harborline-settings";

export function DashboardProvider({
  children,
  initialData,
}: {
  children: React.ReactNode;
  initialData: DashboardData;
}) {
  const [data, setData] = useState<DashboardData | null>(initialData);
  const [error, setError] = useState<string | null>(null);
  const [loading] = useState(false);
  const [settings, setSettingsState] = useState<AppSettings>(defaultSettings);
  const [region, setRegion] = useState("All");
  const [query, setQuery] = useState("");

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setSettingsState({ ...defaultSettings, ...JSON.parse(stored) });
      } catch {
        /* keep defaults */
      }
    }
    fetch("/data/dashboard.json")
      .then(async (res) => {
        if (!res.ok) return initialData;
        return res.json();
      })
      .then((json) => setData(json))
      .catch(() => {
        if (!initialData) setError("Dashboard extract missing. Run `make pipeline`.");
      });
  }, [initialData]);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", settings.inkTheme);
  }, [settings.inkTheme]);

  const setSettings = (next: Partial<AppSettings>) => {
    setSettingsState((prev) => {
      const merged = { ...prev, ...next };
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
      return merged;
    });
  };

  const resetSettings = () => {
    window.localStorage.removeItem(STORAGE_KEY);
    setSettingsState(defaultSettings);
  };

  const suppliers = useMemo(() => {
    if (!data) return [];
    let rows = applyWeights(data.suppliers, settings).map((row) => ({
      ...row,
      recommended_action: actionFor(row, settings.otifAlert),
    }));
    if (region !== "All") rows = rows.filter((row) => row.supplier_region === region);
    if (query.trim()) {
      const q = query.toLowerCase();
      rows = rows.filter(
        (row) =>
          row.supplier_name.toLowerCase().includes(q) ||
          row.supplier_id.toLowerCase().includes(q) ||
          row.supplier_category.toLowerCase().includes(q)
      );
    }
    return rows;
  }, [data, settings, region, query]);

  return (
    <DashboardContext.Provider
      value={{
        data,
        error,
        loading,
        settings,
        setSettings,
        resetSettings,
        suppliers,
        region,
        setRegion,
        query,
        setQuery,
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  const ctx = useContext(DashboardContext);
  if (!ctx) throw new Error("useDashboard must be used within DashboardProvider");
  return ctx;
}
