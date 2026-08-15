# Defines request and response models for user APIs.

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UpdateUserRequest(BaseModel):
    name: str