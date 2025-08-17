from typing import Optional

from sqlalchemy.exc import IntegrityError
from app import database

from app.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryUpdateDTO
from app.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import Category
from app.repositories import category_repository

entity_type: str = "Category"


def get_categories() -> list[CategoryReadDTO]:
    categories: list[Category] = category_repository.get_categories()

    return [CategoryReadDTO.model_validate(category) for category in categories]


def get_category_by_id(category_id: int) -> CategoryReadDTO:
    category: Category = get_category_entity(category_id)

    return CategoryReadDTO.model_validate(category)


def create_category(category_dto: CategoryCreateDTO) -> CategoryReadDTO:
    category: Category = convert_dto_to_model(category_dto)

    try:
        with database.session.begin():
            created_category: Category = category_repository.create_category(database.session, category)

        return CategoryReadDTO.model_validate(created_category)
    except IntegrityError:
        raise EntityPersistenceException(entity_type)


def update_category(category_id: int, category_updates: CategoryUpdateDTO) -> CategoryReadDTO:
    with database.session.begin():
        category: Category = get_category_entity(category_id)

        if category_updates.name is not None:
            category.name = category_updates.name

        if category_updates.description is not None:
            category.description = category_updates.description

    return CategoryReadDTO.model_validate(category)


def delete_category(category_id: int) -> CategoryReadDTO:
    category: Category = get_category_entity(category_id)

    with database.session.begin():
        category_repository.delete_category(database.session, category)

    return CategoryReadDTO.model_validate(category)


def convert_dto_to_model(category_dto: CategoryCreateDTO) -> Category:
    return Category(
        user_id=category_dto.user_id,
        name=category_dto.name,
        description=category_dto.description
    )


def get_category_entity(category_id: int) -> Category:
    category: Optional[Category] = category_repository.get_category_by_id(category_id)

    if category is None:
        raise EntityNotFoundException(entity_type)

    return category