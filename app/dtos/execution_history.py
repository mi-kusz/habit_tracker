from datetime import datetime

from pydantic import BaseModel


class ExecutionHistoryBaseDTO(BaseModel):
    habit_task_id: int
    executed_at: datetime

    class Config:
        extra = "ignore"
        from_attributes = True


class ExecutionHistoryCreateDTO(ExecutionHistoryBaseDTO):
    pass


class ExecutionHistoryReadDTO(ExecutionHistoryBaseDTO):
    id: int
