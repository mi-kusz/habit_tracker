from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError

from app.dtos import HabitTaskCreateDTO, HabitTaskUpdateDTO, HabitTaskReadDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import HabitTask, Category
from app.models.User import UserRole
from app.services.habit_task_service import get_habit_tasks, get_habit_task_by_id, create_habit_task, update_habit_task, \
    delete_habit_task, convert_dto_to_model

DATABASE_SESSION = "app.services.habit_task_service.database.session"
DATABASE_SESSION_BEGIN = "app.services.habit_task_service.database.session.begin"
GET_HABIT_TASKS = "app.repositories.habit_task_repository.get_habit_tasks"
GET_HABIT_TASK_ENTITY = "app.services.habit_task_service.get_habit_task_entity"
HABIT_TASK_REPO_CREATE = "app.repositories.habit_task_repository.create_habit_task"
HABIT_TASK_REPO_DELETE = "app.repositories.habit_task_repository.delete_habit_task"
GET_CATEGORY_ENTITY = "app.services.habit_task_service.get_category_entity"


def test_get_habit_tasks_by_self(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(GET_HABIT_TASKS, return_value=[fake_habit_task_model])

    result: list[HabitTaskReadDTO] = get_habit_tasks(
        requester_id=1,
        requester_role=UserRole.USER,
        user_id=None,
        category_id=None,
        name=None
    )

    assert len(result) == 1

    habit_task_dto: HabitTaskReadDTO = result[0]
    assert isinstance(habit_task_dto, HabitTaskReadDTO)


def test_get_habit_tasks_by_different_user(mocker: MockerFixture):
    mocker.patch(GET_HABIT_TASKS, return_value=[])

    with pytest.raises(PermissionError):
        get_habit_tasks(
            requester_id=1,
            requester_role=UserRole.USER,
            user_id="2",
            category_id=None,
            name=None
        )


def test_get_habit_tasks_by_admin(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(GET_HABIT_TASKS, return_value=[fake_habit_task_model])

    result: list[HabitTaskReadDTO] = get_habit_tasks(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id="2",
        category_id=None,
        name=None
    )

    assert len(result) == 1

    habit_task_dto: HabitTaskReadDTO = result[0]
    assert isinstance(habit_task_dto, HabitTaskReadDTO)


def test_get_habit_tasks_does_not_call_repository_if_forbidden(mocker: MockerFixture):
    mock_get_habit_tasks = mocker.patch(GET_HABIT_TASKS, return_value=[])

    with pytest.raises(PermissionError):
        get_habit_tasks(
            requester_id=1,
            requester_role=UserRole.USER,
            user_id="2",
            category_id=None,
            name=None
        )

    mock_get_habit_tasks.assert_not_called()


def test_get_habit_tasks_calls_repository_with_correct_arguments(mocker: MockerFixture,
                                                                 fake_habit_task_model: HabitTask):
    mock_get_habit_tasks = mocker.patch(GET_HABIT_TASKS, return_value=[fake_habit_task_model])

    result: list[HabitTaskReadDTO] = get_habit_tasks(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id="1",
        category_id="5",
        name="Name"
    )

    mock_get_habit_tasks.assert_called_once_with(1, 5, "Name")

    assert len(result) == 1

    habit_task_dto: HabitTaskReadDTO = result[0]
    assert isinstance(habit_task_dto, HabitTaskReadDTO)


def test_get_habit_tasks_calls_repository_with_none_arguments(mocker: MockerFixture):
    mock_get_habit_tasks = mocker.patch(GET_HABIT_TASKS, return_value=[])

    get_habit_tasks(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id=None,
        category_id=None,
        name=None
    )

    mock_get_habit_tasks.assert_called_once_with(None, None, None)


def test_get_habit_tasks_returns_empty_list(mocker: MockerFixture):
    mocker.patch(GET_HABIT_TASKS, return_value=[])

    result: list[HabitTaskReadDTO] = get_habit_tasks(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id=None,
        category_id=None,
        name=None
    )

    assert result == []


def test_get_habit_tasks_returns_list_of_habit_task_read_dto(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(GET_HABIT_TASKS, return_value=[fake_habit_task_model] * 50)

    result: list[HabitTaskReadDTO] = get_habit_tasks(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id=None,
        category_id=None,
        name=None
    )

    assert len(result) == 50

    for habit_task in result:
        assert isinstance(habit_task, HabitTaskReadDTO)


def test_get_habit_task_by_id_by_self(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = get_habit_task_by_id(
        requester_id=1,
        requester_role=UserRole.USER,
        habit_task_id=1
    )

    assert isinstance(result, HabitTaskReadDTO)


def test_get_habit_task_by_id_by_different_user(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)

    with pytest.raises(PermissionError):
        get_habit_task_by_id(
            requester_id=999,
            requester_role=UserRole.USER,
            habit_task_id=1
        )


def test_get_habit_task_by_id_by_admin(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = get_habit_task_by_id(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        habit_task_id=1
    )

    assert isinstance(result, HabitTaskReadDTO)


def test_get_habit_task_by_id_not_found(mocker: MockerFixture):
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))

    with pytest.raises(EntityNotFoundException):
        get_habit_task_by_id(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            habit_task_id=1
        )


def test_create_habit_task_by_self(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                   fake_habit_task_dto: HabitTaskCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mock_create_habit_task = mocker.patch(HABIT_TASK_REPO_CREATE, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = create_habit_task(
        requester_id=1,
        requester_role=UserRole.USER,
        habit_task_dto=fake_habit_task_dto
    )

    mock_create_habit_task.assert_called_once()

    assert isinstance(result, HabitTaskReadDTO)


def test_create_habit_task_by_different_user(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                             fake_habit_task_dto: HabitTaskCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))

    with pytest.raises(PermissionError):
        create_habit_task(
            requester_id=999,
            requester_role=UserRole.USER,
            habit_task_dto=fake_habit_task_dto
        )


def test_create_habit_task_by_admin(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                    fake_habit_task_dto: HabitTaskCreateDTO, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)
    mock_create_habit_task = mocker.patch(HABIT_TASK_REPO_CREATE, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = create_habit_task(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        habit_task_dto=fake_habit_task_dto
    )

    mock_create_habit_task.assert_called_once()

    assert isinstance(result, HabitTaskReadDTO)


def test_create_habit_task_failure(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                   fake_habit_task_dto: HabitTaskCreateDTO, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)
    mocker.patch(HABIT_TASK_REPO_CREATE, side_effect=IntegrityError(None, None, Exception()))

    fake_habit_task_dto.category_id = 500

    with pytest.raises(EntityPersistenceException):
        create_habit_task(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            habit_task_dto=fake_habit_task_dto
        )


def test_update_habit_task_by_self(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                   fake_habit_task_update_dto: HabitTaskUpdateDTO, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: HabitTaskReadDTO = update_habit_task(
        requester_id=fake_habit_task_model.category.user_id,
        requester_role=UserRole.USER,
        habit_task_id=fake_habit_task_model.id,
        habit_task_updates=fake_habit_task_update_dto
    )

    assert isinstance(result, HabitTaskReadDTO)
    assert fake_habit_task_model.category_id == fake_habit_task_update_dto.category_id
    assert fake_habit_task_model.name == fake_habit_task_update_dto.name
    assert fake_habit_task_model.description == fake_habit_task_update_dto.description


def test_update_habit_task_by_different_user(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                             fake_habit_task_update_dto: HabitTaskUpdateDTO,
                                             fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))

    with pytest.raises(PermissionError):
        update_habit_task(
            requester_id=999,
            requester_role=UserRole.USER,
            habit_task_id=fake_habit_task_model.id,
            habit_task_updates=fake_habit_task_update_dto
        )


def test_update_habit_task_by_admin(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                    fake_habit_task_update_dto: HabitTaskUpdateDTO, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: HabitTaskReadDTO = update_habit_task(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        habit_task_id=fake_habit_task_model.id,
        habit_task_updates=fake_habit_task_update_dto
    )

    assert isinstance(result, HabitTaskReadDTO)
    assert fake_habit_task_model.category_id == fake_habit_task_update_dto.category_id
    assert fake_habit_task_model.name == fake_habit_task_update_dto.name
    assert fake_habit_task_model.description == fake_habit_task_update_dto.description


def test_update_non_existing_habit_task(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                        fake_habit_task_update_dto: HabitTaskUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))

    with pytest.raises(EntityNotFoundException):
        update_habit_task(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            habit_task_id=fake_habit_task_model.id,
            habit_task_updates=fake_habit_task_update_dto
        )


def test_update_habit_task_invalid_data(mocker: MockerFixture, fake_habit_task_model: HabitTask,
                                        fake_habit_task_update_dto: HabitTaskUpdateDTO):
    mocker.patch(DATABASE_SESSION_BEGIN, side_effect=IntegrityError(None, None, Exception()))

    with pytest.raises(EntityPersistenceException):
        update_habit_task(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            habit_task_id=fake_habit_task_model.id,
            habit_task_updates=fake_habit_task_update_dto
        )


def test_delete_habit_task_by_self(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = delete_habit_task(
        requester_id=fake_habit_task_model.category.user_id,
        requester_role=UserRole.USER,
        habit_task_id=fake_habit_task_model.id
    )

    assert isinstance(result, HabitTaskReadDTO)


def test_delete_habit_task_by_different_user(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))

    with pytest.raises(PermissionError):
        delete_habit_task(
            requester_id=999,
            requester_role=UserRole.USER,
            habit_task_id=fake_habit_task_model.id
        )


def test_delete_habit_task_by_admin(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = delete_habit_task(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        habit_task_id=fake_habit_task_model.id
    )

    assert isinstance(result, HabitTaskReadDTO)


def test_delete_non_existing_habit_task(mocker: MockerFixture):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))

    with pytest.raises(EntityNotFoundException):
        delete_habit_task(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            habit_task_id=123
        )


def test_delete_habit_task_calls_repository(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    session_mock = mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)
    mock_repo = mocker.patch(HABIT_TASK_REPO_DELETE, return_value=fake_habit_task_model)

    result: HabitTaskReadDTO = delete_habit_task(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        habit_task_id=fake_habit_task_model.id
    )

    assert isinstance(result, HabitTaskReadDTO)
    mock_repo.assert_called_once_with(session_mock, fake_habit_task_model)


def test_delete_habit_task_does_not_call_repository_if_wrong(mocker: MockerFixture, fake_habit_task_model: HabitTask):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))
    mock_repo = mocker.patch(HABIT_TASK_REPO_DELETE, return_value=fake_habit_task_model)

    with pytest.raises(EntityNotFoundException):
        delete_habit_task(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            habit_task_id=123
        )

    mock_repo.assert_not_called()


def test_convert_dto_to_model(fake_habit_task_dto: HabitTaskCreateDTO):
    habit_task_model: HabitTask = convert_dto_to_model(fake_habit_task_dto)

    assert habit_task_model.category_id == fake_habit_task_dto.category_id
    assert habit_task_model.name == fake_habit_task_dto.name
    assert habit_task_model.description == fake_habit_task_dto.description


def test_convert_model_to_dto(fake_habit_task_model: HabitTask):
    habit_task_dto: HabitTaskReadDTO = HabitTaskReadDTO.model_validate(fake_habit_task_model)

    assert habit_task_dto.id == fake_habit_task_model.id
    assert habit_task_dto.category_id == fake_habit_task_model.category_id
    assert habit_task_dto.name == fake_habit_task_model.name
    assert habit_task_dto.description == fake_habit_task_model.description
    assert habit_task_dto.created_at == fake_habit_task_model.created_at
    assert habit_task_dto.updated_at == fake_habit_task_model.updated_at
