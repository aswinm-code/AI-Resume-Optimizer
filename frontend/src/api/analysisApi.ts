
// src/api/analysisApi.ts

import apiClient from "./client";

import type {
  AnalysisResult,
} from "@/types";

interface AnalysisResponse {
  id: number;
  resume_id: number;
  job_description_id: number;
  result: AnalysisResult;
  created_at: string;
}


// ============================================================
// ANALYZE RESUME
// ============================================================

export async function analyzeResume(
  resumeId: number,
  jobDescriptionId: number
): Promise<AnalysisResult> {

  const response =
    await apiClient.post<AnalysisResponse>(
      "/analysis",
      {
        resume_id: resumeId,
        job_description_id: jobDescriptionId,
      }
    );

  return response.data.result;
}


// ============================================================
// GET ALL ANALYSIS
// ============================================================

export async function getAllAnalysis(): Promise<
  AnalysisResult[]
> {

  const response =
    await apiClient.get<AnalysisResponse[]>(
      "/analysis"
    );

  return response.data.map((item) => item.result);
}

export const listAnalyses = getAllAnalysis;


// ============================================================
// GET ANALYSIS
// ============================================================

export async function getAnalysis(
  analysisId: number
): Promise<AnalysisResult> {

  const response =
    await apiClient.get<AnalysisResponse>(
      `/analysis/${analysisId}`
    );

  return response.data.result;
}
