
// src/api/exportApi.ts

import apiClient from "./client";


// ============================================================
// EXPORT RESUME AS DOCX
// ============================================================

export async function downloadDocx(
  versionId: number
): Promise<Blob> {

  const response =
    await apiClient.get<Blob>(
      `/export/docx/${versionId}`,
      {
        responseType: "blob",
      }
    );

  return response.data;
}


// ============================================================
// EXPORT RESUME AS PDF
// ============================================================

export async function downloadPdf(
  versionId: number
): Promise<Blob> {

  const response =
    await apiClient.get<Blob>(
      `/export/pdf/${versionId}`,
      {
        responseType: "blob",
      }
    );

  return response.data;
}


// ============================================================
// GENERIC FILE DOWNLOAD
// ============================================================

export function saveBlob(
  blob: Blob,
  filename: string
): void {

  const url =
    window.URL.createObjectURL(blob);

  const link =
    document.createElement("a");

  link.href = url;

  link.download = filename;

  document.body.appendChild(link);

  link.click();

  link.remove();

  window.URL.revokeObjectURL(url);
}


// ============================================================
// DOWNLOAD DOCX
// ============================================================

export async function exportDocx(
  versionId: number
): Promise<void> {

  const blob =
    await downloadDocx(
      versionId
    );

  saveBlob(
    blob,
    `resume_${versionId}.docx`
  );
}


// ============================================================
// DOWNLOAD PDF
// ============================================================

export async function exportPdf(
  versionId: number
): Promise<void> {

  const blob =
    await downloadPdf(
      versionId
    );

  saveBlob(
    blob,
    `resume_${versionId}.pdf`
  );
}
