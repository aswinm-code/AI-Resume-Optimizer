import React from "react";
import { PieChart, Pie, Cell } from "recharts";
import { Card, SectionHeading } from "@/components/common/ui";
import type { AnalysisResult } from "@/types";

function scoreLabel(score: number) {
  if (score >= 85) return "Excellent Match";
  if (score >= 70) return "Strong Match";
  if (score >= 50) return "Fair Match";
  return "Needs Work";
}

function scoreColor(score: number) {
  if (score >= 85) return "#16A34A";
  if (score >= 70) return "#2563EB";
  if (score >= 50) return "#D97706";
  return "#DC2626";
}

function RingScore({ score, size = 160 }: { score: number; size?: number }) {
  const color = scoreColor(score);
  const data = [
    { value: score },
    { value: 100 - score },
  ];
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <PieChart width={size} height={size}>
        <Pie
          data={data}
          dataKey="value"
          startAngle={90}
          endAngle={-270}
          innerRadius={size / 2 - 14}
          outerRadius={size / 2 - 2}
          stroke="none"
        >
          <Cell fill={color} />
          <Cell fill="#E5E7EB" />
        </Pie>
      </PieChart>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold" style={{ color }}>
          {Math.round(score)}%
        </span>
      </div>
    </div>
  );
}

function SubScore({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="flex items-center justify-between text-xs mb-1.5">
        <span className="text-muted font-medium">{label}</span>
        <span className="font-semibold text-ink">{Math.round(value)}%</span>
      </div>
      <div className="h-1.5 rounded-full bg-line overflow-hidden">
        <div className="h-full rounded-full bg-accent" style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

export function ScoreCard({ analysis }: { analysis: AnalysisResult }) {
  return (
    <Card className="p-6">
      <SectionHeading eyebrow="Match" title="Resume Analysis" />
      <div className="grid sm:grid-cols-[auto_1fr] gap-8 items-center">
        <div className="flex flex-col items-center">
          <RingScore score={analysis.overall_score} />
          <p className="text-sm font-medium mt-3">{scoreLabel(analysis.overall_score)}</p>
          <p className="text-xs text-muted">Overall Match</p>
        </div>
        <div className="space-y-4 w-full">
          <SubScore label="Skills Match" value={analysis.skills_score} />
          <SubScore label="Experience Match" value={analysis.experience_score} />
          <SubScore label="Education Match" value={analysis.education_score} />
          <SubScore label="Projects Match" value={analysis.projects_score} />
        </div>
      </div>
    </Card>
  );
}
