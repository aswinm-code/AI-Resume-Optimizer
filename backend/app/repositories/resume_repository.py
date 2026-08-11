# Contains database operations for resumes.

from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    @staticmethod
    def create(db: Session, resume: Resume):
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def get_all_by_user(db: Session, user_id: int):
        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, resume_id: int):
        return (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

    @staticmethod
    def delete(db: Session, resume: Resume):
        db.delete(resume)
        db.commit()