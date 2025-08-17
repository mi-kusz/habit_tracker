from typing import Optional

from sqlalchemy.orm import Session

from app.models import HabitTask


def get_habit_tasks() -> list[HabitTask]:
    return HabitTask.query.all()


def get_habit_task_by_id(habit_task_id: int) -> Optional[HabitTask]:
    return HabitTask.query.get(habit_task_id)


def create_habit_task(session: Session, habit_task: HabitTask) -> HabitTask:
    session.add(habit_task)
    return habit_task


def delete_habit_task(session: Session, habit_task: HabitTask) -> HabitTask:
    session.delete(habit_task)
    return habit_task