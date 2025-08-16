from typing import Optional

from sqlalchemy.orm import Session

from app.models import Category


def get_categories() -> list[Category]:
    return Category.query.all()


def get_category_by_id(category_id: int) -> Optional[Category]:
    return Category.query.get(category_id)


def create_category(session: Session, category: Category) -> Category:
    session.add(category)
    return category


def create_default_category_for_user(session: Session, user_id: int) -> Category:
    category = Category(
        user_id=user_id,
        name="Default",
        description="Default category created on user creation"
    )

    session.add(category)
    return category