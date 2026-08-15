# Handles user profile logic.

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def get_profile(user: User):
        return user

    @staticmethod
    def update_profile(
        db: Session,
        user: User,
        name: str
    ):
        user.name = name
        return UserRepository.update(db, user)