# API routes for authentication
# Exposes authentication endpoints to the client

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    return AuthService.register(
        db,
        request.name,
        request.email,
        request.password
    )


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db,
        form_data.username,
        form_data.password
    )