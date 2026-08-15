from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.job_description import (
    JobDescriptionCreate,
    JobDescriptionResponse
)

from app.services.job_description_service import (
    JobDescriptionService
)

router = APIRouter(
    prefix="/job-descriptions",
    tags=["Job Descriptions"]
)


@router.post(
    "",
    response_model=JobDescriptionResponse
)
def create_job_description(request: JobDescriptionCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return JobDescriptionService.create(
        db,
        current_user.id,
        request
    )


@router.get(
    "",
    response_model=list[JobDescriptionResponse]
)
def get_job_descriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobDescriptionService.get_all(
        db,
        current_user.id
    )


@router.delete(
    "/{job_description_id}"
)
def delete_job_description(
    job_description_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobDescriptionService.delete(
        db,
        current_user.id,
        job_description_id
    )