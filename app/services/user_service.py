from app.dtos import UserCreateDTO, UserReadDTO, UserUpdateDTO
from app.models import User
from app.repositories import user_repository


def get_users() -> list[UserReadDTO]:
    users: list[User] = user_repository.get_users()

    return [UserReadDTO.model_validate(user) for user in users]


def get_user_by_id(user_id: int) -> UserReadDTO:
    user: User = user_repository.get_user_by_id(user_id)

    return UserReadDTO.model_validate(user)


def create_user(user_dto: UserCreateDTO) -> UserReadDTO:
    user: User = convert_dto_to_model(user_dto)

    created_user: User = user_repository.create_user(user)

    return UserReadDTO.model_validate(created_user)


def update_user(user_id: int, user_updates: UserUpdateDTO) -> UserReadDTO:
    user: User = user_repository.get_user_by_id(user_id)

    if user_updates.first_name is not None:
        user.first_name = user_updates.first_name

    if user_updates.last_name is not None:
        user.last_name = user_updates.last_name

    if user_updates.email is not None:
        user.email = user_updates.email

    if user_updates.is_active is not None:
        user.is_active = user_updates.is_active

    updated_user: User = user_repository.update_user(user)

    return UserReadDTO.model_validate(updated_user)


def convert_dto_to_model(user_dto: UserCreateDTO) -> User:
    return User(
        first_name=user_dto.first_name,
        last_name=user_dto.last_name,
        email=user_dto.email,
        password=user_dto.password
    )