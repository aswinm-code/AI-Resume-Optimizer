import os
import subprocess
from pathlib import Path
from typing import Callable

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from app.schemas.parsed_resume import ParsedResume


EXPORT_DIR = Path("app/exports/resumes")

BLACK = RGBColor(0, 0, 0)

FONT_NAME = "Calibri"
BODY_SIZE = 11
HEADING_SIZE = 13
NAME_SIZE = 20
CONTACT_SIZE = 10


class ATSResumeBuilder:

    # ==========================================================
    # PUBLIC METHODS
    # ==========================================================

    @staticmethod
    def build(
        resume: ParsedResume,
        filename: str
    ) -> str:

        EXPORT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        document = Document()

        ATSResumeBuilder._set_default_style(document)
        ATSResumeBuilder._set_page(document)

        # Header
        ATSResumeBuilder._header(
            document,
            resume
        )

        # Resume sections
        sections = [
            (
                "Professional Summary",
                ATSResumeBuilder._summary
            ),
            (
                "Skills",
                ATSResumeBuilder._skills
            ),
            (
                "Professional Experience",
                ATSResumeBuilder._experience
            ),
            (
                "Projects",
                ATSResumeBuilder._projects
            ),
            (
                "Education",
                ATSResumeBuilder._education
            ),
            (
                "Certifications",
                ATSResumeBuilder._certifications
            ),
        ]

        for title, builder in sections:

            ATSResumeBuilder._section(
                document=document,
                title=title,
                resume=resume,
                builder=builder
            )

        output_path = EXPORT_DIR / filename

        document.save(output_path)

        return str(output_path)

    @staticmethod
    def build_pdf(
        resume: ParsedResume,
        filename: str
    ) -> str:

        """
        Generates DOCX first and converts it to PDF
        using LibreOffice.

        Works on Linux, Windows and Docker as long as
        LibreOffice is installed.
        """

        # ------------------------------------------------------
        # Generate DOCX
        # ------------------------------------------------------

        docx_filename = Path(filename).with_suffix(".docx").name

        docx_path = ATSResumeBuilder.build(
            resume=resume,
            filename=docx_filename
        )

        docx_path = Path(docx_path)

        # ------------------------------------------------------
        # PDF output directory
        # ------------------------------------------------------

        pdf_dir = docx_path.parent

        # ------------------------------------------------------
        # Convert DOCX -> PDF using LibreOffice
        # ------------------------------------------------------

        command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(pdf_dir),
            str(docx_path),
        ]

        try:

            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )

        except FileNotFoundError:

            raise RuntimeError(
                "LibreOffice is not installed or "
                "not available in PATH."
            )

        except subprocess.CalledProcessError as exc:

            raise RuntimeError(
                f"LibreOffice PDF conversion failed: "
                f"{exc.stderr}"
            )

        # ------------------------------------------------------
        # Expected PDF path
        # ------------------------------------------------------

        pdf_path = pdf_dir / (
            docx_path.stem + ".pdf"
        )

        if not pdf_path.exists():

            raise RuntimeError(
                "PDF conversion completed but "
                "the PDF file was not created."
            )

        return str(pdf_path)

    # ==========================================================
    # DOCUMENT CONFIGURATION
    # ==========================================================

    @staticmethod
    def _set_default_style(
        document: Document
    ):

        style = document.styles["Normal"]

        style.font.name = FONT_NAME
        style.font.size = Pt(BODY_SIZE)
        style.font.color.rgb = BLACK

    @staticmethod
    def _set_page(
        document: Document
    ):

        section = document.sections[0]

        section.top_margin = Pt(36)
        section.bottom_margin = Pt(36)
        section.left_margin = Pt(36)
        section.right_margin = Pt(36)

    # ==========================================================
    # SECTION HANDLING
    # ==========================================================

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
    def _heading(
        document: Document,
        title: str
    ):

        paragraph = document.add_paragraph()

        paragraph.paragraph_format.space_before = Pt(10)
        paragraph.paragraph_format.space_after = Pt(4)

        run = paragraph.add_run(
            title.upper()
        )

        run.bold = True
        run.font.name = FONT_NAME
        run.font.size = Pt(HEADING_SIZE)
        run.font.color.rgb = BLACK

        # Full-width black underline
        ATSResumeBuilder._add_bottom_border(
            paragraph
        )

    # ==========================================================
    # HEADER
    # ==========================================================

    @staticmethod
    def _header(
        document: Document,
        resume: ParsedResume
    ):

        # ------------------------------------------------------
        # Name
        # ------------------------------------------------------

        paragraph = document.add_paragraph()

        paragraph.alignment = (
            WD_PARAGRAPH_ALIGNMENT.CENTER
        )

        run = paragraph.add_run(
            resume.name.upper()
        )

        run.bold = True
        run.font.name = FONT_NAME
        run.font.size = Pt(NAME_SIZE)
        run.font.color.rgb = BLACK

        # ------------------------------------------------------
        # Contact information
        # ------------------------------------------------------

        contact = document.add_paragraph()

        contact.alignment = (
            WD_PARAGRAPH_ALIGNMENT.CENTER
        )

        values = []

        if resume.email:
            values.append(resume.email)

        if resume.phone:
            values.append(resume.phone)

        if getattr(resume, "linkedin", None):
            values.append(resume.linkedin)

        if getattr(resume, "github", None):
            values.append(resume.github)

        if not values:
            return

        run = contact.add_run(
            " | ".join(values)
        )

        run.font.name = FONT_NAME
        run.font.size = Pt(CONTACT_SIZE)
        run.font.color.rgb = BLACK

    # ==========================================================
    # PROFESSIONAL SUMMARY
    # ==========================================================

    @staticmethod
    def _summary(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.summary:
            return

        paragraph = document.add_paragraph()

        run = paragraph.add_run(
            resume.summary
        )

        ATSResumeBuilder._body_font(run)

    # ==========================================================
    # SKILLS
    # ==========================================================

    @staticmethod
    def _skills(
        document: Document,
        resume: ParsedResume
    ):

        skills = resume.technical_skills

        if not skills:
            return

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

            # Category
            title = paragraph.add_run(
                f"{category}: "
            )

            title.bold = True
            ATSResumeBuilder._body_font(title)

            # Skills
            value = paragraph.add_run(
                ", ".join(values)
            )

            ATSResumeBuilder._body_font(value)

    # ==========================================================
    # PROFESSIONAL EXPERIENCE
    # ==========================================================

    @staticmethod
    def _experience(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.experience:
            return

        for exp in resume.experience:

            # --------------------------------------------------
            # Role | Company
            # --------------------------------------------------

            title = document.add_paragraph()

            role = title.add_run(
                exp.role
            )

            role.bold = True
            ATSResumeBuilder._body_font(role)

            if exp.company:

                company = title.add_run(
                    f" | {exp.company}"
                )

                ATSResumeBuilder._body_font(
                    company
                )

            # --------------------------------------------------
            # Duration
            # --------------------------------------------------

            if exp.duration:

                duration = document.add_paragraph()

                run = duration.add_run(
                    exp.duration
                )

                run.italic = True
                run.font.name = FONT_NAME
                run.font.size = Pt(CONTACT_SIZE)
                run.font.color.rgb = BLACK

            # --------------------------------------------------
            # Responsibilities
            # --------------------------------------------------

            for point in exp.description:

                if not point:
                    continue

                bullet = document.add_paragraph(
                    style="List Bullet"
                )

                run = bullet.add_run(
                    point
                )

                ATSResumeBuilder._body_font(
                    run
                )

    # ==========================================================
    # PROJECTS
    # ==========================================================

    @staticmethod
    def _projects(
        document: Document,
        resume: ParsedResume
    ):

        if not resume.projects:
            return

        for project in resume.projects:

            # Project title
            title = document.add_paragraph()

            run = title.add_run(
                project.title
            )

            run.bold = True

            ATSResumeBuilder._body_font(
                run
            )

            # Description
            if project.description:

                description = document.add_paragraph()

                run = description.add_run(
                    project.description
                )

                ATSResumeBuilder._body_font(
                    run
                )

            # Technologies
            if project.technologies:

                technologies = document.add_paragraph()

                label = technologies.add_run(
                    "Technologies: "
                )

                label.bold = True

                ATSResumeBuilder._body_font(
                    label
                )

                values = technologies.add_run(
                    ", ".join(
                        project.technologies
                    )
                )

                ATSResumeBuilder._body_font(
                    values
                )

    # ==========================================================
    # EDUCATION
    # ==========================================================

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
            if edu.degree:

                degree = paragraph.add_run(
                    edu.degree
                )

                degree.bold = True

                ATSResumeBuilder._body_font(
                    degree
                )

            # Institution
            if edu.institution:

                institution = paragraph.add_run(
                    f"\n{edu.institution}"
                )

                ATSResumeBuilder._body_font(
                    institution
                )

            # Year
            if edu.year:

                year = paragraph.add_run(
                    f"\n{edu.year}"
                )

                year.font.name = FONT_NAME
                year.font.size = Pt(CONTACT_SIZE)
                year.font.color.rgb = BLACK

    # ==========================================================
    # CERTIFICATIONS
    # ==========================================================

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

            run = bullet.add_run(
                text
            )

            ATSResumeBuilder._body_font(
                run
            )

    # ==========================================================
    # FONT HELPER
    # ==========================================================

    @staticmethod
    def _body_font(run):

        run.font.name = FONT_NAME
        run.font.size = Pt(BODY_SIZE)
        run.font.color.rgb = BLACK

    # ==========================================================
    # FULL-WIDTH HEADING BORDER
    # ==========================================================

    @staticmethod
    def _add_bottom_border(
        paragraph
    ):

        p = paragraph._p

        pPr = p.get_or_add_pPr()

        # Remove existing paragraph borders
        existing = pPr.find(
            qn("w:pBdr")
        )

        if existing is not None:

            pPr.remove(existing)

        # Create paragraph border
        pBdr = OxmlElement("w:pBdr")

        bottom = OxmlElement("w:bottom")

        bottom.set(
            qn("w:val"),
            "single"
        )

        bottom.set(
            qn("w:sz"),
            "8"
        )

        bottom.set(
            qn("w:space"),
            "3"
        )

        bottom.set(
            qn("w:color"),
            "000000"
        )

        pBdr.append(bottom)

        pPr.append(pBdr)



# import os
# from pathlib import Path
# from typing import Callable

# from docx import Document
# from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
# from docx.shared import Pt, RGBColor

# from app.schemas.parsed_resume import ParsedResume

# from docx.oxml import OxmlElement
# from docx.oxml.ns import qn

# EXPORT_DIR = "app/exports/resumes"


# class ATSResumeBuilder:

#     @staticmethod
#     def build(resume: ParsedResume,filename: str) -> str:

#         Path(EXPORT_DIR).mkdir(parents=True,exist_ok=True)

#         document = Document()

#         ATSResumeBuilder._set_default_style(document)
#         ATSResumeBuilder._set_page(document)

#         ATSResumeBuilder._header(document, resume)

#         sections = [
#             ("Professional Summary", ATSResumeBuilder._summary),
#             ("Skills", ATSResumeBuilder._skills),
#             ("Professional Experience", ATSResumeBuilder._experience),
#             ("Projects", ATSResumeBuilder._projects),
#             ("Education", ATSResumeBuilder._education),
#             ("Certifications", ATSResumeBuilder._certifications),
#         ]

#         for title, builder in sections:

#             ATSResumeBuilder._section(document=document,title=title,resume=resume,builder=builder
#         )

#         output_path = os.path.join(
#             EXPORT_DIR,
#             filename
#         )

#         document.save(output_path)

#         return output_path

#     @staticmethod
#     def _set_default_style(
#         document: Document
#     ):

#         style = document.styles["Normal"]

#         style.font.name = "Calibri"
#         style.font.size = Pt(11)
#         style.font.color.rgb = RGBColor(0, 0, 0)

#     @staticmethod
#     def _set_page(document: Document):

#         section = document.sections[0]

#         section.top_margin = Pt(36)
#         section.bottom_margin = Pt(36)
#         section.left_margin = Pt(36)
#         section.right_margin = Pt(36)

#     @staticmethod
#     def _heading(document: Document,title: str):

#         p = document.add_paragraph()

#         p.space_before = Pt(10)
#         p.space_after = Pt(4)

#         run = p.add_run(title.upper())

#         run.bold = True
#         run.font.name = "Calibri"
#         run.font.size = Pt(13)
#         run.font.color.rgb = RGBColor(0, 0, 0)

#         ATSResumeBuilder._add_bottom_border(p)

#     @staticmethod
#     def _section(
#         document: Document,
#         title: str,
#         resume: ParsedResume,
#         builder: Callable
#     ):

#         ATSResumeBuilder._heading(
#             document,
#             title
#         )

#         builder(
#             document,
#             resume
#         )

#     @staticmethod
#     def _header(document: Document,resume: ParsedResume):

#         # Name
#         p = document.add_paragraph()
#         p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

#         run = p.add_run(resume.name.upper())

#         run.bold = True
#         run.font.name = "Calibri"
#         run.font.size = Pt(20)
#         run.font.color.rgb = RGBColor(0, 0, 0)

#         # Contact Information
#         contact = document.add_paragraph()
#         contact.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

#         values = []

#         if resume.email:
#             values.append(resume.email)

#         if resume.phone:
#             values.append(resume.phone)

#         if getattr(resume, "linkedin", None):
#             values.append(resume.linkedin)

#         if getattr(resume, "github", None):
#             values.append(resume.github)

#         contact_run = contact.add_run(" | ".join(values))

#         contact_run.font.name = "Calibri"
#         contact_run.font.size = Pt(10)
#         contact_run.font.color.rgb = RGBColor(0, 0, 0)

#     @staticmethod
#     def _summary(
#         document: Document,
#         resume: ParsedResume
#     ):

#         if not resume.summary:
#             return

#         paragraph = document.add_paragraph()

#         paragraph.add_run(
#             resume.summary
#         )

#     @staticmethod
#     def _skills(document: Document,resume: ParsedResume):

#         skills = resume.technical_skills

#         categories = {
#             "Languages": skills.languages,
#             "Frameworks": skills.frameworks,
#             "Databases": skills.databases,
#             "Cloud": skills.cloud,
#             "DevOps": skills.devops,
#             "Tools": skills.tools,
#             "Testing": skills.testing,
#             "Others": skills.other,
#         }

#         for category, values in categories.items():

#             if not values:
#                 continue

#             paragraph = document.add_paragraph()

#             title = paragraph.add_run(
#                 f"{category}: "
#             )

#             title.bold = True
#             title.font.name = "Calibri"
#             title.font.size = Pt(11)
#             title.font.color.rgb = RGBColor(0, 0, 0)

#             value = paragraph.add_run(
#                 ", ".join(values)
#             )

#             value.font.name = "Calibri"
#             value.font.size = Pt(11)
#             value.font.color.rgb = RGBColor(0, 0, 0)

#     @staticmethod
#     def _experience(
#         document: Document,
#         resume: ParsedResume
#     ):

#         if not resume.experience:
#             return

#         for exp in resume.experience:

#             # Role | Company
#             title = document.add_paragraph()

#             role = title.add_run(exp.role)

#             role.bold = True
#             role.font.name = "Calibri"
#             role.font.size = Pt(11)
#             role.font.color.rgb = RGBColor(0, 0, 0)

#             if exp.company:
#                 company = title.add_run(f" | {exp.company}")

#                 company.font.name = "Calibri"
#                 company.font.size = Pt(11)
#                 company.font.color.rgb = RGBColor(0, 0, 0)

#             # Duration
#             if exp.duration:

#                 duration = document.add_paragraph()

#                 run = duration.add_run(exp.duration)

#                 run.italic = True
#                 run.font.name = "Calibri"
#                 run.font.size = Pt(10)
#                 run.font.color.rgb = RGBColor(0, 0, 0)

#             # Description
#             for point in exp.description:

#                 bullet = document.add_paragraph(
#                     style="List Bullet"
#                 )

#                 run = bullet.add_run(point)

#                 run.font.name = "Calibri"
#                 run.font.size = Pt(11)
#                 run.font.color.rgb = RGBColor(0, 0, 0)

#     @staticmethod
#     def _projects(
#         document: Document,
#         resume: ParsedResume
#     ):

#         if not resume.projects:
#             return

#         for project in resume.projects:

#             # Project Title
#             title = document.add_paragraph()

#             run = title.add_run(project.title)

#             run.bold = True
#             run.font.name = "Calibri"
#             run.font.size = Pt(11)
#             run.font.color.rgb = RGBColor(0, 0, 0)

#             # Description
#             if project.description:

#                 description = document.add_paragraph()

#                 desc = description.add_run(
#                     project.description
#                 )

#                 desc.font.name = "Calibri"
#                 desc.font.size = Pt(11)
#                 desc.font.color.rgb = RGBColor(0, 0, 0)

#             # Technologies
#             if project.technologies:

#                 tech = document.add_paragraph()

#                 heading = tech.add_run(
#                     "Technologies: "
#                 )

#                 heading.bold = True
#                 heading.font.name = "Calibri"
#                 heading.font.size = Pt(11)
#                 heading.font.color.rgb = RGBColor(0, 0, 0)

#                 value = tech.add_run(
#                     ", ".join(project.technologies)
#                 )

#                 value.font.name = "Calibri"
#                 value.font.size = Pt(11)
#                 value.font.color.rgb = RGBColor(0, 0, 0)


#     @staticmethod
#     def _education(
#         document: Document,
#         resume: ParsedResume
#     ):

#         if not resume.education:
#             return

#         for edu in resume.education:

#             paragraph = document.add_paragraph()

#             # Degree
#             degree = paragraph.add_run(
#                 edu.degree
#             )

#             degree.bold = True
#             degree.font.name = "Calibri"
#             degree.font.size = Pt(11)
#             degree.font.color.rgb = RGBColor(0, 0, 0)

#             # Institution
#             if edu.institution:

#                 institution = paragraph.add_run(
#                     f"\n{edu.institution}"
#                 )

#                 institution.font.name = "Calibri"
#                 institution.font.size = Pt(11)
#                 institution.font.color.rgb = RGBColor(0, 0, 0)

#             # Year
#             if edu.year:

#                 year = paragraph.add_run(
#                     f"\n{edu.year}"
#                 )

#                 year.font.name = "Calibri"
#                 year.font.size = Pt(10)
#                 year.font.color.rgb = RGBColor(0, 0, 0)

#     @staticmethod
#     def _certifications(
#         document: Document,
#         resume: ParsedResume
#     ):

#         if not resume.certifications:
#             return

#         for cert in resume.certifications:

#             bullet = document.add_paragraph(
#                 style="List Bullet"
#             )

#             text = cert.name

#             if cert.issuer:
#                 text += f" ({cert.issuer})"

#             if getattr(cert, "year", None):
#                 text += f" - {cert.year}"

#             run = bullet.add_run(text)

#             run.font.name = "Calibri"
#             run.font.size = Pt(11)
#             run.font.color.rgb = RGBColor(0, 0, 0)

#     @staticmethod
#     def _add_bottom_border(paragraph):

#         pPr = paragraph._p.get_or_add_pPr()

#         pBdr = OxmlElement("w:pBdr")

#         bottom = OxmlElement("w:bottom")
#         bottom.set(qn("w:val"), "single")
#         bottom.set(qn("w:sz"), "12")        # Line thickness
#         bottom.set(qn("w:space"), "3")     # Space from text
#         bottom.set(qn("w:color"), "000000")

#         pBdr.append(bottom)

#         pPr.append(pBdr)