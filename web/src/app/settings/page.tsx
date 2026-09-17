"use client";

import { SettingsForm } from "@/components/settings-form";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-xl border border-[#c8c8c8] bg-white p-4">
      <h2 className="mb-1 text-xl font-bold text-[#1f4e79]">Settings</h2>
      <p className="mb-4 text-[#555]">
        Same options as the three-line menu in the top bar. These change scoring and display only.
      </p>
      <SettingsForm />
    </div>
  );
}
