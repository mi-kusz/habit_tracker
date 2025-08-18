from typing import Optional

from sqlalchemy.orm import Session

from app.models import User


def get_users(first_name: Optional[str],
              last_name: Optional[str],
              is_active: Optional[bool]) -> list[User]:
    query = User.query

    if first_name is not None:
        query = query.filter(User.first_name.ilike(f"%{first_name}%"))

    if last_name is not None:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.all()


def get_user_by_id(user_id: int) -> Optional[User]:
    return User.query.get(user_id)


def get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter(User.email == email).first()


def create_user(session: Session, user: User) -> User:
    session.add(user)
    return user


def delete_user(session: Session, user: User) -> User:
    session.delete(user)
    return user
