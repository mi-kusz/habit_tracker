from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt

from app.exceptions.exceptions import EntityNotFoundException
from app.exceptions.handlers import create_error_response
from ..dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from ..services import user_service
from ..services.auth_service import get_jwt_data

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_users() -> tuple[Response, HTTPStatus]:
    _, role = get_jwt_data(get_jwt())

    if role != "ADMIN":
        raise PermissionError("Forbidden")

    first_name: Optional[str] = request.args.get("first_name")
    last_name: Optional[str] = request.args.get("last_name")
    is_active: Optional[str] = request.args.get("is_active")

    users: list[UserReadDTO] = user_service.get_users(first_name, last_name, is_active)
    users_dicts: list[dict] = [user.model_dump() for user in users]
    return jsonify(users_dicts), HTTPStatus.OK


@user_blueprint.route("/id/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data(get_jwt())

    if not (role == "ADMIN" or jwt_user_id == user_id):
        raise PermissionError("Forbidden")

    user: UserReadDTO = user_service.get_user_by_id(user_id)

    return jsonify(user.model_dump()), HTTPStatus.OK


@user_blueprint.route("/email/<email>", methods=["GET"])
@jwt_required()
def get_user_by_email(email: str) -> tuple[Response, HTTPStatus]:
    role = None
    try:
        user_id, role = get_jwt_data(get_jwt())
        user: UserReadDTO = user_service.get_user_by_email(email)

        if not (role == "ADMIN" or user.id == user_id):
            raise PermissionError("Forbidden")

        return jsonify(user.model_dump()), HTTPStatus.OK
    except (EntityNotFoundException, PermissionError) as e:
        if role == "ADMIN":
            return create_error_response(str(e)), HTTPStatus.NOT_FOUND
        else:
            return create_error_response(str(e)), HTTPStatus.FORBIDDEN


@user_blueprint.route("/", methods=["POST"])
def create_user() -> tuple[Response, HTTPStatus]:
    payload: Optional[dict] = request.get_json()

    if payload is None:
        return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

    user_create_dto: UserCreateDTO = UserCreateDTO(**payload)
    user_read_dto: UserReadDTO = user_service.create_user(user_create_dto)

    return jsonify(user_read_dto.model_dump()), HTTPStatus.CREATED


@user_blueprint.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data(get_jwt())

    if not (role == "ADMIN" or jwt_user_id == user_id):
        raise PermissionError("Forbidden")

    payload: Optional[dict] = request.get_json()

    if payload is None:
        return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

    user_update_dto: UserUpdateDTO = UserUpdateDTO(**payload)
    user_read_dto: UserReadDTO = user_service.update_user(user_id, user_update_dto)

    return jsonify(user_read_dto.model_dump()), HTTPStatus.OK


@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data(get_jwt())

    if not (role == "ADMIN" or jwt_user_id == user_id):
        raise PermissionError("Forbidden")

    user: UserReadDTO = user_service.delete_user(user_id)

    return jsonify(user.model_dump()), HTTPStatus.NO_CONTENT