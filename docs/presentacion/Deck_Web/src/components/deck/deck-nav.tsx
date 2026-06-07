"use client";

import {
  ChevronLeft,
  ChevronRight,
  LayoutGrid,
  Palette,
  Maximize,
  NotebookText,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useDeck } from "./deck-context";
import { toggleFullscreen } from "./deck";

function NavButton({
  label,
  onClick,
  disabled,
  children,
  className,
}: {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <button
      type="button"
      aria-label={label}
      title={label}
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "inline-flex h-8 w-8 items-center justify-center rounded-full text-white/80",
        "transition hover:bg-white/15 hover:text-white focus-visible:outline-none",
        "focus-visible:ring-2 focus-visible:ring-[var(--brand-gold)]",
        "disabled:cursor-not-allowed disabled:opacity-30",
        className,
      )}
    >
      {children}
    </button>
  );
}

/** Floating control bar: navigation, slide counter, overview, theme, fullscreen. */
export function DeckNav() {
  const {
    current,
    total,
    next,
    prev,
    goTo,
    brand,
    toggleBrand,
    setOverview,
    notesOpen,
    toggleNotes,
    rehearsing,
    totalElapsed,
  } = useDeck();

  const mm = String(Math.floor(totalElapsed / 60000)).padStart(2, "0");
  const ss = String(Math.floor((totalElapsed % 60000) / 1000)).padStart(2, "0");

  return (
    <div className="deck-no-print absolute inset-x-0 bottom-0 z-40 flex justify-center pb-3 sm:pb-4">
      <div
        className={cn(
          "flex items-center gap-1 rounded-full border border-white/10 px-2 py-1.5",
          "bg-black/45 backdrop-blur-md shadow-lg",
        )}
      >
        {rehearsing && (
          <span className="mr-1 inline-flex items-center gap-1.5 rounded-full bg-emerald-500/15 px-2.5 py-1 font-mono text-xs font-bold text-emerald-300">
            <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
            {mm}:{ss}
          </span>
        )}
        <NavButton label="Previous slide" onClick={prev} disabled={current === 0}>
          <ChevronLeft className="h-4 w-4" />
        </NavButton>

        <button
          type="button"
          onClick={() => setOverview(true)}
          title="Slide overview (G)"
          className="min-w-[64px] rounded-full px-3 py-1 text-center font-mono text-xs tracking-widest text-white/90 transition hover:bg-white/10"
        >
          {String(current + 1).padStart(2, "0")}
          <span className="text-white/40"> / {String(total).padStart(2, "0")}</span>
        </button>

        <NavButton
          label="Next slide"
          onClick={next}
          disabled={current === total - 1}
        >
          <ChevronRight className="h-4 w-4" />
        </NavButton>

        <span className="mx-1 h-5 w-px bg-white/15" />

        <NavButton
          label="Presenter notes (N)"
          onClick={toggleNotes}
          className={cn(notesOpen && "bg-white/15 text-[var(--brand-gold)]")}
        >
          <NotebookText className="h-[15px] w-[15px]" />
        </NavButton>
        <NavButton label="Slide overview (G)" onClick={() => setOverview(true)}>
          <LayoutGrid className="h-[15px] w-[15px]" />
        </NavButton>
        <NavButton
          label={`Theme: ${brand} — switch (T)`}
          onClick={toggleBrand}
        >
          <Palette className="h-[15px] w-[15px]" />
        </NavButton>
        <NavButton label="Fullscreen (F)" onClick={toggleFullscreen}>
          <Maximize className="h-[15px] w-[15px]" />
        </NavButton>
      </div>

      {/* tiny dot rail above the bar */}
      <div className="pointer-events-none absolute -top-2 left-1/2 hidden -translate-x-1/2 gap-1 sm:flex">
        {Array.from({ length: total }).map((_, i) => (
          <button
            key={i}
            type="button"
            aria-label={`Go to slide ${i + 1}`}
            onClick={() => goTo(i)}
            className={cn(
              "pointer-events-auto h-1 rounded-full transition-all",
              i === current
                ? "w-4 bg-[var(--brand-gold)]"
                : "w-1 bg-white/30 hover:bg-white/60",
            )}
          />
        ))}
      </div>
    </div>
  );
}
