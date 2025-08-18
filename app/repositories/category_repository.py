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


def delete_category(session: Session, category: Category) -> Category:
    session.delete(category)
    return category


def get_categories_by_user_id(session: Session, user_id: int) -> list[Category]:
    return session.query(Category).filter(Category.user_id == user_id).all()


def get_categories_by_name(session: Session, name: str) -> list[Category]:
    return session.query(Category).filter(Category.name.ilike(f"%{name}%")).all()


def get_categories_by_user_and_name(session: Session, user_id: int, name: str) -> list[Category]:
    query = session.query(Category)
    query = query.filter(Category.user_id == user_id)
    query = query.filter(Category.name.ilike(f"%{name}%"))

    return query.all()
