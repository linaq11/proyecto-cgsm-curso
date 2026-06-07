import { type ComponentProps, type ReactNode } from "react";
import { type LucideIcon } from "lucide-react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

/* ---------------------------------------------------------------- Eyebrow */

export function Eyebrow({
  className,
  children,
  ...props
}: ComponentProps<"p">) {
  return (
    <p
      data-slot="eyebrow"
      className={cn(
        "deck-sans text-[0.72cqw] font-semibold uppercase tracking-[0.26em] text-[var(--brand-primary)]",
        className,
      )}
      {...props}
    >
      {children}
    </p>
  );
}

/* ------------------------------------------------------------- SlideHeader */

export function SlideHeader({
  eyebrow,
  title,
  className,
}: {
  eyebrow?: ReactNode;
  title: ReactNode;
  className?: string;
}) {
  return (
    <header data-slot="slide-header" className={cn("shrink-0", className)}>
      {eyebrow && <Eyebrow className="mb-[0.6cqw]">{eyebrow}</Eyebrow>}
      <h2 className="deck-serif text-[2.5cqw] font-semibold leading-[1.08] text-[var(--brand-ink)]">
        {title}
      </h2>
      <span className="mt-[0.9cqw] block h-[3px] w-[3.4cqw] rounded-full bg-[var(--brand-gold)]" />
    </header>
  );
}

/* --------------------------------------------------------------- Lead text */

export function Lead({ className, children, ...props }: ComponentProps<"p">) {
  return (
    <p
      className={cn(
        "deck-sans text-[1.2cqw] leading-[1.5] text-[var(--brand-ink-soft)]",
        className,
      )}
      {...props}
    >
      {children}
    </p>
  );
}

/* ------------------------------------------------------------------- Stat */

export function StatCard({
  value,
  unit,
  label,
  className,
}: {
  value: ReactNode;
  unit?: ReactNode;
  label: ReactNode;
  className?: string;
}) {
  return (
    <div
      data-slot="stat"
      className={cn(
        "flex flex-col justify-center rounded-2xl border border-[var(--brand-line)] bg-[var(--brand-paper-2)] px-[1.4cqw] py-[1.2cqw]",
        className,
      )}
    >
      <p className="deck-serif text-[2.7cqw] font-semibold leading-none text-[var(--brand-primary)]">
        {value}
        {unit && (
          <span className="deck-sans ml-1 text-[1cqw] font-medium text-[var(--brand-ink-soft)]">
            {unit}
          </span>
        )}
      </p>
      <p className="deck-sans mt-[0.7cqw] text-[0.92cqw] leading-snug text-[var(--brand-ink-soft)]">
        {label}
      </p>
    </div>
  );
}

/* ------------------------------------------------------------- IconBadge */

const iconBadge = cva(
  "inline-flex shrink-0 items-center justify-center rounded-xl",
  {
    variants: {
      tone: {
        primary: "bg-[var(--brand-tint-strong)] text-[var(--brand-primary)]",
        gold: "bg-[var(--brand-gold)]/18 text-[#9a6a00]",
        ink: "bg-[var(--brand-ink)]/8 text-[var(--brand-ink)]",
      },
      size: {
        md: "h-[2.4cqw] w-[2.4cqw]",
        lg: "h-[3cqw] w-[3cqw]",
      },
    },
    defaultVariants: { tone: "primary", size: "md" },
  },
);

export function IconBadge({
  icon: Icon,
  tone,
  size,
  className,
}: {
  icon: LucideIcon;
  className?: string;
} & VariantProps<typeof iconBadge>) {
  return (
    <span className={cn(iconBadge({ tone, size }), className)}>
      <Icon className="h-[52%] w-[52%]" strokeWidth={1.9} />
    </span>
  );
}

/* ------------------------------------------------------------ FeatureItem */

export function FeatureItem({
  icon,
  title,
  children,
  className,
}: {
  icon: LucideIcon;
  title: ReactNode;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <div
      data-slot="feature"
      className={cn(
        "flex gap-[1cqw] rounded-2xl border border-[var(--brand-line)] bg-[var(--brand-paper)] p-[1.2cqw]",
        className,
      )}
    >
      <IconBadge icon={icon} />
      <div className="min-w-0">
        <p className="deck-sans text-[1.06cqw] font-semibold text-[var(--brand-ink)]">
          {title}
        </p>
        {children && (
          <p className="deck-sans mt-[0.3cqw] text-[0.9cqw] leading-snug text-[var(--brand-ink-soft)]">
            {children}
          </p>
        )}
      </div>
    </div>
  );
}

/* --------------------------------------------------------- NumberedItem */

export function NumberedItem({
  n,
  title,
  children,
  tag,
  className,
}: {
  n: number | string;
  title: ReactNode;
  children?: ReactNode;
  tag?: ReactNode;
  className?: string;
}) {
  return (
    <div
      data-slot="numbered"
      className={cn(
        "relative flex flex-col rounded-2xl border border-[var(--brand-line)] bg-[var(--brand-paper)] p-[1.3cqw]",
        className,
      )}
    >
      <div className="mb-[0.6cqw] flex items-center justify-between">
        <span className="deck-serif text-[2cqw] font-semibold leading-none text-[var(--brand-primary)]/85">
          {typeof n === "number" ? String(n).padStart(2, "0") : n}
        </span>
        {tag && <Tag>{tag}</Tag>}
      </div>
      <p className="deck-sans text-[1.06cqw] font-semibold leading-snug text-[var(--brand-ink)]">
        {title}
      </p>
      {children && (
        <p className="deck-sans mt-[0.4cqw] text-[0.9cqw] leading-snug text-[var(--brand-ink-soft)]">
          {children}
        </p>
      )}
    </div>
  );
}

/* -------------------------------------------------------------------- Tag */

export function Tag({ className, children, ...props }: ComponentProps<"span">) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full bg-[var(--brand-tint-strong)] px-[0.7cqw] py-[0.25cqw] deck-sans text-[0.66cqw] font-semibold uppercase tracking-wider text-[var(--brand-primary)]",
        className,
      )}
      {...props}
    >
      {children}
    </span>
  );
}

/* ------------------------------------------------------------------ Panel */

export function Panel({
  title,
  icon: Icon,
  children,
  className,
  accent,
}: {
  title?: ReactNode;
  icon?: LucideIcon;
  children: ReactNode;
  className?: string;
  accent?: boolean;
}) {
  return (
    <section
      data-slot="panel"
      className={cn(
        "flex flex-col rounded-2xl border p-[1.2cqw]",
        accent
          ? "border-transparent bg-[var(--brand-primary)] text-[var(--brand-on-color)]"
          : "border-[var(--brand-line)] bg-[var(--brand-paper-2)]",
        className,
      )}
    >
      {title && (
        <div className="mb-[0.8cqw] flex items-center gap-[0.6cqw]">
          {Icon && (
            <Icon
              className={cn(
                "h-[1.2cqw] w-[1.2cqw]",
                accent
                  ? "text-[var(--brand-gold)]"
                  : "text-[var(--brand-primary)]",
              )}
              strokeWidth={2}
            />
          )}
          <h3
            className={cn(
              "deck-sans text-[1.02cqw] font-semibold",
              accent ? "text-white" : "text-[var(--brand-ink)]",
            )}
          >
            {title}
          </h3>
        </div>
      )}
      {children}
    </section>
  );
}

/* ------------------------------------------------------------- BulletList */

export function BulletList({
  items,
  className,
  inverted,
}: {
  items: ReactNode[];
  className?: string;
  inverted?: boolean;
}) {
  return (
    <ul className={cn("flex flex-col gap-[0.55cqw]", className)}>
      {items.map((item, i) => (
        <li key={i} className="flex gap-[0.6cqw]">
          <span
            className={cn(
              "mt-[0.55cqw] h-[0.45cqw] w-[0.45cqw] shrink-0 rounded-full",
              inverted ? "bg-[var(--brand-gold)]" : "bg-[var(--brand-primary)]",
            )}
          />
          <span
            className={cn(
              "deck-sans text-[0.96cqw] leading-snug",
              inverted
                ? "text-[var(--brand-on-color-soft)]"
                : "text-[var(--brand-ink-soft)]",
            )}
          >
            {item}
          </span>
        </li>
      ))}
    </ul>
  );
}
