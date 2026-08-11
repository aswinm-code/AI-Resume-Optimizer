# Stores the original job description entered by the user.

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class JobDescription(Base):

    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(Text, nullable=True)

    description = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    profile = relationship(
        "JobDescriptionProfile",
        back_populates="job_description",
        uselist=False,
        cascade="all, delete-orphan"
    )