"use client";

import { useDashboard } from "@/components/dashboard-context";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { defaultSettings } from "@/lib/scoring";

export function SettingsForm() {
  const { settings, setSettings, resetSettings } = useDashboard();
  const total = settings.qualityWeight + settings.deliveryWeight + settings.costWeight;

  const setWeight = (key: "qualityWeight" | "deliveryWeight" | "costWeight", value: number) => {
    setSettings({ [key]: value });
  };

  return (
    <div className="space-y-6 text-sm">
      <div>
        <p className="mb-1 font-bold">Scorecard weights</p>
        <p className="mb-3 text-[#555]">Quality 40 / Delivery 40 / Cost 20 is the default. Current total {total}.</p>
        {(
          [
            ["qualityWeight", "Quality"],
            ["deliveryWeight", "Delivery (OTIF)"],
            ["costWeight", "Cost"],
          ] as const
        ).map(([key, label]) => (
          <div key={key} className="mb-4">
            <div className="mb-1 flex justify-between">
              <Label>{label}</Label>
              <span className="tabular">{settings[key]}%</span>
            </div>
            <Slider value={[settings[key]]} min={0} max={80} onValueChange={(v) => setWeight(key, Array.isArray(v) ? v[0] : v)} />
          </div>
        ))}
      </div>

      <div>
        <p className="mb-1 font-bold">OTIF alert</p>
        <div className="mb-1 flex justify-between">
          <Label>Alert when OTIF is below</Label>
          <span className="tabular">{settings.otifAlert}%</span>
        </div>
        <Slider value={[settings.otifAlert]} min={70} max={98} onValueChange={(v) => setSettings({ otifAlert: Array.isArray(v) ? v[0] : v })} />
      </div>

      <div className="space-y-3">
        <p className="font-bold">Display</p>
        <label className="flex items-center justify-between gap-3">
          <span>Compact tables</span>
          <Switch checked={settings.compact} onCheckedChange={(checked) => setSettings({ compact: Boolean(checked) })} />
        </label>
        <label className="flex items-center justify-between gap-3">
          <span>Show dataset note</span>
          <Switch checked={settings.showBanner} onCheckedChange={(checked) => setSettings({ showBanner: Boolean(checked) })} />
        </label>
        <label className="flex items-center justify-between gap-3">
          <span>Dark background</span>
          <Switch checked={settings.inkTheme} onCheckedChange={(checked) => setSettings({ inkTheme: Boolean(checked) })} />
        </label>
      </div>

      <Button variant="outline" onClick={resetSettings}>
        Restore defaults ({defaultSettings.qualityWeight}/{defaultSettings.deliveryWeight}/{defaultSettings.costWeight})
      </Button>
    </div>
  );
}
