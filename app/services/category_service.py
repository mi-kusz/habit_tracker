from app.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryUpdateDTO
from app.models import Category
from app.repositories import category_repository


def get_categories() -> list[CategoryReadDTO]:
    categories: list[Category] = category_repository.get_categories()

    return [CategoryReadDTO.model_validate(category) for category in categories]


def get_category_by_id(category_id) -> CategoryReadDTO:
    category: Category = category_repository.get_category_by_id(category_id)

    return CategoryReadDTO.model_validate(category)


def create_category(category_dto: CategoryCreateDTO) -> CategoryReadDTO:
    category: Category = convert_dto_to_model(category_dto)

    created_category: Category = category_repository.create_category(category)

    return CategoryReadDTO.model_validate(created_category)


def update_category(category_id: int, category_updates: CategoryUpdateDTO) -> CategoryReadDTO:
    category: Category = category_repository.get_category_by_id(category_id)

    if category_updates.name is not None:
        category.name = category_updates.name

    if category_updates.description is not None:
        category.description = category_updates.description

    updated_category: Category = category_repository.update_category(category)

    return CategoryReadDTO.model_validate(updated_category)


def convert_dto_to_model(category_dto: CategoryCreateDTO) -> Category:
    return Category(
        user_id=category_dto.user_id,
        name=category_dto.name,
        description=category_dto.description
    )
