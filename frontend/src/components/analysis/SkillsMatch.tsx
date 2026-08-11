import React from "react";
import { Check, Plus } from "lucide-react";
import { Card, Badge, SectionHeading } from "@/components/common/ui";
import type { AnalysisResult } from "@/types";

export function SkillsMatch({ analysis }: { analysis: AnalysisResult }) {
  return (
    <div className="grid sm:grid-cols-2 gap-4">
      <Card className="p-6">
        <SectionHeading title="Matched Skills" />
        {analysis.matched_skills.length === 0 ? (
          <p className="text-sm text-muted">No matched skills reported.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {analysis.matched_skills.map((s) => (
              <Badge key={s} tone="good">
                <Check size={11} className="mr-1" /> {s}
              </Badge>
            ))}
          </div>
        )}
      </Card>
      <Card className="p-6">
        <SectionHeading title="Missing Skills" />
        {analysis.missing_skills.length === 0 ? (
          <p className="text-sm text-muted">No gaps found — nice work.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {analysis.missing_skills.map((s) => (
              <Badge key={s} tone="bad">
                <Plus size={11} className="mr-1" /> {s}
              </Badge>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
