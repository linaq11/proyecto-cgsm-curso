"use client";

import { X } from "lucide-react";
import { motion } from "motion/react";
import { cn } from "@/lib/utils";
import { useDeck } from "./deck-context";

/** Full-screen grid of slide titles for quick jumping (press G or Esc to close). */
export function DeckOverview() {
  const { slides, current, goTo, setOverview, brand } = useDeck();

  return (
    <motion.div
      data-brand={brand}
      className="deck-no-print absolute inset-0 z-50 flex flex-col bg-[var(--brand-primary-deep)]/97 backdrop-blur-sm"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="flex items-center justify-between px-8 py-6 text-white">
        <div>
          <p className="deck-sans text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--brand-gold)]">
            Overview
          </p>
          <h2 className="deck-serif text-2xl">Jump to a slide</h2>
        </div>
        <button
          type="button"
          aria-label="Close overview"
          onClick={() => setOverview(false)}
          className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-white transition hover:bg-white/20"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      <div className="deck-scroll flex-1 overflow-y-auto px-8 pb-10">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {slides.map((s) => {
            const isCurrent = s.index === current;
            return (
              <button
                key={s.index}
                type="button"
                onClick={() => goTo(s.index)}
                className={cn(
                  "group flex aspect-[16/10] flex-col justify-between rounded-xl border p-4 text-left transition",
                  isCurrent
                    ? "border-[var(--brand-gold)] bg-white/15"
                    : "border-white/12 bg-white/5 hover:border-white/40 hover:bg-white/10",
                )}
              >
                <span
                  className={cn(
                    "deck-serif text-3xl tabular-nums",
                    isCurrent ? "text-[var(--brand-gold)]" : "text-white/45",
                  )}
                >
                  {String(s.index + 1).padStart(2, "0")}
                </span>
                <span className="deck-sans text-sm font-medium leading-snug text-white">
                  {s.title}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
}
