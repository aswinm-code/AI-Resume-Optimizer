import os

from docx2pdf import convert
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.builders.resume_builder import ATSResumeBuilder
from app.repositories.resume_version_repository import (
    ResumeVersionRepository
)
from app.schemas.parsed_resume import ParsedResume


EXPORT_DIR = "app/exports/resumes"


class ExportService:

    @staticmethod
    def export_docx(
        db: Session,
        user_id: int,
        version_id: int
    ):

        version = ResumeVersionRepository.get_by_id(
            db,
            version_id
        )

        if not version:
            raise HTTPException(
                status_code=404,
                detail="Resume version not found."
            )

        if version.resume.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied."
            )

        os.makedirs(
            EXPORT_DIR,
            exist_ok=True
        )

        filename = f"version_{version.id}.docx"

        output_path = os.path.join(
            EXPORT_DIR,
            filename
        )

        # Return existing file
        if os.path.exists(output_path):
            return output_path

        resume = ParsedResume.model_validate(
            version.optimized_json
        )

        ATSResumeBuilder.build(
            resume,
            filename
        )

        return {
            "file_name": f"version_{version.id}.docx",
            "file_path": output_path
            }

    @staticmethod
    def export_pdf(
        db: Session,
        user_id: int,
        version_id: int
    ):

        docx_path = ExportService.export_docx(
            db,
            user_id,
            version_id
        )

        pdf_path = docx_path.replace(
            ".docx",
            ".pdf"
        )

        # Return existing PDF
        if os.path.exists(pdf_path):
            return pdf_path

        convert(
            docx_path,
            pdf_path
        )

        return pdf_path