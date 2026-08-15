from pydantic import BaseModel, Field


class Experience(BaseModel):

    company: str = ""
    role: str = ""
    duration: str = ""
    location: str = ""
    employment_type: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)

class Education(BaseModel):

    degree: str = ""

    institution: str = ""

    location: str = ""

    year: str = ""

    score: str = ""

class Project(BaseModel):

    title: str = ""

    description: str = ""

    technologies: list[str] = Field(default_factory=list)

    highlights: list[str] = Field(default_factory=list)

class Certification(BaseModel):

    name: str = ""

    issuer: str = ""

    year: str = ""

class TechnicalSkills(BaseModel):

    languages: list[str] = Field(default_factory=list)

    frameworks: list[str] = Field(default_factory=list)

    databases: list[str] = Field(default_factory=list)

    cloud: list[str] = Field(default_factory=list)

    devops: list[str] = Field(default_factory=list)

    tools: list[str] = Field(default_factory=list)

    testing: list[str] = Field(default_factory=list)

    other: list[str] = Field(default_factory=list)

class ParsedResume(BaseModel):

    name: str = ""

    email: str = ""

    phone: str = ""

    linkedin: str = ""

    github: str = ""

    portfolio: str = ""

    location: str = ""

    summary: str = ""

    technical_skills: TechnicalSkills

    experience: list[Experience] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    certifications: list[Certification] = Field(default_factory=list)

    soft_skills: list[str] = Field(default_factory=list)
