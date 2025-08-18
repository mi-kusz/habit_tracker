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


def delete_user(session: Session, user: User) -> User:
    session.delete(user)
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter(User.email.ilike(email)).first()


def get_users_by_names(session: Session, first_name: Optional[str], last_name: Optional[str]) -> list[User]:
    query = session.query(User)

    if first_name is not None:
        query = query.filter(User.first_name.ilike(f"%{first_name}%"))

    if last_name is not None:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))

    return query.all()


def get_active_users(session: Session, is_active: bool = True) -> list[User]:
    return session.query(User).filter(User.is_active == is_active).all()