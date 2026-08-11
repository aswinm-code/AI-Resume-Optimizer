# Handles the complete Job Description workflow

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.job_description import JobDescription
from app.models.job_description_profile import JobDescriptionProfile

from app.schemas.job_description import JobDescriptionCreate

from app.services.ai_service import AIService

from app.repositories.job_description_repository import (
    JobDescriptionRepository
)

from app.repositories.job_description_profile_repository import (
    JobDescriptionProfileRepository
)


class JobDescriptionService:

    @staticmethod
    def create(db: Session,user_id: int,request: JobDescriptionCreate):

        # Save Original Job Description
        job_description = JobDescription(
            user_id=user_id,
            title=request.title,
            description=request.description
        )

        job_description = JobDescriptionRepository.create( db, job_description)

        # Parse using AI
        parsed_job_description = AIService.parse_job_description(
            request.description
        )

        # Save Parsed JSON
        JobDescriptionProfileRepository.create(
            db,
            JobDescriptionProfile(
                job_description_id=job_description.id,
                parsed_json=parsed_job_description.model_dump()
            )
        )

        return job_description

    @staticmethod
    def get_all(
        db: Session,
        user_id: int
    ):

        return JobDescriptionRepository.get_all_by_user(
            db,
            user_id
        )

    @staticmethod
    def delete(
        db: Session,
        user_id: int,
        job_description_id: int
    ):

        job_description = JobDescriptionRepository.get_by_id(
            db,
            job_description_id
        )

        if (
            not job_description
            or job_description.user_id != user_id
        ):
            raise HTTPException(
                status_code=404,
                detail="Job Description not found"
            )

        JobDescriptionRepository.delete(
            db,
            job_description
        )

        return {
            "message": "Job Description deleted successfully"
        }