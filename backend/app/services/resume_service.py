# Handles resume upload, retrieval, and deletion logic.

import os
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository

from app.services.parser_service import ParserService
from app.services.ai_service import AIService
from app.models.resume_profile import ResumeProfile

from app.repositories.resume_profile_repository import (ResumeProfileRepository)



UPLOAD_DIR = "app/uploads"


class ResumeService:

    @staticmethod
    async def upload( db: Session, user_id: int, file: UploadFile):

        extension = file.filename.split(".")[-1]

        stored_filename = f"{uuid.uuid4()}.{extension}"

        file_path = os.path.join( UPLOAD_DIR, stored_filename)
        

        content = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        text = ParserService.extract_text(file_path)
        parsed_resume = AIService.parse_resume(text)
        resume = Resume(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_type=file.content_type,
            file_size=len(content),
            extracted_text=text
        )

        resume = ResumeRepository.create(db, resume)
        ResumeProfileRepository.create(db,ResumeProfile(resume_id=resume.id,parsed_json=parsed_resume.model_dump()))
        return resume
    

    @staticmethod
    def get_all(
        db: Session,
        user_id: int
    ):
        return ResumeRepository.get_all_by_user(
            db,
            user_id
        )

    @staticmethod
    def delete( db: Session, user_id: int, resume_id: int):

        resume = ResumeRepository.get_by_id(db,resume_id)

        if not resume or resume.user_id != user_id:
            raise HTTPException(
                404,
                "Resume not found"
            )

        file_path = os.path.join(
            UPLOAD_DIR,
            resume.stored_filename
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        ResumeRepository.delete(db, resume)

        return {
            "message": "Resume deleted successfully"
        }