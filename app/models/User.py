from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app import database
from ..utils import get_utc_time


class User(database.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=get_utc_time)
    updated_at = Column(DateTime, nullable=False, default=get_utc_time, onupdate=get_utc_time)