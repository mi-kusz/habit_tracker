from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import User

entity_type: str = "User"


def get_users() -> list[User]:
    return User.query.all()


def get_user_by_id(user_id: int) -> User:
    user: Optional[User] = User.query.get(user_id)

    if user is None:
        raise EntityNotFoundException(entity_type)

    return user


def create_user(user: User) -> User:
    try:
        database.session.add(user)
        database.session.commit()
        return user
    except IntegrityError:
        database.session.rollback()
        raise EntityPersistenceException(entity_type)


def update_user(user: User) -> User:
    try:
        database.session.commit()
        return user
    except IntegrityError:
        database.session.rollback()
        raise EntityPersistenceException(entity_type)
