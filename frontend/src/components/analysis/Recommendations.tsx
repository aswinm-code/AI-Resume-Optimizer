import React from "react";
import { Card, SectionHeading } from "@/components/common/ui";

export function Recommendations({ items }: { items: string[] }) {
  if (items.length === 0) return null;
  return (
    <Card className="p-6">
      <SectionHeading title="Recommendations" />
      <ol className="space-y-2.5">
        {items.map((s, i) => (
          <li key={i} className="flex items-start gap-3 text-sm">
            <span className="w-5 h-5 rounded-full bg-accent-light text-accent text-xs font-semibold flex items-center justify-center shrink-0 mt-0.5">
              {i + 1}
            </span>
            <span>{s}</span>
          </li>
        ))}
      </ol>
    </Card>
  );
}
