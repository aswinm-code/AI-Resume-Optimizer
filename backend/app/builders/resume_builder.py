import os
from pathlib import Path
from typing import Callable

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor

from app.schemas.parsed_resume import ParsedResume

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

EXPORT_DIR = "app/exports/resumes"


class ATSResumeBuilder:

    @staticmethod
    def build(resume: ParsedResume,filename: str) -> str:

        Path(EXPORT_DIR).mkdir(parents=True,exist_ok=True)

        document = Document()

        ATSResumeBuilder._set_default_style(document)
        ATSResumeBuilder._set_page(document)

        ATSResumeBuilder._header(document, resume)

        sections = [
            ("Professional Summary", ATSResumeBuilder._summary),
            ("Skills", ATSResumeBuilder._skills),
            ("Professional Experience", ATSResumeBuilder._experience),
            ("Projects", ATSResumeBuilder._projects),
            ("Education", ATSResumeBuilder._education),
            ("Certifications", ATSResumeBuilder._certifications),
        ]

        for title, builder in sections:

            ATSResumeBuilder._section(document=document,title=title,resume=resume,builder=builder
        )

        output_path = os.path.join(
            EXPORT_DIR,
            filename
        )

        document.save(output_path)

        return output_path

    @staticmethod
    def _set_default_style(
        document: Document
    ):

        style = document.styles["Normal"]

        style.font.name = "Calibri"
        style.font.size = Pt(11)
        style.font.color.rgb = RGBColor(0, 0, 0)

    @staticmethod
    def _set_page(document: Document):

        section = document.sections[0]

        section.top_margin = Pt(36)
        section.bottom_margin = Pt(36)
        section.left_margin = Pt(36)
        section.right_margin = Pt(36)

    @staticmethod
    def _heading(document: Document,title: str):

        p = document.add_paragraph()

        p.space_before = Pt(10)
        p.space_after = Pt(4)

        run = p.add_run(title.upper())

        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 0, 0)

        ATSResumeBuilder._add_bottom_border(p)

    @staticmethod
    def _section(
        document: Document,
        title: str,
        resume: ParsedResume,
        builder: Callable
    ):

        ATSResumeBuilder._heading(
            document,
            title
        )

        builder(
            document,
            resume
        )

    @staticmethod
    def _header(document: Document,resume: ParsedResume):

        # Name
        p = document.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        run = p.add_run(resume.name.upper())

        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(20)
        run.font.color.rgb = RGBColor(0, 0, 0)

        # Contact Information
        contact = document.add_paragraph()
        contact.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        values = []

        if resume.email:
            values.append(resume.email)

        if resume.phone:
            values.append(resume.phone)

        if getattr(resume, "linkedin", None):
            values.append(resume.linkedin)

        if getattr(resume, "github", None):
            values.append(resume.github)

        contact_run = contact.add_run(" | ".join(values))

        contact_run.font.name = "Calibri"
        contact_run.font.size = Pt(10)
        contact_run.font.color.rgb = RGBColor(0, 0, 0)

    @staticmethod
    def _summary(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.summary:
            return

        paragraph = document.add_paragraph()

        paragraph.add_run(
            resume.summary
        )

    @staticmethod
    def _skills(document: Document,resume: ParsedResume):

        skills = resume.technical_skills

        categories = {
            "Languages": skills.languages,
            "Frameworks": skills.frameworks,
            "Databases": skills.databases,
            "Cloud": skills.cloud,
            "DevOps": skills.devops,
            "Tools": skills.tools,
            "Testing": skills.testing,
            "Others": skills.other,
        }

        for category, values in categories.items():

            if not values:
                continue

            paragraph = document.add_paragraph()

            title = paragraph.add_run(
                f"{category}: "
            )

            title.bold = True
            title.font.name = "Calibri"
            title.font.size = Pt(11)
            title.font.color.rgb = RGBColor(0, 0, 0)

            value = paragraph.add_run(
                ", ".join(values)
            )

            value.font.name = "Calibri"
            value.font.size = Pt(11)
            value.font.color.rgb = RGBColor(0, 0, 0)

    @staticmethod
    def _experience(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.experience:
            return

        for exp in resume.experience:

            # Role | Company
            title = document.add_paragraph()

            role = title.add_run(exp.role)

            role.bold = True
            role.font.name = "Calibri"
            role.font.size = Pt(11)
            role.font.color.rgb = RGBColor(0, 0, 0)

            if exp.company:
                company = title.add_run(f" | {exp.company}")

                company.font.name = "Calibri"
                company.font.size = Pt(11)
                company.font.color.rgb = RGBColor(0, 0, 0)

            # Duration
            if exp.duration:

                duration = document.add_paragraph()

                run = duration.add_run(exp.duration)

                run.italic = True
                run.font.name = "Calibri"
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)

            # Description
            for point in exp.description:

                bullet = document.add_paragraph(
                    style="List Bullet"
                )

                run = bullet.add_run(point)

                run.font.name = "Calibri"
                run.font.size = Pt(11)
                run.font.color.rgb = RGBColor(0, 0, 0)

    @staticmethod
    def _projects(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.projects:
            return

        for project in resume.projects:

            # Project Title
            title = document.add_paragraph()

            run = title.add_run(project.title)

            run.bold = True
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)

            # Description
            if project.description:

                description = document.add_paragraph()

                desc = description.add_run(
                    project.description
                )

                desc.font.name = "Calibri"
                desc.font.size = Pt(11)
                desc.font.color.rgb = RGBColor(0, 0, 0)

            # Technologies
            if project.technologies:

                tech = document.add_paragraph()

                heading = tech.add_run(
                    "Technologies: "
                )

                heading.bold = True
                heading.font.name = "Calibri"
                heading.font.size = Pt(11)
                heading.font.color.rgb = RGBColor(0, 0, 0)

                value = tech.add_run(
                    ", ".join(project.technologies)
                )

                value.font.name = "Calibri"
                value.font.size = Pt(11)
                value.font.color.rgb = RGBColor(0, 0, 0)


    @staticmethod
    def _education(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.education:
            return

        for edu in resume.education:

            paragraph = document.add_paragraph()

            # Degree
            degree = paragraph.add_run(
                edu.degree
            )

            degree.bold = True
            degree.font.name = "Calibri"
            degree.font.size = Pt(11)
            degree.font.color.rgb = RGBColor(0, 0, 0)

            # Institution
            if edu.institution:

                institution = paragraph.add_run(
                    f"\n{edu.institution}"
                )

                institution.font.name = "Calibri"
                institution.font.size = Pt(11)
                institution.font.color.rgb = RGBColor(0, 0, 0)

            # Year
            if edu.year:

                year = paragraph.add_run(
                    f"\n{edu.year}"
                )

                year.font.name = "Calibri"
                year.font.size = Pt(10)
                year.font.color.rgb = RGBColor(0, 0, 0)

    @staticmethod
    def _certifications(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.certifications:
            return

        for cert in resume.certifications:

            bullet = document.add_paragraph(
                style="List Bullet"
            )

            text = cert.name

            if cert.issuer:
                text += f" ({cert.issuer})"

            if getattr(cert, "year", None):
                text += f" - {cert.year}"

            run = bullet.add_run(text)

            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)

    @staticmethod
    def _add_bottom_border(paragraph):

        pPr = paragraph._p.get_or_add_pPr()

        pBdr = OxmlElement("w:pBdr")

        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "12")        # Line thickness
        bottom.set(qn("w:space"), "3")     # Space from text
        bottom.set(qn("w:color"), "000000")

        pBdr.append(bottom)

        pPr.append(pBdr)