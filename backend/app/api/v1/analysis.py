from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisResponse
)

from app.services.analysis_service import (
    AnalysisService
)

from app.repositories.analysis_repository import (
    AnalysisRepository
)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.post(
    "",
    response_model=AnalysisResponse
)
def analyze_resume(request: AnalysisCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return AnalysisService.analyze(
        db,
        current_user.id,
        request
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse
)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = AnalysisRepository.get_by_id(
        db,
        analysis_id
    )

    if (
        not analysis
        or analysis.resume.user_id != current_user.id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return analysis


@router.get(
    "",
    response_model=list[AnalysisResponse]
)
def get_all_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AnalysisRepository.get_all_by_user(
        db,
        current_user.id
    )