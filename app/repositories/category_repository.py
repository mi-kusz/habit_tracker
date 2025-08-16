from typing import Optional

from sqlalchemy.exc import IntegrityError

from app import database
from app.exceptions import EntityNotFoundException, EntityPersistenceException
from app.models import Category

entity_type: str = "Category"


def get_categories() -> list[Category]:
    return Category.query.all()


def get_category_by_id(category_id: int) -> Category:
    category: Optional[Category] = Category.query.get(category_id)

    if category is None:
        raise EntityNotFoundException(entity_type)

    return category


def create_category(category: Category) -> Category:
    try:
        database.session.add(category)
        database.session.commit()
        return category
    except IntegrityError:
        database.session.rollback()
        raise EntityPersistenceException(entity_type)


def update_category(category: Category) -> Category:
    try:
        database.session.commit()
        return category
    except IntegrityError:
        database.session.rollback()
        raise EntityPersistenceException(entity_type)
