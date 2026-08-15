# Resume ORM model

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

# will use for extracting pdf/resume
from sqlalchemy import Text

from sqlalchemy.orm import relationship

class Resume(BaseModel):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    original_filename = Column(String, nullable=False)

    stored_filename = Column(String, nullable=False)

    file_type = Column(String(20), nullable=False)

    file_size = Column(BigInteger, nullable=False)

    user = relationship(
        "User",
        back_populates="resumes"
    )
    extracted_text = Column(Text,nullable=True)
    profile = relationship(
    "ResumeProfile",
    back_populates="resume",
    uselist=False,
    cascade="all, delete-orphan"
)