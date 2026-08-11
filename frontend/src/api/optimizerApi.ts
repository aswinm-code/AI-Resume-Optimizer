
// src/api/optimizerApi.ts

import apiClient from "./client";

import type {
  ResumeVersionResponse,
} from "@/types";


// ============================================================
// OPTIMIZE RESUME
// ============================================================

export async function optimizeResume(
  resumeId: number,
  jobDescriptionId: number
): Promise<ResumeVersionResponse> {

  const response =
    await apiClient.post<ResumeVersionResponse>(
      "/resume-optimizer",
      {
        resume_id: resumeId,
        job_description_id: jobDescriptionId,
        version_name: "AI Optimized Resume",
      }
    );

  return response.data;
}
