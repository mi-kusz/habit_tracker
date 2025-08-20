from datetime import datetime
from typing import Optional

from app.models.User import UserRole

from pydantic import BaseModel, EmailStr, Field


class UserBaseDTO(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

    class Config:
        extra = "ignore"
        from_attributes = True


class UserCreateDTO(UserBaseDTO):
    password: str = Field(..., min_length=1)
    role: Optional[UserRole] = None


class UserReadDTO(UserBaseDTO):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateDTO(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
