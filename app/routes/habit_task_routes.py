from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required

from ..dtos import HabitTaskReadDTO, HabitTaskCreateDTO, HabitTaskUpdateDTO
from ..services import habit_task_service
from ..services.auth_service import get_jwt_data
from ..utils import get_payload

habit_task_blueprint = Blueprint("habit_tasks", __name__)


@habit_task_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_habit_tasks() -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    user_id: Optional[str] = request.args.get("user_id")
    category_id: Optional[str] = request.args.get("category_id")
    name: Optional[str] = request.args.get("name")

    habit_tasks: list[HabitTaskReadDTO] = habit_task_service.get_habit_tasks(jwt_user_id, role, user_id, category_id, name)
    habit_tasks_dicts: list[dict] = [habit_task.model_dump() for habit_task in habit_tasks]

    return jsonify(habit_tasks_dicts), HTTPStatus.OK


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["GET"])
@jwt_required()
def get_habit_task_by_id(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    habit_task: HabitTaskReadDTO = habit_task_service.get_habit_task_by_id(jwt_user_id, role, habit_task_id)

    return jsonify(habit_task.model_dump()), HTTPStatus.OK


@habit_task_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_habit_task() -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    payload: dict = get_payload()

    habit_task_create_dto: HabitTaskCreateDTO = HabitTaskCreateDTO(**payload)
    habit_task_read_dto: HabitTaskReadDTO = habit_task_service.create_habit_task(jwt_user_id, role, habit_task_create_dto)

    return jsonify(habit_task_read_dto.model_dump()), HTTPStatus.CREATED


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["PUT"])
@jwt_required()
def update_habit_task(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    payload: dict = get_payload()

    habit_task_update_dto: HabitTaskUpdateDTO = HabitTaskUpdateDTO(**payload)
    habit_task_read_dto: HabitTaskReadDTO = habit_task_service.update_habit_task(jwt_user_id, role, habit_task_id, habit_task_update_dto)

    return jsonify(habit_task_read_dto.model_dump()), HTTPStatus.CREATED


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["DELETE"])
@jwt_required()
def delete_habit_task(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    jwt_user_id, role = get_jwt_data()

    habit_task: HabitTaskReadDTO = habit_task_service.delete_habit_task(jwt_user_id, role, habit_task_id)

    return jsonify({}), HTTPStatus.NO_CONTENT