from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)

    class Config:
        extra = "ignore"
        from_attributes = True


class CategoryCreateDTO(CategoryBaseDTO):
    user_id: int


class CategoryReadDTO(CategoryBaseDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class CategoryUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
