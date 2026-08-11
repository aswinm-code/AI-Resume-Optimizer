# Defines the response model for resume APIs

from datetime import datetime

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    original_filename: str
    file_type: str
    file_size: int
    created_at: datetime

    class Config:
        from_attributes = True