from pydantic import BaseModel


class ParsedJobDescription(BaseModel):

    title: str

    experience_required: str

    skills: list[str]

    responsibilities: list[str]

    qualifications: list[str]

    preferred_skills: list[str]

    technologies: list[str]

    keywords: list[str]