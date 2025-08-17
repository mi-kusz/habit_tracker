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