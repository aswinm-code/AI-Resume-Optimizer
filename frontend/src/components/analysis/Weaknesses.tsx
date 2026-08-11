import React from "react";
import { Card, SectionHeading } from "@/components/common/ui";

export function Weaknesses({ items }: { items: string[] }) {
  if (items.length === 0) return null;
  return (
    <Card className="p-6">
      <SectionHeading title="Areas to Improve" />
      <ul className="space-y-2.5">
        {items.map((s, i) => (
          <li key={i} className="flex items-start gap-2 text-sm">
            <span className="text-warn mt-1.5 w-1.5 h-1.5 rounded-full bg-warn shrink-0" />
            <span>{s}</span>
          </li>
        ))}
      </ul>
    </Card>
  );
}
