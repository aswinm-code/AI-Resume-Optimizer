import React from "react";
import { Loader2, Inbox } from "lucide-react";

export function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  loading = false,
  disabled,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md";
  loading?: boolean;
}) {
  const base = "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
  const sizes = { sm: "text-xs px-3 py-1.5", md: "text-sm px-4 py-2.5" };
  const variants = {
    primary: "bg-accent text-white hover:bg-accent-dark",
    secondary: "bg-surface text-ink border border-line hover:border-ink/40",
    ghost: "bg-transparent text-muted hover:text-ink hover:bg-canvas",
    danger: "bg-transparent text-bad border border-bad/30 hover:bg-bad/5",
  };
  return (
    <button
      className={`${base} ${sizes[size]} ${variants[variant]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <Loader2 size={14} className="animate-spin" />}
      {children}
    </button>
  );
}

export function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`bg-surface border border-line rounded-xl shadow-card ${className}`}>{children}</div>;
}

export function Badge({
  children,
  tone = "neutral",
  className = "",
}: {
  children: React.ReactNode;
  tone?: "neutral" | "good" | "bad" | "accent";
  className?: string;
}) {
  const tones = {
    neutral: "bg-canvas text-muted border-line",
    good: "bg-good/10 text-good border-good/20",
    bad: "bg-bad/5 text-bad/90 border-bad/20",
    accent: "bg-accent-light text-accent border-accent/20",
  };
  return (
    <span className={`inline-flex items-center text-xs font-medium px-2.5 py-1 rounded-full border ${tones[tone]} ${className}`}>
      {children}
    </span>
  );
}

export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 text-sm text-muted">
      <Loader2 size={16} className="animate-spin" />
      {label}
    </div>
  );
}

export function EmptyState({ title, description }: { title: string; description?: string }) {
  return (
    <div className="text-center py-12 px-6">
      <Inbox size={28} className="mx-auto text-muted/60 mb-3" />
      <p className="text-sm font-medium text-ink">{title}</p>
      {description && <p className="text-sm text-muted mt-1">{description}</p>}
    </div>
  );
}

export function SectionHeading({ eyebrow, title }: { eyebrow?: string; title: string }) {
  return (
    <div className="mb-4">
      {eyebrow && <p className="text-xs font-semibold uppercase tracking-wide text-accent mb-1">{eyebrow}</p>}
      <h2 className="text-lg font-semibold text-ink">{title}</h2>
    </div>
  );
}
