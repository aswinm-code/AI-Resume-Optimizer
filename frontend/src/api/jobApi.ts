
// src/api/jobDescription.ts

import apiClient from "./client";

// ============================================================
// TYPES
// ============================================================

export interface ParsedJobDescription {
  title: string;
  experience_required: string;
  skills: string[];
  responsibilities: string[];
  qualifications: string[];
  preferred_skills: string[];
  technologies: string[];
  keywords: string[];
}

export interface JobDescription {
  id: number;
  title?: string;
  description: string;
  parsed_json?: ParsedJobDescription;
  created_at?: string;
}

// ============================================================
// CREATE JOB DESCRIPTION
// ============================================================

export async function createJobDescription(
  text: string
): Promise<JobDescription> {
  const response = await apiClient.post<JobDescription>(
    "/job-descriptions",
    {
      description: text.trim(),
    }
  );

  return response.data;
}

// ============================================================
// GET JOB DESCRIPTION
// ============================================================

export async function getJobDescription(
  jobDescriptionId: number
): Promise<JobDescription> {
  const response = await apiClient.get<JobDescription>(
    `/job-descriptions/${jobDescriptionId}`
  );

  return response.data;
}

// ============================================================
// GET USER JOB DESCRIPTIONS
// ============================================================

export async function getJobDescriptions(): Promise<JobDescription[]> {
  const response = await apiClient.get<JobDescription[]>(
    "/job-descriptions",
  );

  return response.data;
}

// ============================================================
// DELETE JOB DESCRIPTION
// ============================================================

export async function deleteJobDescription(
  jobDescriptionId: number
): Promise<void> {
  await apiClient.delete(
    `/job-descriptions/${jobDescriptionId}`
  );
}
