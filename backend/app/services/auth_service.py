# Implements the authentication business logic

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register(db: Session, name: str, email: str, password: str):

        if UserRepository.get_by_email(db, email):
            raise HTTPException(400, "Email already registered")

        user = User(
            name=name,
            email=email,
            hashed_password=hash_password(password)
        )

        return UserRepository.create(db, user)

    @staticmethod
    def login(db: Session, email: str, password: str):

        user = UserRepository.get_by_email(db, email)

        if not user:
            raise HTTPException(401, "Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")

        token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }