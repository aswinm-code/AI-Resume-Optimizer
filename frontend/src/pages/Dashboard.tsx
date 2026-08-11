// src/pages/Dashboard.tsx

import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  Sparkles,
  Wand2,
} from "lucide-react";

import {
  AppLayout,
} from "@/components/layout/AppLayout";

import {
  ResumeUpload,
} from "@/components/resume/ResumeUpload";

import {
  JobDescriptionInput,
} from "@/components/job/JobDescriptionInput";

import {
  ResumePreview,
} from "@/components/resume/ResumePreview";

import {
  ResumeDownload,
} from "@/components/resume/ResumeDownload";

import {
  ScoreCard,
} from "@/components/analysis/ScoreCard";

import {
  SkillsMatch,
} from "@/components/analysis/SkillsMatch";

import {
  Strengths,
} from "@/components/analysis/Strengths";

import {
  Weaknesses,
} from "@/components/analysis/Weaknesses";

import {
  Recommendations,
} from "@/components/analysis/Recommendations";

import {
  Button,
  Card,
  EmptyState,
} from "@/components/common/ui";

import {
  useToast,
} from "@/hooks/useToast";

import {
  readError,
} from "@/api/client";

import * as resumeApi
  from "@/api/resumeApi";

import * as jobApi
  from "@/api/jobApi";

import * as analysisApi
  from "@/api/analysisApi";

import * as optimizerApi
  from "@/api/optimizerApi";

import type {
  JobDescription,
  AnalysisResult,
  ResumeVersionResponse,
} from "@/types";

// ============================================================
// OPTIMIZATION PROGRESS
// ============================================================

const OPTIMIZE_STEPS = [

  "Analyzing job requirements",

  "Matching relevant skills",

  "Improving resume wording",

  "Preparing optimized resume",

];


// ============================================================
// DASHBOARD
// ============================================================

export default function Dashboard() {

  const toast =
    useToast();

  const queryClient =
    useQueryClient();


  // ==========================================================
  // STATE
  // ==========================================================

  const [
    jdText,
    setJdText,
  ] = useState("");

  const [
    savedJd,
    setSavedJd,
  ] = useState<JobDescription | null>(
    null
  );

  const [
    analysis,
    setAnalysis,
  ] = useState<AnalysisResult | null>(
    null
  );

  const [
    optimized,
    setOptimized,
  ] = useState<ResumeVersionResponse | null>(
    null
  );

  const [
    uploadProgress,
    setUploadProgress,
  ] = useState(0);

  const [
    stepIndex,
    setStepIndex,
  ] = useState(0);

  const stepTimer =
    useRef<ReturnType<typeof setInterval> | null>(
      null
    );

  // ==========================================================
  // GET USER RESUMES
  // ==========================================================

  const resumesQuery = useQuery({
    queryKey: ["resumes"],
    queryFn: resumeApi.getResumes,
  });

  
  const currentResume =
    resumesQuery.data?.[0] ?? null;

  // ==========================================================
  // UPLOAD RESUME
  // ==========================================================

  const uploadMutation =
    useMutation({
      mutationFn:
        (file: File) =>
          resumeApi.uploadResume(file),
      onSuccess: () => {
        queryClient.invalidateQueries({
          queryKey: [
            "resumes",
          ],
        });
        toast.success("Resume uploaded successfully.");
        setUploadProgress(0);
        setAnalysis(null);
        setOptimized(null);
      },
      onError: (error) => {
        toast.error(
          readError(
            error,
            "Unable to upload resume."
          )
        );
        setUploadProgress(0);
      },
    });

  // ==========================================================
  // CREATE / REUSE JOB DESCRIPTION
  // ==========================================================

  const ensureJobDescription =
    async (): Promise<JobDescription> => {
      if (
        savedJd &&
        savedJd.description === jdText
      ) {
        return savedJd;
      }
      const jobDescription =
        await jobApi.createJobDescription(jdText);
      setSavedJd(jobDescription);
      return jobDescription;
    };

  // ==========================================================
  // ANALYZE
  // ==========================================================

  const analyzeMutation =
    useMutation({
      mutationFn:
        async () => {
          if (!currentResume) {
            throw new Error("Please upload a resume first.");
          }
          if (!jdText.trim()) {
            throw new Error("Please enter a job description.");
          }
          const jobDescription = await ensureJobDescription();
          return analysisApi.analyzeResume(currentResume.id, jobDescription.id);
        },
      onSuccess: (result) => {
        setAnalysis(result);
        toast.success("Resume analysis completed.");
      },
      onError: (error) => {
        toast.error(
          readError(
            error,
            "Unable to analyze resume."
          )
        );
      },
    });

  // ==========================================================
  // OPTIMIZE
  // ==========================================================

  const optimizeMutation =
    useMutation({
      mutationFn:
        async () => {
          if (!currentResume) {
            throw new Error("Please upload a resume first.");
          }
          if (!jdText.trim()) {
            throw new Error("Please enter a job description.");
          }
          const jobDescription = await ensureJobDescription();
          return optimizerApi.optimizeResume(currentResume.id, jobDescription.id);
        },
      onSuccess: (result) => {
        setOptimized(result);
        toast.success("Resume optimized successfully.");
      },
      onError: (error) => {
        toast.error(
          readError(
            error,
            "Unable to optimize resume."
          )
        );
      },
    });

  // ==========================================================
  // OPTIMIZATION PROGRESS
  // ==========================================================

  useEffect(() => {
    if (optimizeMutation.isPending) {
      setStepIndex(0);
      stepTimer.current = setInterval(() => {
        setStepIndex((current) => (current + 1) % OPTIMIZE_STEPS.length);
      }, 1400);
    }
    return () => {
      if (stepTimer.current) {
        clearInterval(stepTimer.current);
        stepTimer.current = null;
      }
    };
  }, [optimizeMutation.isPending]);

  // ==========================================================
  // VALIDATION
  // ==========================================================

  const canRun =
    Boolean(currentResume) && jdText.trim().length > 0;

  const validationMessage =
    !currentResume
      ? "Upload your resume to get started."
      : !jdText.trim()
        ? "Paste a job description to continue."
        : null;

  // ==========================================================
  // UI
  // ==========================================================

  return (
    <AppLayout>
      <div className="space-y-8">
        {/* ==================================================
            HEADER
        ================================================== */}

        <div>
          <h1 className="text-2xl font-bold text-ink">
            AI Resume Optimizer
          </h1>
          <p className="text-sm text-muted mt-1">
            Analyze and optimize your resume
            against a specific job description.
          </p>
        </div>


        {/* ==================================================
            INPUT AREA
        ================================================== */}

        <div
          className="
            grid
            grid-cols-1
            lg:grid-cols-2
            gap-5
          "
        >
          <ResumeUpload
            currentResume={currentResume}
            uploading={uploadMutation.isPending}
            progress={uploadProgress}
            onUpload={(file) => uploadMutation.mutate(file)}
          />
          <JobDescriptionInput
            value={jdText}
            onChange={setJdText}
          />
        </div>


        {/* ==================================================
            ACTIONS
        ================================================== */}

        <div
          className="
            flex
            flex-col
            items-center
            gap-2
          "
        >
          <div
            className="
              flex
              flex-wrap
              justify-center
              gap-3
            "
          >
            <Button
              variant="secondary"
              loading={analyzeMutation.isPending}
              disabled={
                !canRun ||
                analyzeMutation.isPending ||
                optimizeMutation.isPending
              }
              onClick={() => analyzeMutation.mutate()}
            >
              <Sparkles size={16} />
              {analyzeMutation.isPending
                ? "Analyzing..."
                : "Analyze Resume"}
            </Button>
            <Button
              loading={optimizeMutation.isPending}
              disabled={
                !canRun ||
                optimizeMutation.isPending ||
                analyzeMutation.isPending
              }
              onClick={() => optimizeMutation.mutate()}
            >
              <Wand2 size={16} />
              {optimizeMutation.isPending
                ? "Optimizing..."
                : "Optimize Resume"}
            </Button>
          </div>
          {validationMessage && (
            <p className="text-xs text-muted">
              {validationMessage}
            </p>
          )}
        </div>


        {/* ==================================================
            OPTIMIZATION PROGRESS
        ================================================== */}

        {optimizeMutation.isPending && (
          <Card className="p-6 text-center">
            <p className="text-sm font-medium">
              AI is optimizing your resume...
            </p>
            <p className="text-xs text-muted mt-1">
              {
                OPTIMIZE_STEPS[stepIndex]
              }
            </p>
          </Card>
        )}


        {/* ==================================================
            ANALYSIS RESULT
        ================================================== */}

        {analysis && (
          <section className="space-y-5">
            <div>
              <h2 className="text-lg font-semibold">
                Resume Analysis
              </h2>
              <p className="text-sm text-muted">
                How well your resume matches
                this job description.
              </p>
            </div>
            <ScoreCard analysis={analysis} />
            <SkillsMatch analysis={analysis} />
            <div
              className="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-5
              "
            >
              <Strengths items={analysis.strengths} />
              <Weaknesses items={analysis.weaknesses} />
            </div>
            <Recommendations items={analysis.recommendations} />
          </section>
        )}


        {/* ==================================================
            NO ANALYSIS
        ================================================== */}

        {!analysis && (
          <Card>
            <EmptyState
              title="No analysis available."
              description="
                Analyze your resume against the
                job description to see your match score.
              "
            />
          </Card>
        )}



        {optimized && (

          <section className="space-y-5">

            <div className="text-center">

              <h2
                className="
                  text-lg
                  font-semibold
                  text-good
                "
              >

                Resume Optimized Successfully

              </h2>


              <p
                className="
                  text-sm
                  text-muted
                  mt-1
                "
              >

                Your optimized resume is ready
                to review and download.

              </p>

            </div>


            <ResumePreview
              resume={
                optimized.optimized_json
              }
            />


            <ResumeDownload

              versionId={
                optimized.id
              }

            />

          </section>

        )}


        {/* ==================================================
            NO OPTIMIZED RESUME
        ================================================== */}

        {!optimized && (

          <Card>

            <EmptyState

              title="
                Your optimized resume will appear here.
              "

              description="
                Click Optimize Resume after
                uploading your resume and
                adding a job description.
              "

            />

          </Card>

        )}

      </div>

    </AppLayout>

  );

}
