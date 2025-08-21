from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.dtos import HabitTaskReadDTO, HabitTaskCreateDTO, HabitTaskUpdateDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import HabitTask, Category
from app.models.User import UserRole
from app.repositories import habit_task_repository
from app.services.category_service import get_category_entity
from app.utils import str_to_int_or_none

entity_type: str = "Habit Task"


def get_habit_tasks(requester_id: int,
                    requester_role: UserRole,
                    user_id: Optional[str],
                    category_id: Optional[str],
                    name: Optional[str]) -> list[HabitTaskReadDTO]:
    user_id_int: Optional[int] = str_to_int_or_none(user_id)
    category_id_int: Optional[int] = str_to_int_or_none(category_id)

    if requester_role == UserRole.USER and user_id_int is None:
        user_id_int = requester_id

    if requester_role != UserRole.ADMIN and requester_id != user_id_int:
        raise PermissionError("Forbidden")

    habit_tasks: list[HabitTask] = habit_task_repository.get_habit_tasks(user_id_int, category_id_int, name)

    return [HabitTaskReadDTO.model_validate(habit_task) for habit_task in habit_tasks]


def get_habit_task_by_id(requester_id: int,
                         requester_role: UserRole,
                         habit_task_id: int) -> HabitTaskReadDTO:
    try:
        habit_task: HabitTask = get_habit_task_entity(habit_task_id)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    if requester_role != UserRole.ADMIN and requester_id != habit_task.category.user_id:
        raise PermissionError("Forbidden")

    return HabitTaskReadDTO.model_validate(habit_task)


def create_habit_task(requester_id: int,
                      requester_role: UserRole,
                      habit_task_dto: HabitTaskCreateDTO) -> HabitTaskReadDTO:
    habit_task: HabitTask = convert_dto_to_model(habit_task_dto)

    try:
        with database.session.begin():
            # Check if category exists / exists and belongs to requester
            if requester_role == UserRole.ADMIN:
                category: Category = get_category_entity(habit_task.category_id)
            else:
                category: Category = get_category_entity(habit_task.category_id, requester_id)

            created_habit_task: HabitTask = habit_task_repository.create_habit_task(database.session, habit_task)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")
    except IntegrityError:
        raise EntityPersistenceException(entity_type)

    return HabitTaskReadDTO.model_validate(created_habit_task)


def update_habit_task(requester_id: int,
                      requester_role: UserRole,
                      habit_task_id: int,
                      habit_task_updates: HabitTaskUpdateDTO) -> HabitTaskReadDTO:
    try:
        with database.session.begin():
            if requester_role == UserRole.ADMIN:
                habit_task: HabitTask = get_habit_task_entity(habit_task_id)
            else:
                habit_task: HabitTask = get_habit_task_entity(habit_task_id, requester_id)

            if habit_task_updates.category_id is not None:
                habit_task.category_id = habit_task_updates.category_id

            if habit_task_updates.name is not None:
                habit_task.name = habit_task_updates.name

            if habit_task_updates.description is not None:
                habit_task.description = habit_task_updates.description
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    return HabitTaskReadDTO.model_validate(habit_task)


def delete_habit_task(requester_id: int,
                      requester_role: UserRole,
                      habit_task_id: int) -> HabitTaskReadDTO:
    try:
        with database.session.begin():
            if requester_role == UserRole.ADMIN:
                habit_task: HabitTask = get_habit_task_entity(habit_task_id)
            else:
                habit_task: HabitTask = get_habit_task_entity(habit_task_id, requester_id)

            habit_task_repository.delete_habit_task(database.session, habit_task)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    return HabitTaskReadDTO.model_validate(habit_task)


def convert_dto_to_model(habit_task_dto: HabitTaskCreateDTO) -> HabitTask:
    return HabitTask(
        category_id=habit_task_dto.category_id,
        name=habit_task_dto.name,
        description=habit_task_dto.description
    )


def get_habit_task_entity(habit_task_id: int, user_id: Optional[int] = None) -> HabitTask:
    habit_task: Optional[HabitTask] = habit_task_repository.get_habit_task_by_id(habit_task_id, user_id)

    if habit_task is None:
        raise EntityNotFoundException(entity_type)

    return habit_task