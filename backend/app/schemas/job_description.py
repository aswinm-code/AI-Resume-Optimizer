# Validate API request and response

from datetime import datetime

from pydantic import BaseModel




class JobDescriptionCreate(BaseModel):
    title: str | None = None
    description: str


class JobDescriptionResponse(BaseModel):
    id: int
    title: str | None
    description: str
    created_at: datetime

    class Config:
        from_attributes = True