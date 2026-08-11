from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.services.export_service import ExportService


router = APIRouter(
    prefix="/export",
    tags=["Resume Export"]
)


@router.get("/docx/{version_id}")
def download_docx(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    file_path = ExportService.export_docx(
        db=db,
        user_id=current_user.id,
        version_id=version_id
    )

    return FileResponse(
        path=file_path,
        filename=f"resume_{version_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.get("/pdf/{version_id}")
def download_pdf(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    file_path = ExportService.export_pdf(
        db=db,
        user_id=current_user.id,
        version_id=version_id
    )

    return FileResponse(
        path=file_path,
        filename=f"resume_{version_id}.pdf",
        media_type="application/pdf"
    )