from typing import Optional

from flask_jwt_extended import create_access_token

from app.exceptions.exceptions import MissingAuthData, InvalidCredentials
from app.models import User
from app.models.User import UserRole
from app.repositories import user_repository


def login(email: Optional[str], password: Optional[str]) -> str:
    if email is None or password is None:
        raise MissingAuthData()

    user: Optional[User] = user_repository.get_user_by_email(email)

    if user is None or user.password != password:
        raise InvalidCredentials()

    return create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role.value}
    )


def get_jwt_data(jwt: dict) -> tuple[int, UserRole]:
    user_id: int = int(jwt["sub"])
    role: UserRole = UserRole(jwt.get("role"))

    return user_id, role
