export function Logo({ light = false }: { light?: boolean }) {
  const word = light ? "#ffffff" : "#1f4e79";
  const sub = light ? "#d6e3f0" : "#555555";
  return (
    <div className="flex items-center gap-2">
      <svg width="32" height="32" viewBox="0 0 32 32" aria-hidden="true">
        <rect width="32" height="32" fill="#1f4e79" />
        <rect x="7" y="6" width="5" height="20" fill="#ffffff" />
        <rect x="7" y="13.5" width="13" height="5" fill="#ffffff" />
        <rect x="20" y="6" width="5" height="20" fill="#ffffff" />
      </svg>
      <div className="leading-tight">
        <div className="text-[15px] font-bold" style={{ color: word }}>
          Harborline
        </div>
        <div className="text-[11px]" style={{ color: sub }}>
          Supplier performance
        </div>
      </div>
    </div>
  );
}

export function MenuLines({ className }: { className?: string }) {
  return (
    <span className={className} aria-hidden="true">
      <span className="flex h-4 w-5 flex-col justify-between">
        <span className="block h-[2px] w-full bg-current" />
        <span className="block h-[2px] w-full bg-current" />
        <span className="block h-[2px] w-full bg-current" />
      </span>
    </span>
  );
}
