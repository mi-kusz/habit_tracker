from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import ExecutionHistory, HabitTask


def get_execution_histories(user_id: Optional[int],
                            category_id: Optional[int],
                            habit_task_id: Optional[int],
                            start_datetime: Optional[datetime],
                            end_datetime: Optional[datetime]) -> list[ExecutionHistory]:
    query = ExecutionHistory.query

    if user_id is not None:
        query = query.filter(ExecutionHistory.habit_task.has(
            HabitTask.category.has(user_id=user_id)
        )
        )

    if category_id is not None:
        query = query.filter(ExecutionHistory.habit_task.has(category_id=category_id))

    if habit_task_id is not None:
        query = query.filter(ExecutionHistory.habit_task_id == habit_task_id)

    if start_datetime is not None:
        query = query.filter(start_datetime <= ExecutionHistory.executed_at)

    if end_datetime is not None:
        query = query.filter(ExecutionHistory.executed_at <= end_datetime)

    return query.all()


def get_execution_history_by_id(execution_history_id: int, user_id: Optional[int]) -> Optional[ExecutionHistory]:
    query = ExecutionHistory.query.filter(ExecutionHistory.id == execution_history_id)

    if user_id is not None:
        query = query.filter(ExecutionHistory.habit_task.has(
            HabitTask.category.has(user_id=user_id)
        ))

    return query.first()


def create_execution_history(session: Session, execution_history: ExecutionHistory) -> ExecutionHistory:
    session.add(execution_history)
    return execution_history


def delete_execution_history(session: Session, execution_history: ExecutionHistory) -> ExecutionHistory:
    session.delete(execution_history)
    return execution_history
