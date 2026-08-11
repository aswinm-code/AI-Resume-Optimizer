from datetime import datetime

from pydantic import BaseModel


class AnalysisCreate(BaseModel):

    resume_id: int

    job_description_id: int


class AnalysisResponse(BaseModel):

    id: int

    resume_id: int

    job_description_id: int

    result: dict

    created_at: datetime

    class Config:
        from_attributes = True