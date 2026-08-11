# Handles all database operations for job_descriptions.

from sqlalchemy.orm import Session

from app.models.job_description import JobDescription


class JobDescriptionRepository:

    @staticmethod
    def create(
        db: Session,
        job_description: JobDescription
    ):
        db.add(job_description)
        db.commit()
        db.refresh(job_description)
        return job_description

    @staticmethod
    def get_by_id(db: Session,job_description_id: int):
        return (
            db.query(JobDescription)
            .filter(
                JobDescription.id == job_description_id
            )
            .first()
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int
    ):
        return (
            db.query(JobDescription)
            .filter(
                JobDescription.user_id == user_id
            )
            .order_by(JobDescription.created_at.desc())
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        job_description: JobDescription
    ):
        db.delete(job_description)
        db.commit()