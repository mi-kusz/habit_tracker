from typing import Optional

from sqlalchemy.exc import IntegrityError
from app import database

from app.dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from app.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import ExecutionHistory
from app.repositories import execution_history_repository


entity_type: str = "Execution history"


def get_execution_histories() -> list[ExecutionHistoryReadDTO]:
    execution_histories: list[ExecutionHistory] = execution_history_repository.get_execution_histories()

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