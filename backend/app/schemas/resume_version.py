from datetime import datetime

from pydantic import BaseModel


class ResumeVersionCreate(BaseModel):

    resume_id: int

    job_description_id: int

    version_name: str


class ResumeVersionResponse(BaseModel):

    id: int

    resume_id: int

    job_description_id: int

    version_name: str

    optimized_json: dict

    created_at: datetime

    class Config:
        from_attributes = True