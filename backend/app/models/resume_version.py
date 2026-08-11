from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    JSON,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ResumeVersion(Base):

    __tablename__ = "resume_versions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    job_description_id = Column(
        Integer,
        ForeignKey(
            "job_descriptions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    version_name = Column(
        String(100),
        nullable=False
    )

    optimized_json = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    resume = relationship("Resume")

    job_description = relationship("JobDescription")