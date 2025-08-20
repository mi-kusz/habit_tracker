from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response

from app.exceptions.handlers import create_error_response
from ..dtos import HabitTaskReadDTO, HabitTaskCreateDTO, HabitTaskUpdateDTO
from ..services import habit_task_service

habit_task_blueprint = Blueprint("habit_tasks", __name__)


@habit_task_blueprint.route("/", methods=["GET"])
def get_habit_tasks() -> tuple[Response, HTTPStatus]:
    category_id: Optional[str] = request.args.get("category_id")
    name: Optional[str] = request.args.get("name")

    habit_tasks: list[HabitTaskReadDTO] = habit_task_service.get_habit_tasks(category_id, name)
    habit_tasks_dicts: list[dict] = [habit_task.model_dump() for habit_task in habit_tasks]

    return jsonify(habit_tasks_dicts), HTTPStatus.OK


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["GET"])
def get_habit_task_by_id(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    habit_task: HabitTaskReadDTO = habit_task_service.get_habit_task_by_id(habit_task_id)

    return jsonify(habit_task.model_dump()), HTTPStatus.OK


@habit_task_blueprint.route("/", methods=["POST"])
def create_habit_task() -> tuple[Response, HTTPStatus]:
    payload: Optional[dict] = request.get_json()

    if payload is None:
        return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

    habit_task_create_dto: HabitTaskCreateDTO = HabitTaskCreateDTO(**payload)
    habit_task_read_dto: HabitTaskReadDTO = habit_task_service.create_habit_task(habit_task_create_dto)

    return jsonify(habit_task_read_dto.model_dump()), HTTPStatus.CREATED


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["PUT"])
def update_habit_task(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    payload: Optional[dict] = request.get_json()

    if payload is None:
        return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

    habit_task_update_dto: HabitTaskUpdateDTO = HabitTaskUpdateDTO(**payload)
    habit_task_read_dto: HabitTaskReadDTO = habit_task_service.update_habit_task(habit_task_id, habit_task_update_dto)

    return jsonify(habit_task_read_dto.model_dump()), HTTPStatus.CREATED


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["DELETE"])
def delete_habit_task(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    habit_task: HabitTaskReadDTO = habit_task_service.delete_habit_task(habit_task_id)

    return jsonify(habit_task.model_dump()), HTTPStatus.NO_CONTENT