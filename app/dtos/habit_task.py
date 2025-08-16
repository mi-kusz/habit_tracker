from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HabitTaskBaseDTO(BaseModel):
    category_id: int
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)

    class Config:
        extra = "ignore"
        from_attributes = True


class HabitTaskCreateDTO(HabitTaskBaseDTO):
    pass


class HabitTaskReadDTO(HabitTaskBaseDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class HabitTaskUpdateDTO(BaseModel):
    category_id: Optional[int]
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
