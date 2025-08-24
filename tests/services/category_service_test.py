from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError

from app.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryUpdateDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import Category
from app.models.User import UserRole
from app.services.category_service import get_categories, convert_dto_to_model, get_category_by_id, create_category, \
    update_category, delete_category

DATABASE_SESSION = "app.services.category_service.database.session"
DATABASE_SESSION_BEGIN = "app.services.category_service.database.session.begin"
GET_CATEGORIES = "app.repositories.category_repository.get_categories"
GET_CATEGORY_ENTITY = "app.services.category_service.get_category_entity"
CATEGORY_REPO_CREATE = "app.repositories.category_repository.create_category"
CATEGORY_REPO_DELETE = "app.repositories.category_repository.delete_category"


def test_get_categories_by_self(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(GET_CATEGORIES, return_value=[fake_category_model])

    result: list[CategoryReadDTO] = get_categories(
        requester_id=1,
        requester_role=UserRole.USER,
        user_id=None,
        name=None
    )

    assert len(result) == 1

    category_dto: CategoryReadDTO = result[0]
    assert isinstance(category_dto, CategoryReadDTO)


def test_get_categories_by_different_user(mocker: MockerFixture):
    mocker.patch(GET_CATEGORIES, return_value=[])

    with pytest.raises(PermissionError):
        get_categories(
            requester_id=1,
            requester_role=UserRole.USER,
            user_id="2",
            name=None
        )


def test_get_categories_by_admin(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(GET_CATEGORIES, return_value=[fake_category_model])

    result: list[CategoryReadDTO] = get_categories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id="2",
        name=None
    )

    assert len(result) == 1

    category_dto: CategoryReadDTO = result[0]
    assert isinstance(category_dto, CategoryReadDTO)


def test_get_categories_does_not_call_repository_if_forbidden(mocker: MockerFixture):
    mock_get_categories = mocker.patch(GET_CATEGORIES, return_value=[])

    with pytest.raises(PermissionError):
        get_categories(
            requester_id=1,
            requester_role=UserRole.USER,
            user_id="2",
            name=None
        )

    mock_get_categories.assert_not_called()


def test_get_categories_calls_repository_with_correct_arguments(mocker: MockerFixture, fake_category_model: Category):
    mock_get_categories = mocker.patch(GET_CATEGORIES, return_value=[fake_category_model])

    result: list[CategoryReadDTO] = get_categories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id="2",
        name="Name"
    )

    mock_get_categories.assert_called_once_with(2, "Name")

    assert len(result) == 1

    category_dto: CategoryReadDTO = result[0]
    assert isinstance(category_dto, CategoryReadDTO)


def test_get_categories_calls_repository_with_none_arguments(mocker: MockerFixture, fake_category_model: Category):
    mock_get_categories = mocker.patch(GET_CATEGORIES, return_value=[fake_category_model])

    get_categories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id=None,
        name=None
    )

    mock_get_categories.assert_called_once_with(None, None)


def test_get_categories_returns_empty_list(mocker: MockerFixture):
    mocker.patch(GET_CATEGORIES, return_value=[])

    result: list[CategoryReadDTO] = get_categories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id="2",
        name="Name"
    )

    assert result == []


def test_get_categories_returns_list_of_category_read_dto(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(GET_CATEGORIES, return_value=[fake_category_model] * 50)

    result: list[CategoryReadDTO] = get_categories(
        requester_id=1,
        requester_role=UserRole.ADMIN,
        user_id="2",
        name="Name"
    )

    assert len(result) == 50

    for category in result:
        assert isinstance(category, CategoryReadDTO)


def test_get_category_by_id_by_self(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: CategoryReadDTO = get_category_by_id(
        requester_id=1,
        requester_role=UserRole.USER,
        category_id=1
    )

    assert isinstance(result, CategoryReadDTO)


def test_get_category_by_id_by_different_user(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    with pytest.raises(PermissionError):
        get_category_by_id(
            requester_id=999,
            requester_role=UserRole.USER,
            category_id=1
        )


def test_get_category_by_id_by_admin(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: CategoryReadDTO = get_category_by_id(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        category_id=1
    )

    assert isinstance(result, CategoryReadDTO)


def test_get_category_by_id_not_found(mocker: MockerFixture):
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))

    with pytest.raises(EntityNotFoundException):
        get_category_by_id(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            category_id=1
        )


def test_create_category_by_self(mocker: MockerFixture, fake_category_model: Category,
                                 fake_category_dto: CategoryCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mock_create_category = mocker.patch(CATEGORY_REPO_CREATE, return_value=fake_category_model)

    result: CategoryReadDTO = create_category(
        requester_id=fake_category_dto.user_id,
        requester_role=UserRole.USER,
        category_dto=fake_category_dto
    )

    mock_create_category.assert_called_once()

    assert isinstance(result, CategoryReadDTO)


def test_create_category_by_different_user(fake_category_dto: CategoryCreateDTO):
    with pytest.raises(PermissionError):
        create_category(
            requester_id=999,
            requester_role=UserRole.USER,
            category_dto=fake_category_dto
        )


def test_create_category_by_admin(mocker: MockerFixture, fake_category_model: Category,
                                  fake_category_dto: CategoryCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mock_create_category = mocker.patch(CATEGORY_REPO_CREATE, return_value=fake_category_model)

    result: CategoryReadDTO = create_category(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        category_dto=fake_category_dto
    )

    mock_create_category.assert_called_once()

    assert isinstance(result, CategoryReadDTO)


def test_create_category_failure(mocker: MockerFixture, fake_category_dto: CategoryCreateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(CATEGORY_REPO_CREATE, side_effect=IntegrityError(None, None, Exception()))

    fake_category_dto.user_id = 500

    with pytest.raises(EntityPersistenceException):
        create_category(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            category_dto=fake_category_dto
        )


def test_update_category_by_self(mocker: MockerFixture, fake_category_model: Category,
                                 fake_category_update_dto: CategoryUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: CategoryReadDTO = update_category(
        requester_id=fake_category_model.user_id,
        requester_role=UserRole.USER,
        category_id=fake_category_model.id,
        category_updates=fake_category_update_dto
    )

    assert isinstance(result, CategoryReadDTO)
    assert fake_category_model.name == fake_category_update_dto.name
    assert fake_category_model.description == fake_category_update_dto.description


def test_update_category_by_different_user(mocker: MockerFixture, fake_category_model: Category,
                                           fake_category_update_dto: CategoryUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))

    with pytest.raises(PermissionError):
        update_category(
            requester_id=999,
            requester_role=UserRole.USER,
            category_id=fake_category_model.id,
            category_updates=fake_category_update_dto
        )


def test_update_category_by_admin(mocker: MockerFixture, fake_category_model: Category,
                                  fake_category_update_dto: CategoryUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: CategoryReadDTO = update_category(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        category_id=fake_category_model.id,
        category_updates=fake_category_update_dto
    )

    assert isinstance(result, CategoryReadDTO)
    assert fake_category_model.name == fake_category_update_dto.name
    assert fake_category_model.description == fake_category_update_dto.description


def test_update_non_existing_category(mocker: MockerFixture, fake_category_model: Category,
                                      fake_category_update_dto: CategoryUpdateDTO):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))

    with pytest.raises(EntityNotFoundException):
        update_category(
            requester_id=1,
            requester_role=UserRole.ADMIN,
            category_id=fake_category_model.id,
            category_updates=fake_category_update_dto
        )


def test_update_category_invalid_data(mocker: MockerFixture, fake_category_model: Category,
                                      fake_category_update_dto: CategoryUpdateDTO):
    mocker.patch(DATABASE_SESSION_BEGIN, side_effect=IntegrityError(None, None, Exception()))

    with pytest.raises(EntityPersistenceException):
        update_category(
            requester_id=1,
            requester_role=UserRole.ADMIN,
            category_id=fake_category_model.id,
            category_updates=fake_category_update_dto
        )


def test_delete_category_by_self(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: CategoryReadDTO = delete_category(
        requester_id=fake_category_model.user_id,
        requester_role=UserRole.USER,
        category_id=fake_category_model.id
    )

    assert isinstance(result, CategoryReadDTO)


def test_delete_category_by_different_user(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))

    with pytest.raises(PermissionError):
        delete_category(
            requester_id=999,
            requester_role=UserRole.USER,
            category_id=fake_category_model.id
        )


def test_delete_category_by_admin(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)

    result: CategoryReadDTO = delete_category(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        category_id=fake_category_model.id
    )

    assert isinstance(result, CategoryReadDTO)


def test_delete_non_existing_category(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))

    with pytest.raises(EntityNotFoundException):
        delete_category(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            category_id=fake_category_model.id
        )


def test_delete_category_calls_repository(mocker: MockerFixture, fake_category_model: Category):
    session_mock = mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, return_value=fake_category_model)
    mock_repo = mocker.patch(CATEGORY_REPO_DELETE, return_value=fake_category_model)

    result: CategoryReadDTO = delete_category(
        requester_id=999,
        requester_role=UserRole.ADMIN,
        category_id=fake_category_model.id
    )

    assert isinstance(result, CategoryReadDTO)
    mock_repo.assert_called_once_with(session_mock, fake_category_model)


def test_delete_category_does_not_call_repository_if_wrong(mocker: MockerFixture, fake_category_model: Category):
    mocker.patch(DATABASE_SESSION, MagicMock())
    mocker.patch(GET_CATEGORY_ENTITY, side_effect=EntityNotFoundException("Category"))
    mock_repo = mocker.patch(CATEGORY_REPO_DELETE, return_value=fake_category_model)

    with pytest.raises(EntityNotFoundException):
        delete_category(
            requester_id=999,
            requester_role=UserRole.ADMIN,
            category_id=fake_category_model.id
        )

    mock_repo.assert_not_called()


def test_convert_dto_to_model(fake_category_dto: CategoryCreateDTO):
    category_model: Category = convert_dto_to_model(fake_category_dto)

    assert category_model.user_id == fake_category_dto.user_id
    assert category_model.name == fake_category_dto.name
    assert category_model.description == fake_category_dto.description


def test_convert_model_to_dto(fake_category_model: Category):
    category_dto: CategoryReadDTO = CategoryReadDTO.model_validate(fake_category_model)

    assert category_dto.id == fake_category_model.id
    assert category_dto.user_id == fake_category_model.user_id
    assert category_dto.name == fake_category_model.name
    assert category_dto.description == fake_category_model.description
    assert category_dto.created_at == fake_category_model.created_at
    assert category_dto.updated_at == fake_category_model.updated_at
