from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import ExecutionHistory


def get_execution_histories() -> list[ExecutionHistory]:
    return ExecutionHistory.query.all()


def get_execution_history_by_id(execution_history_id: int) -> Optional[ExecutionHistory]:
    return ExecutionHistory.query.get(execution_history_id)


def create_execution_history(session: Session, execution_history: ExecutionHistory) -> ExecutionHistory:
    session.add(execution_history)
    return execution_history


def delete_execution_history(session: Session, execution_history: ExecutionHistory) -> ExecutionHistory:
    session.delete(execution_history)
    return execution_history


def get_execution_histories_by_habit_task_id(session: Session, habit_task_id: int) -> list[ExecutionHistory]:
    return session.query(ExecutionHistory).filter(ExecutionHistory.habit_task_id == habit_task_id).all()


def get_execution_histories_by_datetime_range(session: Session,
                                              datetime_start: Optional[datetime],
                                              datetime_end: Optional[datetime]) -> list[ExecutionHistory]:
    query = session.query(ExecutionHistory)

    if datetime_start is not None:
        query = query.filter(datetime_start <= ExecutionHistory.executed_at)

    if datetime_end is not None:
        query = query.filter(ExecutionHistory.executed_at <= datetime_end)

    return query.all()


def get_execution_histories_by_habit_task_id_and_datetime_range(session: Session,
                                                                habit_task_id: int,
                                                                datetime_start: Optional[datetime],
                                                                datetime_end: Optional[datetime]) -> list[ExecutionHistory]:
    query = session.query(ExecutionHistory).filter(ExecutionHistory.habit_task_id == habit_task_id)

    if datetime_start is not None:
        query = query.filter(datetime_start <= ExecutionHistory.executed_at)

    if datetime_end is not None:
        query = query.filter(ExecutionHistory.executed_at <= datetime_end)

    return query.all()