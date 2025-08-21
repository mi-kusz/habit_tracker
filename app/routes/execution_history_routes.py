from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required

from ..dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from ..services import execution_history_service
from ..services.auth_service import get_jwt_data
from ..utils import get_payload

execution_history_blueprint = Blueprint("execution_histories", __name__)


@execution_history_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_execution_histories() -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    user_id: Optional[str] = request.args.get("user_id")
    category_id: Optional[str] = request.args.get("category_id")
    habit_task_id: Optional[str] = request.args.get("habit_task_id")
    start_datetime: Optional[str] = request.args.get("start_datetime")
    end_datetime: Optional[str] = request.args.get("end_datetime")



    execution_histories: list[ExecutionHistoryReadDTO] = execution_history_service.get_execution_histories(jwt_user_id,
                                                                                                           role,
                                                                                                           user_id,
                                                                                                           category_id,
                                                                                                           habit_task_id,
                                                                                                           start_datetime,
                                                                                                           end_datetime)
    execution_histories_dicts: list[dict] = [execution_history.model_dump() for execution_history in execution_histories]

    return jsonify(execution_histories_dicts), HTTPStatus.OK


@execution_history_blueprint.route("/<int:execution_history_id>", methods=["GET"])
@jwt_required()
def get_execution_history_by_id(execution_history_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    execution_history: ExecutionHistoryReadDTO = execution_history_service.get_execution_history_by_id(jwt_user_id, role, execution_history_id)

    return jsonify(execution_history.model_dump()), HTTPStatus.OK


@execution_history_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_execution_history() -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    payload: dict = get_payload()

    execution_history_dto: ExecutionHistoryCreateDTO = ExecutionHistoryCreateDTO(**payload)
    execution_history_read_dto: ExecutionHistoryReadDTO = execution_history_service.create_execution_history(jwt_user_id, role, execution_history_dto)

    return jsonify(execution_history_read_dto.model_dump()), HTTPStatus.CREATED


@execution_history_blueprint.route("/<int:execution_history_id>", methods=["DELETE"])
@jwt_required()
def delete_execution_history(execution_history_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    execution_history: ExecutionHistoryReadDTO = execution_history_service.delete_execution_history(jwt_user_id, role, execution_history_id)

    return jsonify({}), HTTPStatus.NO_CONTENT