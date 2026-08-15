# API routes for user management
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.user import (
    UserResponse,
    UpdateUserRequest
)

from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me",response_model=UserResponse)
def profile(current_user: User = Depends(get_current_user)):
    return UserService.get_profile(current_user)


@router.put( "/me", response_model=UserResponse)
def update_profile(request: UpdateUserRequest,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return UserService.update_profile(
        db,
        current_user,
        request.name
    )