"use client";

import { type ReactNode } from "react";
import { motion } from "motion/react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { useDeck } from "./deck-context";

const slideVariants = cva(
  "absolute inset-0 h-full w-full overflow-hidden bg-cover bg-center",
  {
    variants: {
      variant: {
        cover: "text-[var(--brand-on-color)]",
        content: "text-[var(--brand-ink)]",
        closing: "text-[var(--brand-on-color)]",
      },
    },
    defaultVariants: { variant: "content" },
  },
);

const safeArea = cva("relative z-10 flex h-full w-full flex-col", {
  variants: {
    variant: {
      // clear the gold top rule, the footer bar and the corner crest
      content: "px-[6%] pt-[7.5%] pb-[12%]",
      cover: "px-[9%] pt-[12%] pb-[16%] justify-center",
      closing: "px-[9%] pt-[10%] pb-[10%] justify-end",
    },
  },
  defaultVariants: { variant: "content" },
});

const BG_BY_VARIANT: Record<
  NonNullable<VariantProps<typeof slideVariants>["variant"]>,
  string
> = {
  cover: "title",
  content: "content",
  closing: "crest",
};

export interface SlideProps
  extends VariantProps<typeof slideVariants> {
  /** short label surfaced in the overview grid + progress rail (required) */
  title: string;
  /** speaker script (Spanish) surfaced in the presenter-notes panel */
  notes?: ReactNode;
  children?: ReactNode;
  className?: string;
  /** injected by <Deck.Root> via cloneElement — do not pass manually */
  index?: number;
}

/**
 * A single full-bleed 16:9 slide. The institutional background is selected
 * from the active palette + variant, so flipping the brand re-skins every
 * slide at once. Only the active slide receives pointer + a11y focus.
 */
export function Slide({
  title,
  children,
  className,
  variant = "content",
  index = 0,
}: SlideProps) {
  const { current, brand } = useDeck();
  const active = index === current;
  const v = variant ?? "content";
  const bgKey = BG_BY_VARIANT[v];

  return (
    <motion.section
      role="group"
      aria-roledescription="slide"
      aria-label={`${index + 1}. ${title}`}
      aria-hidden={!active}
      data-slot="slide"
      data-slide-variant={v}
      data-state={active ? "active" : "inactive"}
      className={cn(
        slideVariants({ variant: v }),
        !active && "pointer-events-none",
        className,
      )}
      style={{ backgroundImage: `url(/brand/${brand}-${bgKey}.png)` }}
      initial={false}
      animate={{ opacity: active ? 1 : 0 }}
      transition={{ duration: 0.45, ease: "easeInOut" }}
    >
      {(v === "cover" || v === "closing") && (
        <div
          aria-hidden
          className="absolute inset-0 z-0"
          style={{
            background:
              "radial-gradient(120% 90% at 18% 30%, rgba(0,0,0,0.18), transparent 60%)",
          }}
        />
      )}

      <motion.div
        className={safeArea({ variant: v })}
        initial={false}
        animate={
          active
            ? { opacity: 1, y: 0 }
            : { opacity: 0, y: 14 }
        }
        transition={{ duration: 0.5, ease: "easeOut", delay: active ? 0.08 : 0 }}
      >
        {children}
      </motion.div>
    </motion.section>
  );
}
