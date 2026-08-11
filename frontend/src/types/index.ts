// src/types/index.ts

// ============================================================
// AUTHENTICATION
// ============================================================

export interface User {
  id: number;
  name: string;
  email: string;
  username?: string;
}


// ============================================================
// RESUME - PARSED STRUCTURE
// Matches backend ParsedResume schema
// ============================================================

export interface TechnicalSkills {
  languages: string[];
  frameworks: string[];
  databases: string[];
  cloud: string[];
  devops: string[];
  tools: string[];
  testing: string[];
  other: string[];
}

export interface Experience {
  company: string;
  role: string;
  duration: string;
  description: string[];
}

export interface Education {
  degree: string;
  institution: string;
  year: string;
}

export interface Project {
  title: string;
  description: string;
  technologies: string[];
}

export interface Certification {
  name: string;
  issuer: string;
  year?: string;
}

export interface ParsedResume {
  name: string;
  email: string;
  phone: string;

  summary: string;

  technical_skills: TechnicalSkills;

  experience: Experience[];

  education: Education[];

  projects: Project[];

  certifications: Certification[];

  // Optional contact information.
  // These are supported by the frontend if your backend
  // schema contains them.
  linkedin?: string;
  github?: string;
}


// ============================================================
// RESUME RECORD
// Represents the uploaded resume stored by the backend
// ============================================================

export interface Resume {
  id: number;
  filename: string;

  uploaded_at?: string;

  parsed_json?: ParsedResume;
}


// ============================================================
// JOB DESCRIPTION
// Matches backend ParsedJobDescription schema
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


// ============================================================
// JOB DESCRIPTION RECORD
// If your backend stores the JD in the database
// ============================================================

export interface JobDescription {
  id: number;

  title?: string;

  description: string;

  parsed_json?: ParsedJobDescription;

  created_at?: string;
}


// ============================================================
// RESUME ANALYSIS
// Matches backend AnalysisResult schema
// ============================================================

export interface AnalysisResult {
  id?: number;

  resume_id?: number;

  job_description_id?: number;

  overall_score: number;

  skills_score: number;

  experience_score: number;

  education_score: number;

  projects_score: number;

  matched_skills: string[];

  missing_skills: string[];

  strengths: string[];

  weaknesses: string[];

  recommendations: string[];
}


// ============================================================
// OPTIMIZED RESUME
// The AI optimizer returns the same basic structure as
// ParsedResume because optimization rewrites the resume,
// rather than creating a completely different structure.
// ============================================================

export interface OptimizedResume extends ParsedResume {
  id?: number;

  resume_id?: number;

  job_description_id?: number;

  version_id?: number;
}


// ============================================================
// OPTIMIZATION RESPONSE
// Use this if ResumeOptimizerService returns a wrapper
// around the optimized resume.
// ============================================================

export interface OptimizeResumeResponse {
  version_id?: number;

  resume_id?: number;

  job_description_id?: number;

  resume: OptimizedResume;
}

export interface ResumeVersionResponse {
  id: number;

  resume_id: number;

  job_description_id?: number;

  version_name: string;

  optimized_json: OptimizedResume;

  created_at?: string;
}


// ============================================================
// RESUME VERSION
// Used by DOCX / PDF export
// ============================================================

export interface ResumeVersion {
  id: number;

  resume_id: number;

  job_description_id?: number;

  version_number?: number;

  resume_data?: ParsedResume;

  created_at?: string;
}


// ============================================================
// API ERROR
// Common structure for frontend error handling
// ============================================================

export interface ApiError {
  detail?: string;

  message?: string;
}


// ============================================================
// API RESPONSE HELPERS
// ============================================================

export interface AuthResponse {
  access_token: string;

  token_type: string;

  user?: User;
}