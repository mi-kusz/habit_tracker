from typing import Optional

from sqlalchemy.orm import Session

from app.models import User


def get_users() -> list[User]:
    return User.query.all()


def get_user_by_id(user_id: int) -> Optional[User]:
    return User.query.get(user_id)


def create_user(session: Session, user: User) -> User:
    session.add(user)
    return user