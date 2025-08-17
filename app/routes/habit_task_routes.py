from http import HTTPStatus
from typing import Optional

from flask import Blueprint, jsonify, request, Response
from pydantic import ValidationError

from ..dtos import HabitTaskReadDTO, HabitTaskCreateDTO, HabitTaskUpdateDTO
from ..exceptions import EntityNotFoundException, EntityPersistenceException
from ..services import habit_task_service
from ..utils import create_error_response


habit_task_blueprint = Blueprint("habit_tasks", __name__)


@habit_task_blueprint.route("/", methods=["GET"])
def get_habit_tasks() -> tuple[Response, HTTPStatus]:
    habit_tasks: list[HabitTaskReadDTO] = habit_task_service.get_habit_tasks()
    habit_tasks_dicts: list[dict] = [habit_task.model_dump() for habit_task in habit_tasks]

    return jsonify(habit_tasks_dicts), HTTPStatus.OK


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["GET"])
def get_habit_task_by_id(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    try:
        habit_task: HabitTaskReadDTO = habit_task_service.get_habit_task_by_id(habit_task_id)

        return jsonify(habit_task.model_dump()), HTTPStatus.OK
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND


@habit_task_blueprint.route("/", methods=["POST"])
def create_habit_task() -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        habit_task_create_dto: HabitTaskCreateDTO = HabitTaskCreateDTO(**payload)
        habit_task_read_dto: HabitTaskReadDTO = habit_task_service.create_habit_task(habit_task_create_dto)

        return jsonify(habit_task_read_dto.model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST


@habit_task_blueprint.route("/<int:habit_task_id>", methods=["PUT"])
def update_habit_task(habit_task_id: int) -> tuple[Response, HTTPStatus]:
    try:
        payload: Optional[dict] = request.get_json()

        if payload is None:
            return create_error_response("Missing JSON body"), HTTPStatus.BAD_REQUEST

        habit_task_update_dto: HabitTaskUpdateDTO = HabitTaskUpdateDTO(**payload)
        habit_task_read_dto: HabitTaskReadDTO = habit_task_service.update_habit_task(habit_task_id, habit_task_update_dto)

        return jsonify(habit_task_read_dto.model_dump()), HTTPStatus.CREATED
    except EntityNotFoundException as e:
        return create_error_response(str(e)), HTTPStatus.NOT_FOUND
    except ValidationError as e:
        return create_error_response(str(e.errors())), HTTPStatus.BAD_REQUEST
    except EntityPersistenceException as e:
        return create_error_response(str(e)), HTTPStatus.BAD_REQUEST