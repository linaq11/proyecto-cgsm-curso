"use client";

import { createContext, useContext, type ReactNode } from "react";

export type Brand = "verde" | "morado" | "monitor";

export interface SlideMeta {
  /** 0-based position in the deck */
  index: number;
  /** short label shown in the overview grid and progress rail */
  title: string;
  /** speaker script (Spanish) shown in the presenter-notes panel */
  notes?: ReactNode;
}

/** A saved rehearsal run: total ms, per-slide ms, ISO date. */
export interface RehearsalRun {
  total: number;
  times: number[];
  date: string;
}

export interface DeckContextValue {
  current: number;
  total: number;
  brand: Brand;
  overview: boolean;
  notesOpen: boolean;
  slides: SlideMeta[];
  goTo: (index: number) => void;
  next: () => void;
  prev: () => void;
  setBrand: (brand: Brand) => void;
  toggleBrand: () => void;
  setOverview: (open: boolean) => void;
  toggleNotes: () => void;
  setNotesOpen: (open: boolean) => void;
  /** rehearsal timer */
  rehearsing: boolean;
  slideTimes: number[];
  totalElapsed: number;
  lastRun: RehearsalRun | null;
  startRehearsal: () => void;
  pauseRehearsal: () => void;
  resetRehearsal: () => void;
}

export const DeckContext = createContext<DeckContextValue | null>(null);

export function useDeck(): DeckContextValue {
  const ctx = useContext(DeckContext);
  if (!ctx) {
    throw new Error("useDeck must be used within a <Deck.Root>.");
  }
  return ctx;
}
