from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from pydantic import ValidationError

from ..dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from ..exceptions import EntityNotFoundException, EntityPersistenceException
from ..services import user_service
from ..utils import create_error_response

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/", methods=["GET"])
def get_users() -> tuple[Response, HTTPStatus]:
    try:
        first_name: Optional[str] = request.args.get("first_name")
        last_name: Optional[str] = request.args.get("last_name")
        is_active: Optional[str] = request.args.get("is_active")

        users: list[UserReadDTO] = user_service.get_users(first_name, last_name, is_active)
        users_dicts: list[dict] = [user.model_dump() for user in users]
        return jsonify(users_dicts), HTTPStatus.OK
    except ValueError as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST


@user_blueprint.route("/id/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int) -> tuple[Response, HTTPStatus]:
    try:
        user: UserReadDTO = user_service.get_user_by_id(user_id)

        return jsonify(user.model_dump()), HTTPStatus.OK
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND


@user_blueprint.route("/email/<email>", methods=["GET"])
def get_user_by_email(email: str) -> tuple[Response, HTTPStatus]:
    try:
        user: UserReadDTO = user_service.get_user_by_email(email)

        return jsonify(user.model_dump()), HTTPStatus.OK
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND


@user_blueprint.route("/", methods=["POST"])
def create_user() -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        user_create_dto: UserCreateDTO = UserCreateDTO(**payload)
        user_read_dto: UserReadDTO = user_service.create_user(user_create_dto)

        return jsonify(user_read_dto.model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST


@user_blueprint.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        user_update_dto: UserUpdateDTO = UserUpdateDTO(**payload)
        user_read_dto: UserReadDTO = user_service.update_user(user_id, user_update_dto)

        return jsonify(user_read_dto.model_dump()), HTTPStatus.OK
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST


@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> tuple[Response, HTTPStatus]:
    try:
        user: UserReadDTO = user_service.delete_user(user_id)

        return jsonify(user.model_dump()), HTTPStatus.NO_CONTENT
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND