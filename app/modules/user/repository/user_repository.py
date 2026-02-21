from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Sequence
from app.modules.user.models.user_model import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(
        self,
        page: int | None = None,
        limit: int | None = None,
        email: str | None = None,
    ) -> tuple[Sequence[User], int]:
        stmt = select(User)

        if email:
            stmt = stmt.where(User.email.ilike(f"%{email}%"))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.execute(count_stmt).scalar_one()

        if page is not None and limit is not None:
            offset = (page - 1) * limit
            stmt = stmt.offset(offset).limit(limit)

        users = self.session.execute(stmt).scalars().all()

        return users, total

    def add(self, user: User) -> None:
        self.session.add(user)

    def update(self, user_id: int, data: dict) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = self.session.execute(stmt).scalar_one_or_none()

        if not user:
            return None

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        return user

    def delete(self, user_id: int) -> bool:
        stmt = select(User).where(User.id == user_id)
        user = self.session.execute(stmt).scalar_one_or_none()

        if not user:
            return False

        self.session.delete(user)
        return True
