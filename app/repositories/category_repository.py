from app import database
from app.models import Category


def get_categories() -> list[Category]:
    return Category.query.all()


def get_category_by_id(category_id: int) -> Category:
    return Category.query.get(category_id)


def create_category(category: Category) -> Category:
    database.session.add(category)
    database.session.commit()
    return category


def update_category(category: Category) -> Category:
    database.session.commit()
    return category
