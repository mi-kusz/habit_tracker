from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.dtos import UserCreateDTO, UserReadDTO, UserUpdateDTO
from app.exceptions.exceptions import EntityPersistenceException, EntityNotFoundException
from app.models import User, Category
from app.models.User import UserRole
from app.repositories import user_repository, category_repository
from app.utils import str_to_bool_or_none

entity_type: str = "User"


def get_users(requester_id: int,
              requester_role: UserRole,
              first_name: Optional[str],
              last_name: Optional[str],
              is_active: Optional[str]) -> list[UserReadDTO]:
    if requester_role != UserRole.ADMIN:
        raise PermissionError("Forbidden")

    is_active_bool: Optional[bool] = str_to_bool_or_none(is_active)

    users: list[User] = user_repository.get_users(first_name, last_name, is_active_bool)

    return [UserReadDTO.model_validate(user) for user in users]


def get_user_by_id(requester_id: int,
                   requester_role: UserRole,
                   user_id: int) -> UserReadDTO:
    if requester_role != UserRole.ADMIN and requester_id != user_id:
        raise PermissionError("Forbidden")

    user: User = get_user_entity_by_id(user_id)

    return UserReadDTO.model_validate(user)


def get_user_by_email(requester_id: int,
                      requester_role: UserRole,
                      email: str) -> UserReadDTO:
    # Security note: normal users get 403 even if email doesn't exist,
    # so they cannot probe the database for valid emails.
    try:
        user: User = get_user_entity_by_email(email)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    if requester_role != UserRole.ADMIN and requester_id != user.id:
        raise PermissionError("Forbidden")

    return UserReadDTO.model_validate(user)


def create_user(user_dto: UserCreateDTO) -> UserReadDTO:
    user: User = convert_dto_to_model(user_dto)

    try:
        with database.session.begin():
            created_user: User = user_repository.create_user(database.session, user)
            database.session.flush()
            _created_category: Category = category_repository.create_default_category_for_user(database.session, created_user.id)

        return UserReadDTO.model_validate(created_user)
    except IntegrityError:
        raise EntityPersistenceException(entity_type)


def update_user(requester_id: int,
                requester_role: UserRole,
                user_id: int,
                user_updates: UserUpdateDTO) -> UserReadDTO:
    if requester_role != UserRole.ADMIN and requester_id != user_id:
        raise PermissionError("Forbidden")

    updates: dict = user_updates.model_dump(exclude_unset=True)

    try:
        with database.session.begin():
            user: User = get_user_entity_by_id(user_id)

            for field, value in updates.items():
                if hasattr(user, field):
                    setattr(user, field, value)
    except IntegrityError:
        raise EntityPersistenceException(entity_type)

    return UserReadDTO.model_validate(user)


def delete_user(requester_id: int,
                requester_role: UserRole,
                user_id: int) -> UserReadDTO:
    if requester_role != UserRole.ADMIN and requester_id != user_id:
        raise PermissionError("Forbidden")

    with database.session.begin():
        user: User = get_user_entity_by_id(user_id)

        user_repository.delete_user(database.session, user)

    return UserReadDTO.model_validate(user)


def convert_dto_to_model(user_dto: UserCreateDTO) -> User:
    user: User = User(
        first_name=user_dto.first_name,
        last_name=user_dto.last_name,
        email=user_dto.email,
        role=user_dto.role or UserRole.USER
    )

    user.set_password(user_dto.password)

    return user


def get_user_entity_by_id(user_id: int) -> User:
    user: Optional[User] = user_repository.get_user_by_id(user_id)

    if user is None:
        raise EntityNotFoundException(entity_type)

    return user


def get_user_entity_by_email(email: str) -> User:
    user: Optional[User] = user_repository.get_user_by_email(email)

    if user is None:
        raise EntityNotFoundException(entity_type)

    return user