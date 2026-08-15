from sqlalchemy.orm import Session

from app.models.analysis import Analysis


class AnalysisRepository:

    @staticmethod
    def create(db: Session,analysis: Analysis):
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_by_id(db: Session,analysis_id: int):
        return (
            db.query(Analysis)
            .filter(
                Analysis.id == analysis_id
            )
            .first()
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Analysis)
            .join(
                Analysis.resume
            )
            .filter(
                Analysis.resume.has(user_id=user_id)
            )
            .order_by(
                Analysis.created_at.desc()
            )
            .all()
        )