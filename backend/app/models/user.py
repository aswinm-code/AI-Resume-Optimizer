# User ORM model

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    hashed_password = Column(String, nullable=False)

    resumes = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan"
    )