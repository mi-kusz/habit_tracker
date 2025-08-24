from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError

from app.dtos import UserReadDTO, UserCreateDTO, UserUpdateDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import User, Category
from app.models.User import UserRole
from app.services.user_service import get_users, get_user_by_id, convert_dto_to_model, get_user_by_email, create_user, \
    update_user, delete_user

DATABASE_SESSION = "app.services.user_service.database.session"
DATABASE_SESSION_BEGIN = "app.services.user_service.database.session.begin"
GET_USERS = "app.repositories.user_repository.get_users"
GET_USER_ENTITY_BY_ID = "app.services.user_service.get_user_entity_by_id"
GET_USER_ENTITY_BY_EMAIL = "app.services.user_service.get_user_entity_by_email"
USER_REPO_CREATE = "app.repositories.user_repository.create_user"
CATEGORY_REPO_CREATE_DEFAULT_CATEGORY = "app.repositories.category_repository.create_default_category_for_user"
USER_REPO_DELETE = "app.repositories.user_repository.delete_user"


def test_get_users_forbidden_for_non_admin(mocker: MockerFixture):
    mocker.patch(GET_USERS, return_value=[])

    with pytest.raises(PermissionError):
        get_users(
            1,
            UserRole.USER,
            None,
            None,
            None
        )


def test_get_users_works_for_admin(mocker: MockerFixture):
    mocker.patch(GET_USERS, return_value=[])

    get_users(
        1,
        UserRole.ADMIN,
        None,
        None,
        None
    )


def test_get_users_does_not_call_repository_if_forbidden(mocker: MockerFixture):
    mock_get_users = mocker.patch(GET_USERS, return_value=[])

    with pytest.raises(PermissionError):
        get_users(
            1,
            UserRole.USER,
            first_name=None,
            last_name=None,
            is_active="true"
        )

    mock_get_users.assert_not_called()


def test_get_users_calls_repository_with_correct_arguments(mocker: MockerFixture, fake_user_model: User):
    mock_get_users = mocker.patch(GET_USERS, return_value=[fake_user_model])

    result: list[UserReadDTO] = get_users(
        1,
        UserRole.ADMIN,
        first_name=fake_user_model.first_name,
        last_name=fake_user_model.last_name,
        is_active="true"
    )

    mock_get_users.assert_called_once_with("John", "Doe", True)

    assert len(result) == 1

    user_dto: UserReadDTO = result[0]
    assert isinstance(user_dto, UserReadDTO)


def test_get_users_calls_repository_with_none_arguments(mocker: MockerFixture, fake_user_model: User):
    mock_get_users = mocker.patch(GET_USERS, return_value=[fake_user_model])

    get_users(
        1,
        UserRole.ADMIN,
        None,
        None,
        None
    )

    mock_get_users.assert_called_once_with(None, None, None)


def test_get_users_returns_empty_list(mocker: MockerFixture):
    mocker.patch(GET_USERS, return_value=[])

    result: list[UserReadDTO] = get_users(
        1,
        UserRole.ADMIN,
        None,
        None,
        None
    )

    assert result == []


def test_get_users_returns_list_of_user_read_dto(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(GET_USERS, return_value=[fake_user_model] * 50)

    result: list[UserReadDTO] = get_users(
        1, UserRole.ADMIN,
        first_name=fake_user_model.first_name,
        last_name=fake_user_model.last_name,
        is_active="true"
    )

    assert len(result) == 50

    for user in result:
        assert isinstance(user, UserReadDTO)


def test_get_user_by_id_by_self(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    result: UserReadDTO = get_user_by_id(
        requester_id=fake_user_model.id,
        requester_role=UserRole.USER,
        user_id=fake_user_model.id
    )

    assert isinstance(result, UserReadDTO)


def test_get_user_by_id_by_different_user(fake_user_model: User):
    with pytest.raises(PermissionError):
        get_user_by_id(
            requester_id=999,
            requester_role=UserRole.USER,
            user_id=fake_user_model.id
        )


def test_get_user_by_id_by_admin(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    result: UserReadDTO = get_user_by_id(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id=fake_user_model.id
    )

    assert isinstance(result, UserReadDTO)


def test_get_user_by_id_not_found(mocker: MockerFixture):
    mocker.patch(GET_USER_ENTITY_BY_ID, side_effect=EntityNotFoundException("User"))

    with pytest.raises(EntityNotFoundException):
        get_user_by_id(
            requester_id=1,
            requester_role=UserRole.ADMIN,
            user_id=1
        )


def test_get_user_by_email_by_self(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(GET_USER_ENTITY_BY_EMAIL, return_value=fake_user_model)

    result: UserReadDTO = get_user_by_email(
        requester_id=fake_user_model.id,
        requester_role=UserRole.USER,
        email=fake_user_model.email
    )

    assert isinstance(result, UserReadDTO)


def test_get_user_by_email_by_different_user(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(GET_USER_ENTITY_BY_EMAIL, return_value=fake_user_model)

    with pytest.raises(PermissionError):
        get_user_by_email(
            requester_id=999,
            requester_role=UserRole.USER,
            email=fake_user_model.email
        )


def test_get_user_by_email_by_admin(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(GET_USER_ENTITY_BY_EMAIL, return_value=fake_user_model)

    result: UserReadDTO = get_user_by_email(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        email=fake_user_model.email
    )

    assert isinstance(result, UserReadDTO)


def test_get_user_by_email_not_found(mocker: MockerFixture):
    mocker.patch(GET_USER_ENTITY_BY_EMAIL, side_effect=EntityNotFoundException("User"))

    with pytest.raises(EntityNotFoundException):
        get_user_by_email(
            requester_id=1,
            requester_role=UserRole.ADMIN,
            email="test@test.com"
        )


def test_create_user_success(mocker: MockerFixture, fake_user_model: User, fake_user_dto: UserCreateDTO):
    session_mock = mocker.patch(DATABASE_SESSION, MagicMock())
    mock_create_user = mocker.patch(USER_REPO_CREATE, return_value=fake_user_model)
    mock_create_category = mocker.patch(CATEGORY_REPO_CREATE_DEFAULT_CATEGORY,
                                        return_value=Category(id=1, user_id=fake_user_model.id, name="Default"))

    result: UserReadDTO = create_user(fake_user_dto)

    mock_create_user.assert_called_once()
    mock_create_category.assert_called_once_with(session_mock, fake_user_model.id)

    assert isinstance(result, UserReadDTO)


def test_create_user_failure(mocker: MockerFixture, fake_user_model: User, fake_user_dto: UserCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(USER_REPO_CREATE, side_effect=IntegrityError(None, None, Exception()))

    with pytest.raises(EntityPersistenceException):
        create_user(fake_user_dto)


def test_update_user_by_self(mocker: MockerFixture, fake_user_model: User, fake_user_update_dto: UserUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    result: UserReadDTO = update_user(
        requester_id=fake_user_model.id,
        requester_role=UserRole.USER,
        user_id=fake_user_model.id,
        user_updates=fake_user_update_dto
    )

    assert isinstance(result, UserReadDTO)
    assert fake_user_model.first_name == fake_user_update_dto.first_name
    assert fake_user_model.last_name == fake_user_update_dto.last_name


def test_update_user_by_different_user(fake_user_model: User, fake_user_update_dto: UserUpdateDTO):
    with pytest.raises(PermissionError):
        update_user(
            requester_id=999,
            requester_role=UserRole.USER,
            user_id=fake_user_model.id,
            user_updates=fake_user_update_dto
        )


def test_update_user_by_admin(mocker: MockerFixture, fake_user_model: User, fake_user_update_dto: UserUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    result: UserReadDTO = update_user(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id=fake_user_model.id,
        user_updates=fake_user_update_dto
    )

    assert isinstance(result, UserReadDTO)
    assert fake_user_model.first_name == fake_user_update_dto.first_name
    assert fake_user_model.last_name == fake_user_update_dto.last_name


@pytest.mark.skip
def test_update_user_invalid_data(mocker: MockerFixture, fake_user_model: User, fake_user_update_dto: UserUpdateDTO):
    mocker.patch(DATABASE_SESSION_BEGIN, side_effect=IntegrityError(None, None, Exception()))
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    with pytest.raises(EntityPersistenceException):
        update_user(
            requester_id=1,
            requester_role=UserRole.ADMIN,
            user_id=fake_user_model.id,
            user_updates=fake_user_update_dto
        )


def test_update_non_existing_user(mocker: MockerFixture, fake_user_model: User, fake_user_update_dto: UserUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, side_effect=EntityNotFoundException("User"))

    with pytest.raises(EntityNotFoundException):
        update_user(
            requester_id=1,
            requester_role=UserRole.ADMIN,
            user_id=999,
            user_updates=fake_user_update_dto
        )


def test_delete_user_by_self(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    result: UserReadDTO = delete_user(
        requester_id=fake_user_model.id,
        requester_role=UserRole.USER,
        user_id=fake_user_model.id
    )

    assert isinstance(result, UserReadDTO)


def test_delete_user_by_different_user(fake_user_model: User):
    with pytest.raises(PermissionError):
        delete_user(
            requester_id=999,
            requester_role=UserRole.USER,
            user_id=fake_user_model.id
        )


def test_delete_user_by_admin(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)

    result: UserReadDTO = delete_user(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id=fake_user_model.id
    )

    assert isinstance(result, UserReadDTO)


def test_delete_non_existing_user(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, side_effect=EntityNotFoundException("User"))

    with pytest.raises(EntityNotFoundException):
        delete_user(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            user_id=fake_user_model.id
        )


@pytest.mark.skip
def test_delete_user_calls_repository(mocker: MockerFixture, fake_user_model: User):
    session_mock = mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, return_value=fake_user_model)
    mock_repo = mocker.patch(USER_REPO_DELETE, return_value=fake_user_model)

    result: UserReadDTO = delete_user(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        user_id=fake_user_model.id
    )

    assert isinstance(result, UserReadDTO)
    assert mock_repo.assert_called_once_with(session_mock, fake_user_model)


def test_delete_user_does_not_call_repository_if_wrong(mocker: MockerFixture, fake_user_model: User):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_USER_ENTITY_BY_ID, side_effect=EntityNotFoundException("User"))
    mock_repo = mocker.patch(USER_REPO_DELETE, return_value=fake_user_model)

    with pytest.raises(EntityNotFoundException):
        delete_user(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            user_id=fake_user_model.id
        )

    mock_repo.assert_not_called()


def test_convert_dto_to_model(fake_user_dto: UserCreateDTO):
    user_model: User = convert_dto_to_model(fake_user_dto)

    assert user_model.first_name == fake_user_dto.first_name
    assert user_model.last_name == fake_user_dto.last_name
    assert user_model.email == fake_user_dto.email
    assert user_model.check_password(fake_user_dto.password)
    assert user_model.role == fake_user_dto.role


def test_convert_model_to_dto(fake_user_model: User):
    user_dto: UserReadDTO = UserReadDTO.model_validate(fake_user_model)

    assert user_dto.id == fake_user_model.id
    assert user_dto.first_name == fake_user_model.first_name
    assert user_dto.last_name == fake_user_model.last_name
    assert user_dto.email == fake_user_model.email
    assert user_dto.is_active == fake_user_model.is_active
    assert user_dto.created_at == fake_user_model.created_at
    assert user_dto.updated_at == fake_user_model.updated_at
