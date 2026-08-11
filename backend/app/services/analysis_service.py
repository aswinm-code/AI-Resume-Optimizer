# Compare a selected resume with a selected job description and save the analysis.

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.analysis import Analysis

from app.schemas.analysis import AnalysisCreate
from app.schemas.parsed_resume import ParsedResume
from app.schemas.parsed_job_description import ParsedJobDescription

from app.services.ai_service import AIService

from app.repositories.resume_repository import ResumeRepository
from app.repositories.resume_profile_repository import ResumeProfileRepository

from app.repositories.job_description_repository import (
    JobDescriptionRepository
)

from app.repositories.job_description_profile_repository import (
    JobDescriptionProfileRepository
)

from app.repositories.analysis_repository import (
    AnalysisRepository
)


class AnalysisService:

    @staticmethod
    def analyze(db: Session,user_id: int,request: AnalysisCreate):

        # ---------- Resume ----------

        resume = ResumeRepository.get_by_id(db,request.resume_id)

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

        # ---------- Convert JSON -> Pydantic ----------

        parsed_resume = ParsedResume.model_validate(
            resume_profile.parsed_json
        )

        parsed_job_description = ParsedJobDescription.model_validate(
            job_description_profile.parsed_json
        )

        # ---------- AI Analysis ----------

        result = AIService.analyze_resume(parsed_resume,parsed_job_description)

        # ---------- Save Analysis ----------

        analysis = Analysis(
            resume_id=resume.id,
            job_description_id=job_description.id,
            result=result.model_dump()
        )

        analysis = AnalysisRepository.create(
            db,
            analysis
        )

        return analysis