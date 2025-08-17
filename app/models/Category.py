from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app import database
from ..utils import get_utc_time


class Category(database.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=get_utc_time, nullable=False)
    updated_at = Column(DateTime, default=get_utc_time, onupdate=get_utc_time, nullable=False)

    user = relationship(
        "User",
        back_populates="categories"
    )

    habit_tasks = relationship(
        "HabitTask",
        back_populates="category",
        cascade="all, delete-orphan"
    )