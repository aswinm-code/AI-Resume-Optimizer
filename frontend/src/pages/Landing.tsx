import React from "react";
import { Link } from "react-router-dom";
import { FileText, Target, Sparkles, FileCheck, Download } from "lucide-react";
import { Button, Card } from "@/components/common/ui";

const features = [
  { icon: Sparkles, title: "AI Resume Analysis", desc: "Get an instant read on how well your resume fits a role." },
  { icon: Target, title: "Job Match Score", desc: "See a clear score across skills, experience, and education." },
  { icon: FileText, title: "AI Resume Optimization", desc: "Let AI rewrite key sections to better match the job." },
  { icon: FileCheck, title: "ATS-Friendly Export", desc: "Clean, single-column formatting built for applicant tracking systems." },
  { icon: Download, title: "DOCX & PDF Download", desc: "Export your optimized resume in the format you need." },
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-canvas">
      <header className="border-b border-line bg-surface">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-md bg-accent flex items-center justify-center">
              <FileText size={15} className="text-white" />
            </div>
            <span className="font-semibold text-sm">Resume Optimizer</span>
          </div>
          <Link to="/login" className="text-sm font-medium text-muted hover:text-ink">
            Login
          </Link>
        </div>
      </header>

      <section className="max-w-3xl mx-auto text-center px-6 pt-20 pb-16">
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-ink">
          Optimize Your Resume for Every Job
        </h1>
        <p className="text-muted text-base sm:text-lg mt-5 leading-relaxed">
          Upload your resume, paste a job description, and see exactly how well you match — then let AI
          generate a tailored, ATS-friendly version ready to download.
        </p>
        <div className="flex items-center justify-center gap-3 mt-8">
          <Link to="/register">
            <Button size="md">Get Started</Button>
          </Link>
          <Link to="/login">
            <Button variant="secondary" size="md">
              Login
            </Button>
          </Link>
        </div>
      </section>

      <section className="max-w-5xl mx-auto px-6 pb-24">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f) => (
            <Card key={f.title} className="p-6">
              <f.icon size={20} className="text-accent mb-3" />
              <h3 className="text-sm font-semibold mb-1">{f.title}</h3>
              <p className="text-sm text-muted leading-relaxed">{f.desc}</p>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
