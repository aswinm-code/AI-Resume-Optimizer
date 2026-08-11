from sqlalchemy.orm import Session

from app.models.resume_version import ResumeVersion


class ResumeVersionRepository:

    @staticmethod
    def create(
        db: Session,
        version: ResumeVersion
    ):
        db.add(version)
        db.commit()
        db.refresh(version)
        return version

    @staticmethod
    def get_by_id(
        db: Session,
        version_id: int
    ):
        return (
            db.query(ResumeVersion)
            .filter(
                ResumeVersion.id == version_id
            )
            .first()
        )

    @staticmethod
    def get_all_by_resume(
        db: Session,
        resume_id: int
    ):
        return (
            db.query(ResumeVersion)
            .filter(
                ResumeVersion.resume_id == resume_id
            )
            .order_by(
                ResumeVersion.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        version: ResumeVersion
    ):
        db.delete(version)
        db.commit()