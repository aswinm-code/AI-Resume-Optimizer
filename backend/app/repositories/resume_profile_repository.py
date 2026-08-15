# Handles database operations for parsed resumes.

from sqlalchemy.orm import Session

from app.models.resume_profile import ResumeProfile


class ResumeProfileRepository:

    @staticmethod
    def create( db: Session, resume_profile: ResumeProfile):
        db.add(resume_profile)
        db.commit()
        db.refresh(resume_profile)
        return resume_profile

    @staticmethod
    def get_by_resume_id(
        db: Session,
        resume_id: int
    ):
        return (db.query(ResumeProfile).filter( ResumeProfile.resume_id == resume_id).first()
        )