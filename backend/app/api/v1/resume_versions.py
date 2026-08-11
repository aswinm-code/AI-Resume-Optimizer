from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.resume_version import (
    ResumeVersionResponse
)

from app.services.resume_version_service import (
    ResumeVersionService
)

router = APIRouter(
    prefix="/resume-versions",
    tags=["Resume Versions"]
)


@router.get("/resume/{resume_id}",response_model=list[ResumeVersionResponse])
def get_versions(resume_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    return ResumeVersionService.get_all(
        db,
        current_user.id,
        resume_id
    )


@router.get(
    "/{version_id}",
    response_model=ResumeVersionResponse
)
def get_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ResumeVersionService.get_by_id(
        db,
        current_user.id,
        version_id
    )


@router.delete("/{version_id}")
def delete_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ResumeVersionService.delete(
        db,
        current_user.id,
        version_id
    )