from typing import Optional

from sqlalchemy.orm import Session

from app.models import HabitTask, Category


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


def get_habit_tasks_by_category_id(session: Session, category_id: int) -> list[HabitTask]:
    return session.query(HabitTask).filter(HabitTask.category_id == category_id).all()


def get_habit_tasks_by_user_id(session: Session, user_id: int) -> list[HabitTask]:
    return session.query(HabitTask).join(Category).filter(Category.user_id == user_id).all()


def get_habit_tasks_by_name(session: Session, name: str) -> list[HabitTask]:
    return session.query(HabitTask).filter(HabitTask.name.ilike(f"%{name}%")).all()