import React, { useRef, useState } from "react";
import { UploadCloud, FileCheck2, RefreshCcw } from "lucide-react";
import { Card, Button, Spinner } from "@/components/common/ui";

interface Props {
  currentResume?: { filename: string; uploaded_at?: string; size_bytes?: number } | null;
  uploading: boolean;
  progress: number;
  onUpload: (file: File) => void;
}

function formatSize(bytes?: number) {
  if (!bytes) return null;
  const kb = bytes / 1024;
  return kb > 1024 ? `${(kb / 1024).toFixed(1)} MB` : `${Math.round(kb)} KB`;
}

export function ResumeUpload({ currentResume, uploading, progress, onUpload }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const pick = (files: FileList | null) => {
    if (files && files[0]) onUpload(files[0]);
  };

  return (
    <Card className="p-6 h-full">
      <h3 className="text-sm font-semibold mb-1">Upload your resume</h3>
      <p className="text-xs text-muted mb-4">Supported formats: PDF / DOCX</p>

      {uploading ? (
        <div className="border-2 border-dashed border-line rounded-xl px-6 py-12 flex flex-col items-center justify-center gap-3">
          <Spinner label={`Uploading… ${progress > 0 ? `${progress}%` : ""}`} />
        </div>
      ) : currentResume ? (
        <div className="border border-line rounded-xl px-5 py-6 flex flex-col items-center text-center gap-2">
          <FileCheck2 size={28} className="text-good" />
          <p className="text-sm font-medium">{currentResume.filename}</p>
          <p className="text-xs text-muted">
            {formatSize(currentResume.size_bytes) || "Uploaded successfully"}
            {currentResume.uploaded_at && ` · ${new Date(currentResume.uploaded_at).toLocaleDateString()}`}
          </p>
          <Button variant="secondary" size="sm" className="mt-2" onClick={() => inputRef.current?.click()}>
            <RefreshCcw size={13} /> Replace
          </Button>
        </div>
      ) : (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            pick(e.dataTransfer.files);
          }}
          onClick={() => inputRef.current?.click()}
          className={`cursor-pointer border-2 border-dashed rounded-xl px-6 py-12 flex flex-col items-center justify-center gap-3 text-center transition-colors ${
            dragging ? "border-accent bg-accent-light" : "border-line hover:border-ink/30"
          }`}
        >
          <UploadCloud size={26} className="text-muted" />
          <div>
            <p className="text-sm font-medium">Drag & drop your resume here</p>
            <p className="text-xs text-muted mt-1">
              or <span className="text-accent font-medium">Browse Files</span>
            </p>
          </div>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.doc"
        className="hidden"
        onChange={(e) => pick(e.target.files)}
      />
    </Card>
  );
}
