import React from "react";
import { CheckCircle2 } from "lucide-react";
import { Card, SectionHeading } from "@/components/common/ui";

export function Strengths({ items }: { items: string[] }) {
  if (items.length === 0) return null;
  return (
    <Card className="p-6">
      <SectionHeading title="Strengths" />
      <ul className="space-y-2.5">
        {items.map((s, i) => (
          <li key={i} className="flex items-start gap-2 text-sm">
            <CheckCircle2 size={15} className="text-good shrink-0 mt-0.5" />
            <span>{s}</span>
          </li>
        ))}
      </ul>
    </Card>
  );
}
