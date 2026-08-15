from typing import Type, TypeVar

from google import genai
from pydantic import BaseModel

from app.core.config import settings

from app.schemas.parsed_resume import ParsedResume
from app.schemas.parsed_job_description import ParsedJobDescription
from app.schemas.analysis_result import AnalysisResult


client = genai.Client(api_key=settings.GEMINI_API_KEY)

T = TypeVar("T", bound=BaseModel)


class AIService:

    MODEL = "gemini-3.5-flash"

    @staticmethod
    def _generate(
        prompt: str,
        schema: Type[T]
    ) -> T:
        """
        Generate structured JSON directly from Gemini
        and validate it using Pydantic.
        """

        response = client.models.generate_content(
            model=AIService.MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        return response.parsed

    @staticmethod
    def parse_resume(
        text: str
    ) -> ParsedResume:

        prompt = f"""
You are an expert resume parser.

Extract all information from the resume.

Rules

- Do not invent information.
- Missing values should be empty.
- Follow the provided schema.

Resume

{text}
"""

        return AIService._generate(
            prompt,
            ParsedResume
        )

    @staticmethod
    def parse_job_description(
        text: str
    ) -> ParsedJobDescription:

        prompt = f"""
You are an expert recruitment assistant.

Analyze this Job Description.

Rules

- Do not invent information.
- Missing values should be empty.
- Follow the schema.

Job Description

{text}
"""

        return AIService._generate(
            prompt,
            ParsedJobDescription
        )

    @staticmethod
    def analyze_resume(
        resume: ParsedResume,
        job_description: ParsedJobDescription
    ) -> AnalysisResult:

        prompt = f"""
You are an ATS Expert.

Compare the resume with the Job Description.

Rules

- Score from 0 to 100.
- Do not invent experience.
- Only use available information.
- Follow the schema.

Resume

{resume.model_dump_json(indent=2)}

Job Description

{job_description.model_dump_json(indent=2)}
"""

        return AIService._generate(
            prompt,
            AnalysisResult
        )

    @staticmethod
    def optimize_resume(
        resume: ParsedResume,
        job_description: ParsedJobDescription
    ) -> ParsedResume:

        prompt = f"""
You are an expert Resume Writer and ATS Specialist.

Optimize this resume.

STRICT RULES

- Never invent experience.
- Never invent skills.
- Never invent certifications.
- Never invent projects.
- Never change company names.
- Never change job titles.
- Rewrite wording only.
- Improve ATS keywords naturally.
- Rewrite summary.
- Improve bullet points.
- Reorder skills by relevance.
- Keep all factual information.

Resume

{resume.model_dump_json(indent=2)}

Job Description

{job_description.model_dump_json(indent=2)}
"""

        return AIService._generate(
            prompt,
            ParsedResume
        )