from sqlalchemy import Column, ForeignKey, Integer, DateTime

from app import database
from ..utils import get_utc_time


class ExecutionHistory(database.Model):
    __tablename__ = "execution_histories"

    id = Column(Integer, primary_key=True)
    habit_task_id = Column(Integer, ForeignKey("habit_tasks.id"), nullable=False)
    executed_at = Column(DateTime, default=get_utc_time, nullable=False)