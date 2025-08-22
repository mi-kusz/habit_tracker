from typing import Optional

from flask_jwt_extended import create_access_token, get_jwt

from app.exceptions.exceptions import MissingAuthDataException, InvalidCredentialsException
from app.models import User
from app.models.User import UserRole
from app.repositories import user_repository


def login(email: Optional[str], password: Optional[str]) -> str:
    if email is None or password is None:
        raise MissingAuthDataException()

    user: Optional[User] = user_repository.get_user_by_email(email)

    if user is None or not user.check_password(password):
        raise InvalidCredentialsException()

    return create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role.value}
    )


def get_jwt_data() -> tuple[int, UserRole]:
    jwt: dict = get_jwt()
    user_id: int = int(jwt["sub"])
    role: UserRole = UserRole(jwt.get("role"))

    return user_id, role
