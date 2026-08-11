import React from "react";
import type { OptimizedResume } from "@/types";
import { Card } from "@/components/common/ui";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-5">
      <h4 className="text-xs font-bold uppercase tracking-wide text-ink border-b border-ink/70 pb-1 mb-2.5">
        {title}
      </h4>
      {children}
    </div>
  );
}

export function ResumePreview({ resume }: { resume: OptimizedResume }) {
  const contactLine = [resume.email, resume.phone, resume.linkedin, resume.github].filter(Boolean).join(" | ");

  const skillItems = [
    ...resume.technical_skills.languages,
    ...resume.technical_skills.frameworks,
    ...resume.technical_skills.databases,
    ...resume.technical_skills.cloud,
    ...resume.technical_skills.devops,
    ...resume.technical_skills.tools,
    ...resume.technical_skills.testing,
    ...resume.technical_skills.other,
  ].filter(Boolean);

  return (
    <Card className="p-8 sm:p-10 max-w-3xl mx-auto font-sans text-sm text-ink leading-relaxed">
      <div className="text-center mb-6">
        {resume.name && <h1 className="text-xl font-bold uppercase tracking-wide">{resume.name}</h1>}
        {contactLine && <p className="text-xs text-muted mt-1">{contactLine}</p>}
      </div>

      {resume.summary && (
        <Section title="Professional Summary">
          <p>{resume.summary}</p>
        </Section>
      )}

      {skillItems.length > 0 && (
        <Section title="Skills">
          <p>{skillItems.join(" · ")}</p>
        </Section>
      )}

      {resume.experience && resume.experience.length > 0 && (
        <Section title="Professional Experience">
          <div className="space-y-4">
            {resume.experience.map((exp, i) => (
              <div key={i}>
                <div className="flex items-baseline justify-between flex-wrap gap-x-3">
                  <span className="font-semibold">{exp.company}</span>
                  {exp.duration && <span className="text-xs text-muted">{exp.duration}</span>}
                </div>
                <p className="italic text-xs text-muted mb-1">{exp.role}</p>
                <ul className="list-disc list-outside pl-4 space-y-0.5">
                  {exp.description.map((desc, j) => (
                    <li key={j}>{desc}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </Section>
      )}

      {resume.projects && resume.projects.length > 0 && (
        <Section title="Projects">
          <div className="space-y-4">
            {resume.projects.map((project, i) => (
              <div key={i}>
                <p className="font-semibold">{project.title}</p>
                {project.description && <p className="text-sm text-muted">{project.description}</p>}
                {project.technologies && project.technologies.length > 0 && (
                  <p className="text-xs text-muted">{project.technologies.join(" · ")}</p>
                )}
              </div>
            ))}
          </div>
        </Section>
      )}

      {resume.education && resume.education.length > 0 && (
        <Section title="Education">
          <ul className="space-y-0.5">
            {resume.education.map((item, i) => (
              <li key={i}>
                {item.degree} at {item.institution}
                {item.year ? ` · ${item.year}` : ""}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {resume.certifications && resume.certifications.length > 0 && (
        <Section title="Certifications">
          <ul className="list-disc list-outside pl-4 space-y-0.5">
            {resume.certifications.map((cert, i) => (
              <li key={i}>
                {cert.name}
                {cert.issuer ? ` · ${cert.issuer}` : ""}
                {cert.year ? ` · ${cert.year}` : ""}
              </li>
            ))}
          </ul>
        </Section>
      )}
    </Card>
  );
}
