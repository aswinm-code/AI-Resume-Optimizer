# API routes for resume operations

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


@router.post("/upload",response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await ResumeService.upload(
        db,
        current_user.id,
        file
    )


@router.get(
    "",
    response_model=list[ResumeResponse]
)
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ResumeService.get_all(
        db,
        current_user.id
    )


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ResumeService.delete(
        db,
        current_user.id,
        resume_id
    )