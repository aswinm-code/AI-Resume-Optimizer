from pydantic import BaseModel, Field


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    location: str = ""
    description: list[str] = Field(default_factory=list)

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


# from pydantic import BaseModel


# class Experience(BaseModel):
#     company: str
#     role: str
#     duration: str
#     description: list[str]


# class Education(BaseModel):
#     degree: str
#     institution: str
#     year: str


# class Project(BaseModel):
#     title: str
#     description: str
#     technologies: list[str]


# class ParsedResume(BaseModel):
#     name: str
#     email: str
#     phone: str
#     summary: str
#     skills: list[str]
#     experience: list[Experience]
#     education: list[Education]
#     projects: list[Project]
#     certifications: list[str]
