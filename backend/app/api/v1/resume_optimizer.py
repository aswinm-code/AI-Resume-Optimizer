from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.resume_version import (
    ResumeVersionCreate,
    ResumeVersionResponse
)

from app.services.resume_optimizer_service import (
    ResumeOptimizerService
)

router = APIRouter(
    prefix="/resume-optimizer",
    tags=["Resume Optimizer"]
)


@router.post(
    "",
    response_model=ResumeVersionResponse
)
def optimize_resume(
    request: ResumeVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ResumeOptimizerService.optimize(
        db=db,
        user_id=current_user.id,
        request=request
    )