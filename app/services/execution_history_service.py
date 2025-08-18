from datetime import datetime
from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from app.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import ExecutionHistory
from app.repositories import execution_history_repository
from app.utils import str_to_int_or_none, str_to_datetime_or_none

entity_type: str = "Execution history"


def get_execution_histories(habit_task_id: Optional[str],
                            start_datetime: Optional[str],
                            end_datetime: Optional[str]) -> list[ExecutionHistoryReadDTO]:
    habit_task_id_int: Optional[int] = str_to_int_or_none(habit_task_id)
    start_datetime_dt: Optional[datetime] = str_to_datetime_or_none(start_datetime)
    end_datetime_dt: Optional[datetime] = str_to_datetime_or_none(end_datetime)

    execution_histories: list[ExecutionHistory] = execution_history_repository.get_execution_histories(habit_task_id_int, start_datetime_dt, end_datetime_dt)

    return [ExecutionHistoryReadDTO.model_validate(execution_history) for execution_history in execution_histories]


def get_execution_history_by_id(execution_history_id: int) -> ExecutionHistoryReadDTO:
    execution_history: ExecutionHistory = get_execution_history_entity(execution_history_id)

    return ExecutionHistoryReadDTO.model_validate(execution_history)


def create_execution_history(execution_history_dto: ExecutionHistoryCreateDTO) -> ExecutionHistoryReadDTO:
    execution_history: ExecutionHistory = convert_dto_to_model(execution_history_dto)

    try:
        with database.session.begin():
            created_execution_history: ExecutionHistory = execution_history_repository.create_execution_history(database.session, execution_history)

        return ExecutionHistoryReadDTO.model_validate(created_execution_history)
    except IntegrityError:
        raise EntityPersistenceException(entity_type)


def delete_execution_history(execution_history_id: int) -> ExecutionHistoryReadDTO:
    execution_history: ExecutionHistory = get_execution_history_entity(execution_history_id)

    with database.session.begin():
        execution_history_repository.delete_execution_history(database.session, execution_history)

    return ExecutionHistoryReadDTO.model_validate(execution_history)


def convert_dto_to_model(execution_history_dto: ExecutionHistoryCreateDTO) -> ExecutionHistory:
    return ExecutionHistory(
        habit_task_id=execution_history_dto.habit_task_id,
        executed_at=execution_history_dto.executed_at
    )


def get_execution_history_entity(execution_history_id: int) -> ExecutionHistory:
    execution_history: Optional[ExecutionHistory] = execution_history_repository.get_execution_history_by_id(execution_history_id)

    if execution_history is None:
        raise EntityNotFoundException(entity_type)

    return execution_history