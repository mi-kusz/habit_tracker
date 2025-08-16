from app import database
from app.models import ExecutionHistory


def get_execution_history() -> list[ExecutionHistory]:
    return ExecutionHistory.query.all()


def get_execution_history_by_id(execution_history_id: int) -> ExecutionHistory:
    return ExecutionHistory.query.get(execution_history_id)


def create_execution_history(execution_history: ExecutionHistory) -> ExecutionHistory:
    database.session.add(execution_history)
    database.session.commit()
    return execution_history


def update_execution_history(execution_history: ExecutionHistory) -> ExecutionHistory:
    database.session.commit()
    return execution_history
