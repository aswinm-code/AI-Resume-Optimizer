
// src/components/resume/ResumeDownload.tsx

import { useState } from "react";

import {
  Download,
  FileText,
} from "lucide-react";

import {
  Button,
  Card,
} from "@/components/common/ui";

import {
  exportDocx,
  exportPdf,
} from "@/api/exportApi";

import {
  useToast,
} from "@/hooks/useToast";

import {
  readError,
} from "@/api/client";


interface ResumeDownloadProps {

  versionId: number;

}


export function ResumeDownload({
  versionId,
}: ResumeDownloadProps) {

  const toast =
    useToast();


  const [
    downloading,
    setDownloading,
  ] = useState<
    "docx" | "pdf" | null
  >(null);


  // ==========================================================
  // DOWNLOAD DOCX
  // ==========================================================

  const handleDocxDownload =
    async () => {

      try {

        setDownloading("docx");

        await exportDocx(
          versionId
        );

        toast.success(
          "DOCX resume downloaded."
        );

      } catch (error) {

        toast.error(
          readError(
            error,
            "Unable to download DOCX resume."
          )
        );

      } finally {

        setDownloading(null);

      }
    };


  // ==========================================================
  // DOWNLOAD PDF
  // ==========================================================

  const handlePdfDownload =
    async () => {

      try {

        setDownloading("pdf");

        await exportPdf(
          versionId
        );

        toast.success(
          "PDF resume downloaded."
        );

      } catch (error) {

        toast.error(
          readError(
            error,
            "Unable to download PDF resume."
          )
        );

      } finally {

        setDownloading(null);

      }
    };


  // ==========================================================
  // UI
  // ==========================================================

  return (

    <Card className="p-6">

      <div className="text-center">

        <h3
          className="
            text-base
            font-semibold
            text-ink
          "
        >
          Download Your Resume
        </h3>


        <p
          className="
            text-sm
            text-muted
            mt-1
            mb-5
          "
        >
          Download your optimized resume
          in an ATS-friendly format.
        </p>


        <div
          className="
            flex
            flex-col
            sm:flex-row
            justify-center
            gap-3
          "
        >

          {/* ==================================================
              DOCX
          ================================================== */}

          <Button
            variant="secondary"
            loading={
              downloading === "docx"
            }
            disabled={
              downloading !== null
            }
            onClick={
              handleDocxDownload
            }
          >

            <FileText size={16} />

            {downloading === "docx"
              ? "Downloading..."
              : "Download DOCX"}

          </Button>


          {/* ==================================================
              PDF
          ================================================== */}

          <Button
            loading={
              downloading === "pdf"
            }
            disabled={
              downloading !== null
            }
            onClick={
              handlePdfDownload
            }
          >

            <Download size={16} />

            {downloading === "pdf"
              ? "Downloading..."
              : "Download PDF"}

          </Button>

        </div>

      </div>

    </Card>
  );
}