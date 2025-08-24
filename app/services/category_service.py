from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryUpdateDTO
from app.exceptions.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import Category
from app.models.User import UserRole
from app.repositories import category_repository
from app.utils import str_to_int_or_none

entity_type: str = "Category"


def get_categories(requester_id: int,
                   requester_role: UserRole,
                   user_id: Optional[str],
                   name: Optional[str]) -> list[CategoryReadDTO]:
    user_id_int: Optional[int] = str_to_int_or_none(user_id)

    # If user does not pass user_id parameter, it is taken from requester_id
    if requester_role == UserRole.USER and user_id_int is None:
        user_id_int = requester_id

    if requester_role != UserRole.ADMIN and requester_id != user_id_int:
        raise PermissionError("Forbidden")

    categories: list[Category] = category_repository.get_categories(user_id_int, name)

    return [CategoryReadDTO.model_validate(category) for category in categories]


def get_category_by_id(requester_id: int,
                       requester_role: UserRole,
                       category_id: int) -> CategoryReadDTO:
    try:
        category: Category = get_category_entity(category_id)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    if requester_role != UserRole.ADMIN and requester_id != category.user_id:
        raise PermissionError("Forbidden")

    return CategoryReadDTO.model_validate(category)


def create_category(requester_id: int,
                    requester_role: UserRole,
                    category_dto: CategoryCreateDTO) -> CategoryReadDTO:
    if requester_role != UserRole.ADMIN and requester_id != category_dto.user_id:
        raise PermissionError("Forbidden")

    category: Category = convert_dto_to_model(category_dto)

    try:
        with database.session.begin():
            created_category: Category = category_repository.create_category(database.session, category)
    except IntegrityError:
        raise EntityPersistenceException(entity_type)

    return CategoryReadDTO.model_validate(created_category)


def update_category(requester_id: int,
                    requester_role: UserRole,
                    category_id: int,
                    category_updates: CategoryUpdateDTO) -> CategoryReadDTO:
    updates: dict = category_updates.model_dump(exclude_unset=True)

    try:
        with database.session.begin():
            if requester_role == UserRole.ADMIN:
                category: Category = get_category_entity(category_id)
            else:
                category: Category = get_category_entity(category_id, requester_id)

            for field, value in updates.items():
                if hasattr(category, field):
                    setattr(category, field, value)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")
    except IntegrityError:
        raise EntityPersistenceException(entity_type)

    return CategoryReadDTO.model_validate(category)


def delete_category(requester_id: int,
                    requester_role: UserRole,
                    category_id: int) -> CategoryReadDTO:
    try:
        with database.session.begin():
            if requester_role == UserRole.ADMIN:
                category: Category = get_category_entity(category_id)
            else:
                category: Category = get_category_entity(category_id, requester_id)

            category_repository.delete_category(database.session, category)
    except EntityNotFoundException as e:
        if requester_role == UserRole.ADMIN:
            raise e
        else:
            raise PermissionError("Forbidden")

    return CategoryReadDTO.model_validate(category)


def convert_dto_to_model(category_dto: CategoryCreateDTO) -> Category:
    return Category(
        user_id=category_dto.user_id,
        name=category_dto.name,
        description=category_dto.description
    )


def get_category_entity(category_id: int, user_id: Optional[int] = None) -> Category:
    category: Optional[Category] = category_repository.get_category_by_id(category_id, user_id)

    if category is None:
        raise EntityNotFoundException(entity_type)

    return category
