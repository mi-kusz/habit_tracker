from datetime import datetime

import pytest

from app.dtos import UserCreateDTO, UserUpdateDTO, CategoryCreateDTO, CategoryUpdateDTO, HabitTaskCreateDTO, \
    HabitTaskUpdateDTO, ExecutionHistoryCreateDTO
from app.models import Category, HabitTask, ExecutionHistory
from app.models.User import UserRole, User


@pytest.fixture
def fake_user_dto() -> UserCreateDTO:
    return UserCreateDTO(
        first_name="John",
        last_name="Doe",
        email="test@email.com",
        password="password123",
        role=UserRole.USER
    )


@pytest.fixture
def fake_user_update_dto() -> UserUpdateDTO:
    return UserUpdateDTO(
        first_name="First name",
        last_name="Last name"
    )


@pytest.fixture
def fake_user_model() -> User:
    return User(
        id=1,
        first_name="John",
        last_name="Doe",
        email="test@email.com",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def fake_category_dto() -> CategoryCreateDTO:
    return CategoryCreateDTO(
        user_id=1,
        name="Category name",
        description="Category description"
    )


@pytest.fixture
def fake_category_update_dto() -> CategoryUpdateDTO:
    return CategoryUpdateDTO(
        name="Changed name",
        description="Changed description"
    )


@pytest.fixture
def fake_category_model() -> Category:
    return Category(
        id=1,
        user_id=1,
        name="Category name",
        description="Category description",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def fake_habit_task_dto() -> HabitTaskCreateDTO:
    return HabitTaskCreateDTO(
        category_id=1,
        name="Habit task name",
        description="Habit task description"
    )


@pytest.fixture
def fake_habit_task_update_dto() -> HabitTaskUpdateDTO:
    return HabitTaskUpdateDTO(
        category_id=10,
        name="Changed name",
        description="Changed description"
    )


@pytest.fixture
def fake_habit_task_model(fake_category_model: Category) -> HabitTask:
    return HabitTask(
        id=1,
        category_id=1,
        name="Habit task name",
        description="Habit task description",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        category=fake_category_model
    )


@pytest.fixture
def fake_execution_history_dto() -> ExecutionHistoryCreateDTO:
    return ExecutionHistoryCreateDTO(
        habit_task_id=1,
        executed_at=datetime.now()
    )


@pytest.fixture
def fake_execution_history_model(fake_habit_task_model: HabitTask) -> ExecutionHistory:
    return ExecutionHistory(
        id=1,
        habit_task_id=1,
        executed_at=datetime.now(),
        habit_task=fake_habit_task_model
    )
