from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required

from ..dtos import CategoryReadDTO, CategoryCreateDTO, CategoryUpdateDTO
from ..services import category_service
from ..services.auth_service import get_jwt_data
from ..utils import get_payload

category_blueprint = Blueprint("categories", __name__)


@category_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_categories() -> tuple[Response, HTTPStatus]:
    user_id: Optional[str] = request.args.get("user_id")
    name: Optional[str] = request.args.get("name")

    jwt_user_id, role = get_jwt_data()

    categories: list[CategoryReadDTO] = category_service.get_categories(jwt_user_id, role, user_id, name)
    categories_dicts: list[dict] = [category.model_dump() for category in categories]

    return jsonify(categories_dicts), HTTPStatus.OK


@category_blueprint.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category_by_id(category_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    category: CategoryReadDTO = category_service.get_category_by_id(jwt_user_id, role, category_id)

    return jsonify(category.model_dump()), HTTPStatus.OK


@category_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_category() -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    payload: dict = get_payload()

    category_create_dto: CategoryCreateDTO = CategoryCreateDTO(**payload)
    category_read_dto: CategoryReadDTO = category_service.create_category(jwt_user_id, role, category_create_dto)

    return jsonify(category_read_dto.model_dump()), HTTPStatus.CREATED


@category_blueprint.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    payload: dict = get_payload()

    category_update_dto: CategoryUpdateDTO = CategoryUpdateDTO(**payload)
    category_read_dto: CategoryReadDTO = category_service.update_category(jwt_user_id, role, category_id, category_update_dto)

    return jsonify(category_read_dto.model_dump()), HTTPStatus.OK


@category_blueprint.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    category: CategoryReadDTO = category_service.delete_category(jwt_user_id, role, category_id)

    return jsonify({}), HTTPStatus.NO_CONTENT