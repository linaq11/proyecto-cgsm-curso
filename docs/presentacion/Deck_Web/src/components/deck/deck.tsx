"use client";

import {
  Children,
  cloneElement,
  isValidElement,
  useCallback,
  useEffect,
  useMemo,
  useReducer,
  useRef,
  useState,
  type ReactElement,
  type ReactNode,
} from "react";
import { cn } from "@/lib/utils";
import {
  DeckContext,
  type Brand,
  type DeckContextValue,
  type RehearsalRun,
  type SlideMeta,
} from "./deck-context";
import { DeckNav } from "./deck-nav";
import { DeckNotes } from "./deck-notes";
import { DeckOverview } from "./deck-overview";
import type { SlideProps } from "./slide";

export interface DeckRootProps {
  children: ReactNode;
  /** initial institutional palette */
  brand?: Brand;
  className?: string;
}

/**
 * Root of the presentation. Holds the active-slide index, the institutional
 * palette, and overview state in context, wires up keyboard navigation, and
 * letterboxes its slides to a fixed 16:9 stage.
 */
export function DeckRoot({
  children,
  brand: initialBrand = "verde",
  className,
}: DeckRootProps) {
  const childArray = useMemo(
    () =>
      Children.toArray(children).filter(isValidElement) as ReactElement<
        SlideProps
      >[],
    [children],
  );

  const total = childArray.length;
  const slides: SlideMeta[] = useMemo(
    () =>
      childArray.map((child, index) => ({
        index,
        title: child.props.title ?? `Slide ${index + 1}`,
        notes: child.props.notes,
      })),
    [childArray],
  );

  const [current, setCurrent] = useState(0);
  const [brand, setBrand] = useState<Brand>(initialBrand);
  const [overview, setOverview] = useState(false);
  const [notesOpen, setNotesOpen] = useState(false);

  const goTo = useCallback(
    (index: number) => {
      setCurrent((c) => {
        const clamped = Math.max(0, Math.min(total - 1, index));
        return clamped === c ? c : clamped;
      });
      setOverview(false);
    },
    [total],
  );

  const next = useCallback(
    () => setCurrent((c) => Math.min(total - 1, c + 1)),
    [total],
  );
  const prev = useCallback(() => setCurrent((c) => Math.max(0, c - 1)), []);
  const toggleBrand = useCallback(
    () => setBrand((b) => (b === "verde" ? "morado" : "verde")),
    [],
  );
  const toggleNotes = useCallback(() => setNotesOpen((o) => !o), []);

  /* ----------------------------- rehearsal timer ----------------------------- */
  const currentRef = useRef(0);
  currentRef.current = current;
  const timesRef = useRef<number[]>(Array(total).fill(0));
  const startRef = useRef(0);
  const idxRef = useRef(0);
  const [rehearsing, setRehearsing] = useState(false);
  const [, force] = useReducer((x: number) => x + 1, 0);
  const [lastRun, setLastRun] = useState<RehearsalRun | null>(null);

  // keep the per-slide buffer sized to the deck
  useEffect(() => {
    if (timesRef.current.length !== total)
      timesRef.current = Array(total).fill(0);
  }, [total]);

  // load the last saved run
  useEffect(() => {
    try {
      const r = localStorage.getItem("deck_rehearsal");
      if (r) setLastRun(JSON.parse(r) as RehearsalRun);
    } catch {}
  }, []);

  // live re-render while rehearsing
  useEffect(() => {
    if (!rehearsing) return;
    const id = setInterval(force, 500);
    return () => clearInterval(id);
  }, [rehearsing]);

  // bank the elapsed time onto the previous slide when the slide changes
  useEffect(() => {
    if (!rehearsing) return;
    if (idxRef.current !== current) {
      const arr = timesRef.current;
      arr[idxRef.current] =
        (arr[idxRef.current] || 0) + (Date.now() - startRef.current);
      startRef.current = Date.now();
      idxRef.current = current;
      force();
    }
  }, [current, rehearsing]);

  const startRehearsal = useCallback(() => {
    timesRef.current = Array(total).fill(0);
    idxRef.current = currentRef.current;
    startRef.current = Date.now();
    setRehearsing(true);
  }, [total]);

  const pauseRehearsal = useCallback(() => {
    const arr = timesRef.current;
    arr[idxRef.current] =
      (arr[idxRef.current] || 0) + (Date.now() - startRef.current);
    const times = arr.slice();
    const run: RehearsalRun = {
      total: times.reduce((a, b) => a + b, 0),
      times,
      date: new Date().toISOString(),
    };
    try {
      localStorage.setItem("deck_rehearsal", JSON.stringify(run));
    } catch {}
    setLastRun(run);
    setRehearsing(false);
  }, []);

  const resetRehearsal = useCallback(() => {
    timesRef.current = Array(total).fill(0);
    idxRef.current = currentRef.current;
    startRef.current = Date.now();
    setRehearsing(false);
    force();
  }, [total]);

  const curLive = rehearsing ? Date.now() - startRef.current : 0;
  const slideTimes = timesRef.current.map((v, i) =>
    i === idxRef.current && rehearsing ? v + curLive : v,
  );
  const totalElapsed = slideTimes.reduce((a, b) => a + b, 0);

  // Keyboard navigation
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName)) return;

      switch (e.key) {
        case "ArrowRight":
        case "PageDown":
        case " ":
          e.preventDefault();
          overview ? setOverview(false) : next();
          break;
        case "ArrowLeft":
        case "PageUp":
          e.preventDefault();
          prev();
          break;
        case "Home":
          e.preventDefault();
          goTo(0);
          break;
        case "End":
          e.preventDefault();
          goTo(total - 1);
          break;
        case "g":
        case "G":
          setOverview((o) => !o);
          break;
        case "t":
        case "T":
          toggleBrand();
          break;
        case "f":
        case "F":
          toggleFullscreen();
          break;
        case "n":
        case "N":
          setNotesOpen((o) => !o);
          break;
        case "r":
        case "R":
          rehearsing ? pauseRehearsal() : startRehearsal();
          break;
        case "Escape":
          setOverview(false);
          setNotesOpen(false);
          break;
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [
    next,
    prev,
    goTo,
    toggleBrand,
    total,
    overview,
    rehearsing,
    startRehearsal,
    pauseRehearsal,
  ]);

  const value: DeckContextValue = {
    current,
    total,
    brand,
    overview,
    notesOpen,
    slides,
    goTo,
    next,
    prev,
    setBrand,
    toggleBrand,
    setOverview,
    toggleNotes,
    setNotesOpen,
    rehearsing,
    slideTimes,
    totalElapsed,
    lastRun,
    startRehearsal,
    pauseRehearsal,
    resetRehearsal,
  };

  return (
    <DeckContext.Provider value={value}>
      <div
        data-brand={brand}
        data-slot="deck"
        className={cn(
          "relative flex h-dvh w-full items-center justify-center overflow-hidden",
          "bg-[var(--deck-stage)] deck-sans select-none",
          className,
        )}
      >
        {/* progress rail */}
        <div className="deck-no-print absolute inset-x-0 top-0 z-30 h-1 bg-black/30">
          <div
            className="h-full bg-[var(--brand-gold)] transition-[width] duration-500 ease-out"
            style={{ width: `${((current + 1) / total) * 100}%` }}
          />
        </div>

        {/* 16:9 stage */}
        <div
          data-slot="deck-stage"
          className="relative aspect-[16/9] w-full max-h-[100dvh] max-w-[177.78dvh] shadow-2xl"
          style={{ containerType: "size" }}
        >
          {childArray.map((child, index) =>
            cloneElement(child, { index, key: index }),
          )}
        </div>

        {overview && <DeckOverview />}
        <DeckNotes />
        <DeckNav />
      </div>
    </DeckContext.Provider>
  );
}

function toggleFullscreen() {
  if (typeof document === "undefined") return;
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen?.().catch(() => {});
  } else {
    document.exitFullscreen?.().catch(() => {});
  }
}

export { toggleFullscreen };
