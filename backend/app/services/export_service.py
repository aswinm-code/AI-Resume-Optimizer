import os

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.builders.resume_builder import ATSResumeBuilder
from app.repositories.resume_version_repository import (
    ResumeVersionRepository
)
from app.schemas.parsed_resume import ParsedResume


EXPORT_DIR = "app/exports/resumes"


class ExportService:

    # ==========================================================
    # EXPORT DOCX
    # ==========================================================

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

        # ------------------------------------------------------
        # Verify ownership
        # ------------------------------------------------------

        if version.resume.user_id != user_id:

            raise HTTPException(
                status_code=403,
                detail="Access denied."
            )

        # ------------------------------------------------------
        # Create export directory
        # ------------------------------------------------------

        os.makedirs(
            EXPORT_DIR,
            exist_ok=True
        )

        filename = (
            f"version_{version.id}.docx"
        )

        output_path = os.path.join(
            EXPORT_DIR,
            filename
        )

        # ------------------------------------------------------
        # Return existing DOCX
        # ------------------------------------------------------

        if os.path.exists(output_path):

            return {
                "file_name": filename,
                "file_path": output_path
            }

        # ------------------------------------------------------
        # Convert optimized JSON → ParsedResume
        # ------------------------------------------------------

        resume = ParsedResume.model_validate(
            version.optimized_json
        )

        # ------------------------------------------------------
        # Generate DOCX
        # ------------------------------------------------------

        generated_path = ATSResumeBuilder.build(
            resume=resume,
            filename=filename
        )

        return {
            "file_name": filename,
            "file_path": generated_path
        }

    # ==========================================================
    # EXPORT PDF
    # ==========================================================

    @staticmethod
    def export_pdf(
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

        # ------------------------------------------------------
        # Verify ownership
        # ------------------------------------------------------

        if version.resume.user_id != user_id:

            raise HTTPException(
                status_code=403,
                detail="Access denied."
            )

        # ------------------------------------------------------
        # Create export directory
        # ------------------------------------------------------

        os.makedirs(
            EXPORT_DIR,
            exist_ok=True
        )

        filename = (
            f"version_{version.id}.pdf"
        )

        output_path = os.path.join(
            EXPORT_DIR,
            filename
        )

        # ------------------------------------------------------
        # Return existing PDF
        # ------------------------------------------------------

        if os.path.exists(output_path):

            return {
                "file_name": filename,
                "file_path": output_path
            }

        # ------------------------------------------------------
        # Convert optimized JSON → ParsedResume
        # ------------------------------------------------------

        resume = ParsedResume.model_validate(
            version.optimized_json
        )

        # ------------------------------------------------------
        # Generate DOCX + PDF
        # ------------------------------------------------------

        generated_pdf = ATSResumeBuilder.build_pdf(
            resume=resume,
            filename=filename
        )

        return {
            "file_name": filename,
            "file_path": generated_pdf
        }