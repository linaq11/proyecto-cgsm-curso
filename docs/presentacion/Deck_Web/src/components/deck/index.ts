import { DeckRoot } from "./deck";
import { Slide } from "./slide";

/** Composition namespace: `<Deck.Root>` … `<Deck.Slide>`. */
export const Deck = {
  Root: DeckRoot,
  Slide,
};

export { DeckRoot, Slide };
export { useDeck } from "./deck-context";
export type { Brand, SlideMeta, DeckContextValue } from "./deck-context";
export type { SlideProps } from "./slide";
export * from "./primitives";
