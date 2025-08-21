from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required

from ..dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from ..services import user_service
from ..services.auth_service import get_jwt_data
from ..utils import get_payload

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_users() -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    first_name: Optional[str] = request.args.get("first_name")
    last_name: Optional[str] = request.args.get("last_name")
    is_active: Optional[str] = request.args.get("is_active")

    users: list[UserReadDTO] = user_service.get_users(jwt_user_id, role, first_name, last_name, is_active)
    users_dicts: list[dict] = [user.model_dump() for user in users]
    return jsonify(users_dicts), HTTPStatus.OK


@user_blueprint.route("/id/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    user: UserReadDTO = user_service.get_user_by_id(jwt_user_id, role, user_id)

    return jsonify(user.model_dump()), HTTPStatus.OK


@user_blueprint.route("/email/<email>", methods=["GET"])
@jwt_required()
def get_user_by_email(email: str) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()
    user: UserReadDTO = user_service.get_user_by_email(jwt_user_id, role, email)

    return jsonify(user.model_dump()), HTTPStatus.OK


@user_blueprint.route("/", methods=["POST"])
def create_user() -> tuple[Response, HTTPStatus]:
    payload: dict = get_payload()

    user_create_dto: UserCreateDTO = UserCreateDTO(**payload)
    user_read_dto: UserReadDTO = user_service.create_user(user_create_dto)

    return jsonify(user_read_dto.model_dump()), HTTPStatus.CREATED


@user_blueprint.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    payload: dict = get_payload()

    user_update_dto: UserUpdateDTO = UserUpdateDTO(**payload)
    user_read_dto: UserReadDTO = user_service.update_user(jwt_user_id, role, user_id, user_update_dto)

    return jsonify(user_read_dto.model_dump()), HTTPStatus.OK


@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    user: UserReadDTO = user_service.delete_user(jwt_user_id, role, user_id)

    return jsonify({}), HTTPStatus.NO_CONTENT