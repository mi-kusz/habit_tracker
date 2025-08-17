from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from pydantic import ValidationError

from ..dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from ..exceptions import EntityNotFoundException, EntityPersistenceException
from ..services import execution_history_service
from ..utils import create_error_response


execution_history_blueprint = Blueprint("execution_histories", __name__)


@execution_history_blueprint.route("/", methods=["GET"])
def get_execution_histories() -> tuple[Response, HTTPStatus]:
    execution_histories: list[ExecutionHistoryReadDTO] = execution_history_service.get_execution_histories()
    execution_histories_dicts: list[dict] = [execution_history.model_dump() for execution_history in execution_histories]

    return jsonify(execution_histories_dicts), HTTPStatus.OK


@execution_history_blueprint.route("/<int:execution_history_id>", methods=["GET"])
def get_execution_history_by_id(execution_history_id: int) -> tuple[Response, HTTPStatus]:
    try:
        execution_history: ExecutionHistoryReadDTO = execution_history_service.get_execution_history_by_id(execution_history_id)

        return jsonify(execution_history.model_dump()), HTTPStatus.OK
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND


@execution_history_blueprint.route("/", methods=["POST"])
def create_execution_history() -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        execution_history_dto: ExecutionHistoryCreateDTO = ExecutionHistoryCreateDTO(**payload)
        execution_history_read_dto: ExecutionHistoryReadDTO = execution_history_service.create_execution_history(execution_history_dto)

        return jsonify(execution_history_read_dto.model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST


@execution_history_blueprint.route("/<int:execution_history_id>", methods=["DELETE"])
def delete_execution_history(execution_history_id: int) -> tuple[Response, HTTPStatus]:
    try:
        execution_history: ExecutionHistoryReadDTO = execution_history_service.delete_execution_history(execution_history_id)

        return jsonify(execution_history.model_dump()), HTTPStatus.NO_CONTENT
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND