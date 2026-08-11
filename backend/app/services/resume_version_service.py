from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.resume_version import ResumeVersion

from app.schemas.resume_version import (
    ResumeVersionCreate
)

from app.repositories.resume_repository import (
    ResumeRepository
)

from app.repositories.resume_version_repository import (
    ResumeVersionRepository
)


class ResumeVersionService:

    @staticmethod
    def get_all(db: Session,user_id: int,resume_id: int
    ):

        resume = ResumeRepository.get_by_id(
            db,
            resume_id
        )

        if not resume or resume.user_id != user_id:
            raise HTTPException(
                404,
                "Resume not found"
            )

        return ResumeVersionRepository.get_all_by_resume(
            db,
            resume_id
        )

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
        version_id: int
    ):

        version = ResumeVersionRepository.get_by_id(
            db,
            version_id
        )

        if (
            not version
            or version.resume.user_id != user_id
        ):
            raise HTTPException(
                404,
                "Version not found"
            )

        return version

    @staticmethod
    def delete(
        db: Session,
        user_id: int,
        version_id: int
    ):

        version = ResumeVersionRepository.get_by_id(
            db,
            version_id
        )

        if (
            not version
            or version.resume.user_id != user_id
        ):
            raise HTTPException(
                404,
                "Version not found"
            )

        ResumeVersionRepository.delete(
            db,
            version
        )

        return {
            "message": "Version deleted successfully"
        }