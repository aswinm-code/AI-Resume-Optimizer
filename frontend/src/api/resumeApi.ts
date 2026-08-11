// src/api/resume.ts

import apiClient from "./client";

import type {
  Resume,
  ParsedResume,
} from "@/types";

// ============================================================
// UPLOAD RESPONSE
// ============================================================

export interface ResumeUploadResponse {

  id: number;

  filename: string;

  uploaded_at?: string;

  parsed_json?: ParsedResume;
}


// ============================================================
// UPLOAD RESUME
// ============================================================

export async function uploadResume(
  file: File
): Promise<ResumeUploadResponse> {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );


  const response =
    await apiClient.post<ResumeUploadResponse>(
      "/resumes/upload",
      formData,
      {
        /*
         * Do not manually set multipart boundary.
         *
         * Axios/browser will generate:
         *
         * Content-Type:
         * multipart/form-data;
         * boundary=....
         */
      }
    );


  return response.data;
}


// ============================================================
// ============================================================
// GET RESUME
// ============================================================

export async function getResume(
  resumeId: number
): Promise<Resume> {

  const response =
    await apiClient.get<Resume>(
      `/resumes/${resumeId}`
    );

  return response.data;
}


// ============================================================
// GET USER RESUMES
// ============================================================

export async function getResumes(): Promise<Resume[]> {

  const response =
    await apiClient.get<Resume[]>(
      "/resumes"
    );

  return response.data;
}

export { getResumes as listResumes };


// ============================================================
// DELETE RESUME
// ============================================================

export async function deleteResume(
  resumeId: number
): Promise<void> {

  await apiClient.delete(
    `/resumes/${resumeId}`
  );
}