"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Line,
  LineChart,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const tooltipStyle = {
  background: "#ffffff",
  border: "1px solid #c8c8c8",
  fontSize: 12,
};

function ChartFrame({
  height,
  children,
}: {
  height: number;
  children: (width: number) => ReactNode;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(640);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const update = () => setWidth(Math.max(el.clientWidth, 320));
    update();
    const observer = new ResizeObserver(update);
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return (
    <div ref={ref} className="w-full overflow-hidden" style={{ height }}>
      {children(width)}
    </div>
  );
}

export function TrendChart({ data, x, y, y2 }: { data: object[]; x: string; y: string; y2?: string }) {
  return (
    <ChartFrame height={240}>
      {(width) => (
        <LineChart width={width} height={240} data={data} margin={{ left: 8, right: 16, top: 8, bottom: 0 }}>
          <CartesianGrid stroke="#e6e6e6" vertical={false} />
          <XAxis dataKey={x} tick={{ fontSize: 11, fill: "#555555" }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 11, fill: "#555555" }} axisLine={false} tickLine={false} tickFormatter={(v) => `${Math.round(Number(v) * 100)}%`} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v) => `${(Number(v) * 100).toFixed(1)}%`} />
          <Line type="monotone" dataKey={y} stroke="#1f4e79" strokeWidth={2} dot={false} isAnimationActive={false} />
          {y2 ? <Line type="monotone" dataKey={y2} stroke="#c00000" strokeWidth={2} dot={false} isAnimationActive={false} /> : null}
        </LineChart>
      )}
    </ChartFrame>
  );
}

export function SpendBars({ data, x, y }: { data: object[]; x: string; y: string }) {
  return (
    <ChartFrame height={260}>
      {(width) => (
        <BarChart width={width} height={260} data={data} margin={{ left: 8, right: 8, top: 8, bottom: 24 }}>
          <CartesianGrid stroke="#e6e6e6" vertical={false} />
          <XAxis dataKey={x} tick={{ fontSize: 11, fill: "#555555" }} axisLine={false} tickLine={false} interval={0} angle={-25} textAnchor="end" height={70} />
          <YAxis tick={{ fontSize: 11, fill: "#555555" }} axisLine={false} tickLine={false} />
          <Tooltip contentStyle={tooltipStyle} />
          <Bar dataKey={y} fill="#1f4e79" radius={0} isAnimationActive={false} />
        </BarChart>
      )}
    </ChartFrame>
  );
}

export function ParetoChart({ data }: { data: { supplier_name: string; problem_count: number; cumulative_pct: number }[] }) {
  const top = data.slice(0, 12);
  return (
    <ChartFrame height={300}>
      {(width) => (
        <ComposedChart width={width} height={300} data={top} margin={{ left: 8, right: 16, top: 8, bottom: 48 }}>
          <CartesianGrid stroke="#e6e6e6" vertical={false} />
          <XAxis dataKey="supplier_name" tick={{ fontSize: 10, fill: "#555555" }} interval={0} angle={-28} textAnchor="end" />
          <YAxis yAxisId="left" tick={{ fontSize: 11, fill: "#555555" }} axisLine={false} tickLine={false} />
          <YAxis yAxisId="right" orientation="right" tickFormatter={(v) => `${Math.round(Number(v) * 100)}%`} tick={{ fontSize: 11, fill: "#555555" }} axisLine={false} tickLine={false} />
          <Tooltip contentStyle={tooltipStyle} />
          <Bar yAxisId="left" dataKey="problem_count" fill="#1f4e79" isAnimationActive={false} />
          <Line yAxisId="right" type="monotone" dataKey="cumulative_pct" stroke="#c00000" strokeWidth={2} dot={false} isAnimationActive={false} />
        </ComposedChart>
      )}
    </ChartFrame>
  );
}

export function RiskScatter({
  data,
}: {
  data: { otif_pct: number; defect_rate: number; risk_band: string; supplier_name: string; total_spend: number }[];
}) {
  const color = (band: string) => {
    if (band === "CRITICAL") return "#c00000";
    if (band === "HIGH") return "#bf8f00";
    if (band === "MEDIUM") return "#1f4e79";
    return "#548235";
  };
  return (
    <ChartFrame height={280}>
      {(width) => (
        <ScatterChart width={width} height={280} margin={{ left: 8, right: 8, top: 8, bottom: 8 }}>
          <CartesianGrid stroke="#e6e6e6" />
          <XAxis type="number" dataKey="otif_pct" name="OTIF" tickFormatter={(v) => `${Math.round(Number(v) * 100)}%`} tick={{ fontSize: 11, fill: "#555555" }} />
          <YAxis type="number" dataKey="defect_rate" name="Defect" tickFormatter={(v) => `${(Number(v) * 100).toFixed(1)}%`} tick={{ fontSize: 11, fill: "#555555" }} />
          <Tooltip contentStyle={tooltipStyle} cursor={{ strokeDasharray: "3 3" }} />
          <Scatter data={data} fill="#1a2f4a" isAnimationActive={false}>
            {data.map((entry) => (
              <Cell key={entry.supplier_name} fill={color(entry.risk_band)} />
            ))}
          </Scatter>
        </ScatterChart>
      )}
    </ChartFrame>
  );
}
