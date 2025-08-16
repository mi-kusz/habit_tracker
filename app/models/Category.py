from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from app import database
from ..utils import get_utc_time


class Category(database.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=get_utc_time, nullable=False)
    updated_at = Column(DateTime, default=get_utc_time, onupdate=get_utc_time, nullable=False)
