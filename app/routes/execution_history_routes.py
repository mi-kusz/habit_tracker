from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response

from app.exceptions.handlers import create_error_response
from ..dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from ..services import execution_history_service

execution_history_blueprint = Blueprint("execution_histories", __name__)


@execution_history_blueprint.route("/", methods=["GET"])
def get_execution_histories() -> tuple[Response, HTTPStatus]:
    habit_task_id: Optional[str] = request.args.get("habit_task_id")
    start_datetime: Optional[str] = request.args.get("start_datetime")
    end_datetime: Optional[str] = request.args.get("end_datetime")

    execution_histories: list[ExecutionHistoryReadDTO] = execution_history_service.get_execution_histories(habit_task_id, start_datetime, end_datetime)
    execution_histories_dicts: list[dict] = [execution_history.model_dump() for execution_history in execution_histories]

    return jsonify(execution_histories_dicts), HTTPStatus.OK


@execution_history_blueprint.route("/<int:execution_history_id>", methods=["GET"])
def get_execution_history_by_id(execution_history_id: int) -> tuple[Response, HTTPStatus]:
    execution_history: ExecutionHistoryReadDTO = execution_history_service.get_execution_history_by_id(execution_history_id)

    return jsonify(execution_history.model_dump()), HTTPStatus.OK


@execution_history_blueprint.route("/", methods=["POST"])
def create_execution_history() -> tuple[Response, HTTPStatus]:
    payload: Optional[dict] = request.get_json()

    if payload is None:
        return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

    execution_history_dto: ExecutionHistoryCreateDTO = ExecutionHistoryCreateDTO(**payload)
    execution_history_read_dto: ExecutionHistoryReadDTO = execution_history_service.create_execution_history(execution_history_dto)

    return jsonify(execution_history_read_dto.model_dump()), HTTPStatus.CREATED


@execution_history_blueprint.route("/<int:execution_history_id>", methods=["DELETE"])
def delete_execution_history(execution_history_id: int) -> tuple[Response, HTTPStatus]:
    execution_history: ExecutionHistoryReadDTO = execution_history_service.delete_execution_history(execution_history_id)

    return jsonify(execution_history.model_dump()), HTTPStatus.NO_CONTENT