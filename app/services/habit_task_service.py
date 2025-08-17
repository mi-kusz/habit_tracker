from typing import Optional

from sqlalchemy.exc import IntegrityError
from app import database

from app.dtos import HabitTaskReadDTO, HabitTaskCreateDTO, HabitTaskUpdateDTO
from app.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import HabitTask
from app.repositories import habit_task_repository


entity_type: str = "Habit Task"


def get_habit_tasks() -> list[HabitTaskReadDTO]:
    habit_tasks: list[HabitTask] = habit_task_repository.get_habit_tasks()

    return [HabitTaskReadDTO.model_validate(habit_task) for habit_task in habit_tasks]


def get_habit_task_by_id(habit_task_id: int) -> HabitTaskReadDTO:
    habit_task: HabitTask = get_habit_task_entity(habit_task_id)

    return HabitTaskReadDTO.model_validate(habit_task)


def create_habit_task(habit_task_dto: HabitTaskCreateDTO) -> HabitTaskReadDTO:
    habit_task: HabitTask = convert_dto_to_model(habit_task_dto)

    try:
        with database.session.begin():
            created_habit_task: HabitTask = habit_task_repository.create_habit_task(database.session, habit_task)

        return HabitTaskReadDTO.model_validate(created_habit_task)
    except IntegrityError:
        raise EntityPersistenceException(entity_type)


def update_habit_task(habit_task_id: int, habit_task_updates: HabitTaskUpdateDTO) -> HabitTaskReadDTO:
    with database.session.begin():
        habit_task: HabitTask = get_habit_task_entity(habit_task_id)

        if habit_task_updates.category_id is not None:
            habit_task.category_id = habit_task_updates.category_id

        if habit_task_updates.name is not None:
            habit_task.name = habit_task_updates.name

        if habit_task_updates.description is not None:
            habit_task.description = habit_task_updates.description

    return HabitTaskReadDTO.model_validate(habit_task)


def delete_habit_task(habit_task_id: int) -> HabitTaskReadDTO:
    with database.session.begin():
        habit_task: HabitTask = get_habit_task_entity(habit_task_id)

        habit_task_repository.delete_habit_task(database.session, habit_task)

    return HabitTaskReadDTO.model_validate(habit_task)


def convert_dto_to_model(habit_task_dto: HabitTaskCreateDTO) -> HabitTask:
    return HabitTask(
        category_id=habit_task_dto.category_id,
        name=habit_task_dto.name,
        description=habit_task_dto.description
    )


def get_habit_task_entity(habit_task_id: int) -> HabitTask:
    habit_task: Optional[HabitTask] = habit_task_repository.get_habit_task_by_id(habit_task_id)

    if habit_task is None:
        raise EntityNotFoundException(entity_type)

    return habit_task