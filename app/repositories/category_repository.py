from typing import Optional

from sqlalchemy.orm import Session

from app.models import Category


def get_categories(user_id: Optional[int],
                   name: Optional[str]) -> list[Category]:
    query = Category.query

    if user_id is not None:
        query = query.filter(Category.user_id == user_id)

    if name is not None:
        query = query.filter(Category.name.ilike(f"%{name}%"))

    return query.all()


def get_category_by_id(category_id: int, user_id: Optional[int]) -> Optional[Category]:
    query = Category.query.filter(Category.id == category_id)

    if user_id is not None:
        query = query.filter(Category.user_id == user_id)

    return query.first()


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


def delete_category(session: Session, category: Category) -> Category:
    session.delete(category)
    return category
