import enum

import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship

from app import database
from ..utils import get_utc_time


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(database.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(DateTime, nullable=False, default=get_utc_time)
    updated_at = Column(DateTime, nullable=False, default=get_utc_time, onupdate=get_utc_time)

    categories = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, plain_password: str) -> None:
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), self.hashed_password.encode("utf-8"))
