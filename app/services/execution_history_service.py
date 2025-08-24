from datetime import datetime
from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import ExecutionHistory, HabitTask
from app.models.User import UserRole
from app.repositories import execution_history_repository
from app.services.habit_task_service import get_habit_task_entity
from app.utils import str_to_int_or_none, str_to_datetime_or_none

entity_type: str = "Execution history"


def get_execution_histories(requester_id: int,
                            requester_role: UserRole,
                            user_id: Optional[str],
                            category_id: Optional[str],
                            habit_task_id: Optional[str],
                            start_datetime: Optional[str],
                            end_datetime: Optional[str]) -> list[ExecutionHistoryReadDTO]:
    user_id_int: Optional[int] = str_to_int_or_none(user_id)
    category_id_int: Optional[int] = str_to_int_or_none(category_id)
    habit_task_id_int: Optional[int] = str_to_int_or_none(habit_task_id)
    start_datetime_dt: Optional[datetime] = str_to_datetime_or_none(start_datetime)
    end_datetime_dt: Optional[datetime] = str_to_datetime_or_none(end_datetime)

    if requester_role == UserRole.USER and user_id_int is None:
        user_id_int = requester_id

    if requester_role != UserRole.ADMIN and requester_id != user_id_int:
        raise PermissionError("Forbidden")

    execution_histories: list[ExecutionHistory] = execution_history_repository.get_execution_histories(user_id_int,
                                                                                                       category_id_int,
                                                                                                       habit_task_id_int,
                                                                                                       start_datetime_dt,
                                                                                                       end_datetime_dt)

    return [ExecutionHistoryReadDTO.model_validate(execution_history) for execution_history in execution_histories]


def get_execution_history_by_id(requester_id: int,
                                requester_role: UserRole,
                                execution_history_id: int) -> ExecutionHistoryReadDTO:
    try:
        execution_history: ExecutionHistory = get_execution_history_entity(execution_history_id)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    if requester_role != UserRole.ADMIN and requester_id != execution_history.habit_task.category.user_id:
        raise PermissionError("Forbidden")

    return ExecutionHistoryReadDTO.model_validate(execution_history)


def create_execution_history(requester_id: int,
                             requester_role: UserRole,
                             execution_history_dto: ExecutionHistoryCreateDTO) -> ExecutionHistoryReadDTO:
    execution_history: ExecutionHistory = convert_dto_to_model(execution_history_dto)

    try:
        with database.session.begin():
            # Check if habit task exists / exists and belongs to requester
            if requester_role == UserRole.ADMIN:
                _habit_task: HabitTask = get_habit_task_entity(execution_history.habit_task_id)
            else:
                _habit_task: HabitTask = get_habit_task_entity(execution_history.habit_task_id, requester_id)

            created_execution_history: ExecutionHistory = execution_history_repository.create_execution_history(
                database.session, execution_history)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")
    except IntegrityError:
        raise EntityPersistenceException(entity_type)

    return ExecutionHistoryReadDTO.model_validate(created_execution_history)


def delete_execution_history(requester_id: int,
                             requester_role: UserRole,
                             execution_history_id: int) -> ExecutionHistoryReadDTO:
    try:
        with database.session.begin():
            if requester_role == UserRole.ADMIN:
                execution_history: ExecutionHistory = get_execution_history_entity(execution_history_id)
            else:
                execution_history: ExecutionHistory = get_execution_history_entity(execution_history_id, requester_id)

            execution_history_repository.delete_execution_history(database.session, execution_history)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    return ExecutionHistoryReadDTO.model_validate(execution_history)


def convert_dto_to_model(execution_history_dto: ExecutionHistoryCreateDTO) -> ExecutionHistory:
    return ExecutionHistory(
        habit_task_id=execution_history_dto.habit_task_id,
        executed_at=execution_history_dto.executed_at
    )


def get_execution_history_entity(execution_history_id: int, user_id: Optional[int] = None) -> ExecutionHistory:
    execution_history: Optional[ExecutionHistory] = execution_history_repository.get_execution_history_by_id(
        execution_history_id, user_id)

    if execution_history is None:
        raise EntityNotFoundException(entity_type)

    return execution_history
