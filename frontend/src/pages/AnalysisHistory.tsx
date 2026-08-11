import React from "react";
import { useQuery } from "@tanstack/react-query";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, EmptyState, Badge } from "@/components/common/ui";
import * as analysisApi from "@/api/analysisApi";

function scoreTone(score: number): "good" | "accent" | "bad" {
  if (score >= 75) return "good";
  if (score >= 50) return "accent";
  return "bad";
}

export default function AnalysisHistory() {
  const { data, isLoading } = useQuery({ queryKey: ["analyses"], queryFn: analysisApi.listAnalyses });

  return (
    <AppLayout>
      <div className="mb-6">
        <h1 className="text-xl font-semibold">Analysis History</h1>
        <p className="text-sm text-muted mt-1">Every resume-to-job match you've run.</p>
      </div>

      {isLoading ? (
        <p className="text-sm text-muted">Loading…</p>
      ) : !data || data.length === 0 ? (
        <Card>
          <EmptyState
            title="No analysis available."
            description="Run an analysis from the Dashboard to see your match score here."
          />
        </Card>
      ) : (
        <div className="space-y-3">
          {data.map((a) => (
            <Card key={a.id} className="p-4 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Analysis #{a.id}</p>
                {a.created_at && <p className="text-xs text-muted mt-0.5">{new Date(a.created_at).toLocaleString()}</p>}
              </div>
              <Badge tone={scoreTone(a.overall_score)}>{Math.round(a.overall_score)}% match</Badge>
            </Card>
          ))}
        </div>
      )}
    </AppLayout>
  );
}
