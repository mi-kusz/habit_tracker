from typing import Optional

from sqlalchemy.orm import Session

from app.models import HabitTask


def get_habit_tasks(user_id: Optional[int],
                    category_id: Optional[int],
                    name: Optional[str]) -> list[HabitTask]:
    query = HabitTask.query

    if user_id is not None:
        query = query.filter(HabitTask.category.has(user_id=user_id))

    if category_id is not None:
        query = query.filter(HabitTask.category_id == category_id)

    if name is not None:
        query = query.filter(HabitTask.name.ilike(f"%{name}%"))

    return query.all()


def get_habit_task_by_id(habit_task_id: int, user_id: Optional[int]) -> Optional[HabitTask]:
    query = HabitTask.query.filter(HabitTask.id == habit_task_id)

    if user_id is not None:
        query = query.filter(HabitTask.category.has(user_id=user_id))

    return query.first()


def create_habit_task(session: Session, habit_task: HabitTask) -> HabitTask:
    session.add(habit_task)
    return habit_task


def delete_habit_task(session: Session, habit_task: HabitTask) -> HabitTask:
    session.delete(habit_task)
    return habit_task
