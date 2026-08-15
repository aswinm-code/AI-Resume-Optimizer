from pydantic import BaseModel


class AnalysisResult(BaseModel):

    overall_score: int

    skills_score: int

    experience_score: int

    education_score: int

    projects_score: int

    matched_skills: list[str]

    missing_skills: list[str]

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]