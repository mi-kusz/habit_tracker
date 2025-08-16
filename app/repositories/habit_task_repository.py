from app import database
from app.models import HabitTask


def get_habit_tasks() -> list[HabitTask]:
    return HabitTask.query.all()


def get_habit_task_by_id(habit_task_id: int) -> HabitTask:
    return HabitTask.query.get(habit_task_id)


def create_habit_task(habit_task: HabitTask) -> HabitTask:
    database.session.add(habit_task)
    database.session.commit()
    return habit_task


def update_habit_task(habit_task: HabitTask) -> HabitTask:
    database.session.commit()
    return habit_task
