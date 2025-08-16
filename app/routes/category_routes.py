from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from pydantic import ValidationError

from ..dtos import CategoryReadDTO, CategoryCreateDTO, CategoryUpdateDTO
from ..exceptions import EntityNotFoundException, EntityPersistenceException
from ..services import category_service
from ..utils import create_error_response

category_blueprint = Blueprint("categories", __name__)


@category_blueprint.route("/", methods=["GET"])
def get_categories() -> tuple[Response, HTTPStatus]:
    categories: list[CategoryReadDTO] = category_service.get_categories()
    categories_dicts: list[dict] = [category.model_dump() for category in categories]
    return jsonify(categories_dicts), HTTPStatus.OK


@category_blueprint.route("/<int:category_id>", methods=["GET"])
def get_category_by_id(category_id: int) -> tuple[Response, HTTPStatus]:
    try:
        category: CategoryReadDTO = category_service.get_category_by_id(category_id)

        return jsonify(category.model_dump()), HTTPStatus.OK
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND


@category_blueprint.route("/", methods=["POST"])
def create_category() -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        category_create_dto: CategoryCreateDTO = CategoryCreateDTO(**payload)
        category_read_dto: CategoryReadDTO = category_service.create_category(category_create_dto)

        return jsonify(category_read_dto.model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST


@category_blueprint.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id: int) -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        category_update_dto: CategoryUpdateDTO = CategoryUpdateDTO(**payload)
        category_read_dto: CategoryReadDTO = category_service.update_category(category_id, category_update_dto)

        return jsonify(category_read_dto.model_dump()), HTTPStatus.CREATED
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST