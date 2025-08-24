from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError

from app.dtos import ExecutionHistoryReadDTO, ExecutionHistoryCreateDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import ExecutionHistory, HabitTask
from app.models.User import UserRole
from app.services.execution_history_service import get_execution_histories, get_execution_history_by_id, \
    create_execution_history, delete_execution_history, convert_dto_to_model
from app.utils import str_to_datetime_or_none

DATABASE_SESSION = "app.services.habit_task_service.database.session"
DATABASE_SESSION_BEGIN = "app.services.habit_task_service.database.session.begin"
GET_EXECUTION_HISTORIES = "app.repositories.execution_history_repository.get_execution_histories"
GET_EXECUTION_HISTORY_ENTITY = "app.services.execution_history_service.get_execution_history_entity"
EXECUTION_HISTORY_REPO_CREATE = "app.repositories.execution_history_repository.create_execution_history"
EXECUTION_HISTORY_REPO_DELETE = "app.repositories.execution_history_repository.delete_execution_history"
GET_HABIT_TASK_ENTITY = "app.services.execution_history_service.get_habit_task_entity"


def test_get_execution_histories_by_self(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory):
    mocker.patch(GET_EXECUTION_HISTORIES, return_value=[fake_execution_history_model])

    result: list[ExecutionHistoryReadDTO] = get_execution_histories(
        requester_id=1,
        requester_role=UserRole.USER,
        user_id=None,
        category_id=None,
        habit_task_id=None,
        start_datetime=None,
        end_datetime=None
    )

    assert len(result) == 1

    execution_history_dto: ExecutionHistoryReadDTO = result[0]
    assert isinstance(execution_history_dto, ExecutionHistoryReadDTO)


def test_get_execution_histories_by_different_user(mocker: MockerFixture):
    mocker.patch(GET_EXECUTION_HISTORIES, return_value=[])

    with pytest.raises(PermissionError):
        get_execution_histories(
            requester_id=999,
            requester_role=UserRole.USER,
            user_id="1",
            category_id=None,
            habit_task_id=None,
            start_datetime=None,
            end_datetime=None
        )


def test_get_execution_histories_by_admin(mocker: MockerFixture, fake_execution_history_model: HabitTask):
    mocker.patch(GET_EXECUTION_HISTORIES, return_value=[fake_execution_history_model])

    result: list[ExecutionHistoryReadDTO] = get_execution_histories(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id="1",
        category_id=None,
        habit_task_id=None,
        start_datetime=None,
        end_datetime=None
    )

    assert len(result) == 1

    execution_history_dto: ExecutionHistoryReadDTO = result[0]
    assert isinstance(execution_history_dto, ExecutionHistoryReadDTO)


def test_get_execution_histories_does_not_call_repository_if_forbidden(mocker: MockerFixture):
    mock_get_execution_histories = mocker.patch(GET_EXECUTION_HISTORIES, return_value=[])

    with pytest.raises(PermissionError):
        get_execution_histories(
            requester_id=999,
            requester_role=UserRole.USER,
            user_id="1",
            category_id=None,
            habit_task_id=None,
            start_datetime=None,
            end_datetime=None
        )

    mock_get_execution_histories.assert_not_called()


def test_get_execution_histories_calls_repository_with_correct_arguments(mocker: MockerFixture,
                                                                         fake_execution_history_model: ExecutionHistory):
    mock_get_execution_histories = mocker.patch(GET_EXECUTION_HISTORIES, return_value=[fake_execution_history_model])

    result: list[ExecutionHistoryReadDTO] = get_execution_histories(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id="1",
        category_id="1",
        habit_task_id="1",
        start_datetime="2020-01-01 00:00:00",
        end_datetime="2021-01-01 00:00:00"
    )

    mock_get_execution_histories.assert_called_once_with(1, 1, 1,
                                                         str_to_datetime_or_none("2020-01-01 00:00:00"),
                                                         str_to_datetime_or_none("2021-01-01 00:00:00"))

    assert len(result) == 1

    execution_history_dto: ExecutionHistoryReadDTO = result[0]
    assert isinstance(execution_history_dto, ExecutionHistoryReadDTO)


def test_get_execution_histories_calls_repository_with_none_arguments(mocker: MockerFixture):
    mock_get_execution_histories = mocker.patch(GET_EXECUTION_HISTORIES, return_value=[])

    get_execution_histories(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id=None,
        category_id=None,
        habit_task_id=None,
        start_datetime=None,
        end_datetime=None
    )

    mock_get_execution_histories.assert_called_once_with(None, None, None, None, None)


def test_get_execution_histories_returns_empty_list(mocker: MockerFixture):
    mocker.patch(GET_EXECUTION_HISTORIES, return_value=[])

    result: list[ExecutionHistoryReadDTO] = get_execution_histories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id=None,
        category_id=None,
        habit_task_id=None,
        start_datetime=None,
        end_datetime=None
    )

    assert result == []


def test_get_execution_histories_returns_list_of_execution_history_read_dto(mocker: MockerFixture,
                                                                            fake_execution_history_model: ExecutionHistory):
    mocker.patch(GET_EXECUTION_HISTORIES, return_value=[fake_execution_history_model] * 50)

    result: list[ExecutionHistoryReadDTO] = get_execution_histories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id=None,
        category_id=None,
        habit_task_id=None,
        start_datetime=None,
        end_datetime=None
    )

    assert len(result) == 50

    for execution_history in result:
        assert isinstance(execution_history, ExecutionHistoryReadDTO)


def test_get_execution_history_by_id_by_self(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory):
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = get_execution_history_by_id(
        requester_id=1,
        requester_role=UserRole.USER,
        execution_history_id=1
    )

    assert isinstance(result, ExecutionHistoryReadDTO)


def test_get_execution_history_by_id_by_different_user(mocker: MockerFixture,
                                                       fake_execution_history_model: ExecutionHistory):
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, return_value=fake_execution_history_model)

    with pytest.raises(PermissionError):
        get_execution_history_by_id(
            requester_id=999,
            requester_role=UserRole.USER,
            execution_history_id=1
        )


def test_get_execution_history_by_id_by_admin(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory):
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = get_execution_history_by_id(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        execution_history_id=1
    )

    assert isinstance(result, ExecutionHistoryReadDTO)


def test_get_execution_history_by_id_not_found(mocker: MockerFixture):
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, side_effect=EntityNotFoundException("Execution History"))

    with pytest.raises(EntityNotFoundException):
        get_execution_history_by_id(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            execution_history_id=1
        )


def test_create_execution_history_by_self(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory,
                                          fake_execution_history_dto: ExecutionHistoryCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mock_create_execution_history = mocker.patch(EXECUTION_HISTORY_REPO_CREATE,
                                                 return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = create_execution_history(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        execution_history_dto=fake_execution_history_dto
    )

    mock_create_execution_history.assert_called_once()

    assert isinstance(result, ExecutionHistoryReadDTO)


def test_create_execution_history_by_different_user(mocker: MockerFixture,
                                                    fake_execution_history_model: ExecutionHistory,
                                                    fake_execution_history_dto: ExecutionHistoryCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, side_effect=EntityNotFoundException("Habit Task"))

    with pytest.raises(PermissionError):
        create_execution_history(
            requester_id=999,
            requester_role=UserRole.USER,
            execution_history_dto=fake_execution_history_dto
        )


def test_create_execution_history_by_admin(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory,
                                           fake_execution_history_dto: ExecutionHistoryCreateDTO,
                                           fake_habit_task_model: HabitTask):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)
    mock_create_execution_history = mocker.patch(EXECUTION_HISTORY_REPO_CREATE,
                                                 return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = create_execution_history(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        execution_history_dto=fake_execution_history_dto
    )

    mock_create_execution_history.assert_called_once()

    assert isinstance(result, ExecutionHistoryReadDTO)


def test_create_execution_history_failure(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory,
                                          fake_execution_history_dto: ExecutionHistoryCreateDTO,
                                          fake_habit_task_model: HabitTask):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_HABIT_TASK_ENTITY, return_value=fake_habit_task_model)
    mocker.patch(EXECUTION_HISTORY_REPO_CREATE,
                 side_effect=IntegrityError(None, None, Exception()))

    fake_execution_history_dto.habit_task_id = 500

    with pytest.raises(EntityPersistenceException):
        create_execution_history(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            execution_history_dto=fake_execution_history_dto
        )


def test_delete_execution_history_by_self(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = delete_execution_history(
        requester_id=fake_execution_history_model.habit_task.category.user_id,
        requester_role=UserRole.USER,
        execution_history_id=fake_execution_history_model.id
    )

    assert isinstance(result, ExecutionHistoryReadDTO)


def test_delete_execution_history_by_different_user(mocker: MockerFixture,
                                                    fake_execution_history_model: ExecutionHistory):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, side_effect=EntityNotFoundException("Execution History"))

    with pytest.raises(PermissionError):
        delete_execution_history(
            requester_id=999,
            requester_role=UserRole.USER,
            execution_history_id=fake_execution_history_model.id
        )


def test_delete_execution_history_by_admin(mocker: MockerFixture, fake_execution_history_model: ExecutionHistory):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = delete_execution_history(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        execution_history_id=fake_execution_history_model.id
    )

    assert isinstance(result, ExecutionHistoryReadDTO)


def test_delete_non_existing_execution_history(mocker: MockerFixture):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, side_effect=EntityNotFoundException("Execution History"))

    with pytest.raises(EntityNotFoundException):
        delete_execution_history(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            execution_history_id=123
        )


def test_delete_execution_history_calls_repository(mocker: MockerFixture,
                                                   fake_execution_history_model: ExecutionHistory):
    session_mock = mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, return_value=fake_execution_history_model)
    mock_repo = mocker.patch(EXECUTION_HISTORY_REPO_DELETE, return_value=fake_execution_history_model)

    result: ExecutionHistoryReadDTO = delete_execution_history(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        execution_history_id=fake_execution_history_model.id
    )

    assert isinstance(result, ExecutionHistoryReadDTO)
    mock_repo.assert_called_once_with(session_mock, fake_execution_history_model)


def test_delete_execution_history_does_not_call_repository_if_wrong(mocker: MockerFixture,
                                                                    fake_execution_history_model: ExecutionHistory):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_EXECUTION_HISTORY_ENTITY, side_effect=EntityNotFoundException("Execution History"))
    mock_repo = mocker.patch(EXECUTION_HISTORY_REPO_DELETE, return_value=fake_execution_history_model)

    with pytest.raises(EntityNotFoundException):
        delete_execution_history(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            execution_history_id=123
        )

    mock_repo.assert_not_called()


def test_convert_dto_to_model(fake_execution_history_dto: ExecutionHistoryCreateDTO):
    execution_history_model: ExecutionHistory = convert_dto_to_model(fake_execution_history_dto)

    assert execution_history_model.habit_task_id == fake_execution_history_dto.habit_task_id
    assert execution_history_model.executed_at == fake_execution_history_dto.executed_at


def test_convert_model_to_dto(fake_execution_history_model: ExecutionHistory):
    execution_history_dto: ExecutionHistoryReadDTO = ExecutionHistoryReadDTO.model_validate(
        fake_execution_history_model)

    assert execution_history_dto.id == fake_execution_history_model.id
    assert execution_history_dto.habit_task_id == fake_execution_history_model.habit_task_id
    assert execution_history_dto.executed_at == fake_execution_history_model.executed_at
