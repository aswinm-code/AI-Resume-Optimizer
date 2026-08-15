# stores and retrieves the AI parsed JSON.

from sqlalchemy.orm import Session

from app.models.job_description_profile import JobDescriptionProfile


class JobDescriptionProfileRepository:

    @staticmethod
    def create( db: Session, profile: JobDescriptionProfile):
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_by_job_description_id( db: Session, job_description_id: int):
        return (
            db.query(JobDescriptionProfile)
            .filter(
                JobDescriptionProfile.job_description_id == job_description_id
            )
            .first()
        )