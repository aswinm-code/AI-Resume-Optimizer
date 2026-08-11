from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class JobDescriptionProfile(Base):

    __tablename__ = "job_description_profiles"

    id = Column(Integer, primary_key=True)

    job_description_id = Column(
        Integer,
        ForeignKey(
            "job_descriptions.id",
            ondelete="CASCADE"
        ),
        unique=True,
        nullable=False
    )

    parsed_json = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    job_description = relationship(
        "JobDescription",
        back_populates="profile"
    )