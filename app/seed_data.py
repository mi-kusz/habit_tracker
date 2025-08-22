import random
from datetime import datetime, timezone, timedelta

from faker import Faker

from app import create_app, database
from app.models import User, Category, HabitTask, ExecutionHistory
from app.models.User import UserRole

app = create_app()
fake = Faker()

def seed_users(n: int = 10) -> list[User]:
    users: list[User] = []

    for _ in range(n):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            role=UserRole.USER,
            is_active=True
        )

        user.set_password("password123")
        users.append(user)

    database.session.add_all(users)
    database.session.flush()

    return users


def seed_categories(users: list[User], categories_per_user: int = 3) -> list[Category]:
    categories: list[Category] = []

    for user in users:
        for _ in range(categories_per_user):
            category = Category(
                user_id=user.id,
                name=fake.word(),
                description=fake.sentence()
            )

            categories.append(category)

    database.session.add_all(categories)
    database.session.flush()

    return categories


def seed_habit_tasks(categories: list[Category], habit_tasks_per_category: int = 5) -> list[HabitTask]:
    habit_tasks: list[HabitTask] = []

    for category in categories:
        for _ in range(habit_tasks_per_category):
            task = HabitTask(
                category_id=category.id,
                name=fake.word(),
                description=fake.sentence()
            )

            habit_tasks.append(task)

    database.session.add_all(habit_tasks)
    database.session.flush()

    return habit_tasks


def seed_execution_histories(habit_tasks: list[HabitTask], execution_histories_per_habit_task: int = 15) -> list[ExecutionHistory]:
    execution_histories: list[ExecutionHistory] = []

    for habit_task in habit_tasks:
        for _ in range(execution_histories_per_habit_task):
            exec_time = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))

            history = ExecutionHistory(
                habit_task_id=habit_task.id,
                executed_at=exec_time
            )

            execution_histories.append(history)

    database.session.add_all(execution_histories)

    return execution_histories


if __name__ == "__main__":
    with app.app_context():
        with database.session.begin():
            users: list[User] = seed_users()
            categories: list[Category] = seed_categories(users)
            habit_tasks: list[HabitTask] = seed_habit_tasks(categories)
            execution_histories: list[ExecutionHistory] = seed_execution_histories(habit_tasks)

            print("Seeding finished")