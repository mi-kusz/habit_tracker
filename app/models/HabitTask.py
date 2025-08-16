from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from app import database
from ..utils import get_utc_time


class HabitTask(database.Model):
    __tablename__ = "habit_tasks"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=get_utc_time, nullable=False)
    updated_at = Column(DateTime, default=get_utc_time, onupdate=get_utc_time, nullable=False)