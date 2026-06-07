"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { X, Play, Pause, RotateCcw, ListChecks, FileText } from "lucide-react";
import { cn } from "@/lib/utils";
import { useDeck } from "./deck-context";

const TEAL = "#14c486";
const GOLD = "#ffb93e";
const RED = "#fb7185";
const TALK_TARGET = 660_000; // 11:00 for the spoken talk

function fmt(ms: number) {
  const s = Math.max(0, Math.round(ms / 1000));
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(
    s % 60,
  ).padStart(2, "0")}`;
}
const slideColor = (ms: number) => (ms < 60_000 ? TEAL : ms < 80_000 ? GOLD : RED);
const totalColor = (ms: number) =>
  ms < TALK_TARGET ? TEAL : ms < TALK_TARGET + 60_000 ? GOLD : RED;

/**
 * Presenter-notes drawer: Spanish speaker script for the active slide plus a
 * rehearsal timer that banks time per slide as you advance. Toggled with "N".
 */
export function DeckNotes() {
  const {
    slides,
    current,
    notesOpen,
    setNotesOpen,
    rehearsing,
    slideTimes,
    totalElapsed,
    lastRun,
    startRehearsal,
    pauseRehearsal,
    resetRehearsal,
  } = useDeck();
  const [view, setView] = useState<"script" | "times">("script");

  const note = slides[current]?.notes;
  const here = slideTimes[current] ?? 0;
  const maxT = Math.max(1, ...slideTimes);

  return (
    <AnimatePresence>
      {notesOpen && (
        <motion.aside
          key="notes"
          aria-label="Presenter notes"
          className="deck-no-print absolute inset-x-0 bottom-0 z-[35] max-h-[42%] overflow-hidden rounded-t-2xl border-t border-white/15 bg-gradient-to-t from-neutral-950/82 via-neutral-950/70 to-neutral-950/50 backdrop-blur-lg"
          initial={{ y: "100%" }}
          animate={{ y: 0 }}
          exit={{ y: "100%" }}
          transition={{ type: "tween", duration: 0.28, ease: "easeOut" }}
        >
          <div className="flex h-full flex-col px-[5%] pb-14 pt-3">
            {/* header */}
            <div className="mb-2 flex items-center justify-between gap-3">
              <p className="font-sans text-[11px] font-semibold uppercase tracking-[0.24em] text-[var(--brand-gold)]">
                Guion · ES
                <span className="ml-3 font-mono tracking-normal text-white/40">
                  {String(current + 1).padStart(2, "0")} / {slides.length} ·{" "}
                  {slides[current]?.title}
                </span>
              </p>
              <button
                type="button"
                aria-label="Close presenter notes"
                onClick={() => setNotesOpen(false)}
                className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/10 text-white/80 transition hover:bg-white/20 hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            {/* rehearsal timer bar */}
            <div className="mb-2 flex flex-wrap items-center gap-2 text-white">
              <span
                className="rounded-lg bg-white/8 px-2.5 py-1 font-mono text-[15px] font-bold tabular-nums"
                style={{ color: slideColor(here) }}
                title="Tiempo en esta diapositiva"
              >
                ◷ {fmt(here)}
              </span>
              <span
                className="rounded-lg bg-white/8 px-2.5 py-1 font-mono text-[15px] font-bold tabular-nums"
                style={{ color: totalColor(totalElapsed) }}
                title="Tiempo total / meta 11:00"
              >
                Σ {fmt(totalElapsed)}{" "}
                <span className="text-[11px] font-normal text-white/40">/ 11:00</span>
              </span>
              <button
                type="button"
                onClick={rehearsing ? pauseRehearsal : startRehearsal}
                className={cn(
                  "inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-[12px] font-bold transition",
                  rehearsing
                    ? "bg-[var(--brand-gold)]/20 text-[var(--brand-gold)] hover:bg-[var(--brand-gold)]/30"
                    : "bg-emerald-500/20 text-emerald-300 hover:bg-emerald-500/30",
                )}
              >
                {rehearsing ? (
                  <>
                    <Pause className="h-3.5 w-3.5" /> Pausar
                  </>
                ) : (
                  <>
                    <Play className="h-3.5 w-3.5" /> Ensayo
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={resetRehearsal}
                title="Reiniciar"
                className="inline-flex h-7 w-7 items-center justify-center rounded-lg bg-white/8 text-white/70 transition hover:bg-white/15 hover:text-white"
              >
                <RotateCcw className="h-3.5 w-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setView((v) => (v === "script" ? "times" : "script"))}
                className="inline-flex items-center gap-1.5 rounded-lg bg-white/8 px-3 py-1.5 text-[12px] font-semibold text-white/80 transition hover:bg-white/15 hover:text-white"
              >
                {view === "script" ? (
                  <>
                    <ListChecks className="h-3.5 w-3.5" /> Tiempos
                  </>
                ) : (
                  <>
                    <FileText className="h-3.5 w-3.5" /> Guion
                  </>
                )}
              </button>
              {lastRun && (
                <span className="font-mono text-[11px] text-white/35">
                  último ensayo: {fmt(lastRun.total)}
                </span>
              )}
            </div>

            {/* body */}
            <div className="deck-scroll overflow-y-auto pr-2">
              {view === "script" ? (
                <p className="max-w-[70ch] font-serif text-[clamp(14px,1.4vw,19px)] leading-relaxed text-white/90">
                  {note ?? (
                    <span className="text-white/40">
                      (Sin guion para esta diapositiva.)
                    </span>
                  )}
                </p>
              ) : (
                <div className="flex flex-col gap-1.5 pb-2">
                  {slides.map((s, i) => {
                    const t = slideTimes[i] ?? 0;
                    return (
                      <div
                        key={i}
                        className={cn(
                          "flex items-center gap-3 rounded-md px-2 py-1",
                          i === current && "bg-white/8",
                        )}
                      >
                        <span className="w-6 shrink-0 font-mono text-[12px] text-white/40">
                          {String(i + 1).padStart(2, "0")}
                        </span>
                        <span className="w-40 shrink-0 truncate text-[12.5px] text-white/80">
                          {s.title}
                        </span>
                        <span className="h-2 flex-1 overflow-hidden rounded-full bg-white/8">
                          <span
                            className="block h-full rounded-full"
                            style={{
                              width: `${(t / maxT) * 100}%`,
                              background: slideColor(t),
                            }}
                          />
                        </span>
                        <span
                          className="w-12 shrink-0 text-right font-mono text-[12.5px] font-bold tabular-nums"
                          style={{ color: t ? slideColor(t) : "rgba(255,255,255,.3)" }}
                        >
                          {fmt(t)}
                        </span>
                      </div>
                    );
                  })}
                  <div className="mt-1 flex items-center justify-end gap-2 border-t border-white/10 pt-1.5 text-[12.5px] text-white/60">
                    Total
                    <span
                      className="font-mono font-bold tabular-nums"
                      style={{ color: totalColor(totalElapsed) }}
                    >
                      {fmt(totalElapsed)}
                    </span>
                    <span className="text-white/30">/ 11:00</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
