from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.resume_version import ResumeVersion

from app.schemas.resume_version import ResumeVersionCreate
from app.schemas.parsed_resume import ParsedResume
from app.schemas.parsed_job_description import ParsedJobDescription

from app.repositories.resume_repository import ResumeRepository
from app.repositories.resume_profile_repository import (
    ResumeProfileRepository
)

from app.repositories.job_description_repository import (
    JobDescriptionRepository
)

from app.repositories.job_description_profile_repository import (
    JobDescriptionProfileRepository
)

from app.repositories.resume_version_repository import (
    ResumeVersionRepository
)

from app.services.ai_service import AIService


class ResumeOptimizerService:

    @staticmethod
    def optimize(
        db: Session,
        user_id: int,
        request: ResumeVersionCreate
    ):

        # ---------- Resume ----------

        resume = ResumeRepository.get_by_id(
            db,
            request.resume_id
        )

        if not resume or resume.user_id != user_id:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )

        resume_profile = ResumeProfileRepository.get_by_resume_id(
            db,
            resume.id
        )

        if not resume_profile:
            raise HTTPException(
                status_code=404,
                detail="Resume profile not found"
            )

        # ---------- Job Description ----------

        job_description = JobDescriptionRepository.get_by_id(
            db,
            request.job_description_id
        )

        if (
            not job_description
            or job_description.user_id != user_id
        ):
            raise HTTPException(
                status_code=404,
                detail="Job Description not found"
            )

        job_description_profile = (
            JobDescriptionProfileRepository.get_by_job_description_id(
                db,
                job_description.id
            )
        )

        if not job_description_profile:
            raise HTTPException(
                status_code=404,
                detail="Job Description profile not found"
            )

        parsed_resume = ParsedResume.model_validate(
            resume_profile.parsed_json
        )

        parsed_job_description = ParsedJobDescription.model_validate(
            job_description_profile.parsed_json
        )

        # ---------- AI Optimization ----------

        optimized_resume = AIService.optimize_resume(
            parsed_resume,
            parsed_job_description
        )

        # ---------- Save Version ----------

        version = ResumeVersion(
            resume_id=resume.id,
            job_description_id=job_description.id,
            version_name=request.version_name,
            optimized_json=optimized_resume.model_dump()
        )

        return ResumeVersionRepository.create(
            db,
            version
        )