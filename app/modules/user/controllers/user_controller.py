import re
import math
from sqlalchemy.orm import Session
from app.modules.user.repository.user_repository import UserRepository
from app.modules.user.models.user_model import User
from app.shared.exceptions import BadRequestError, NotFoundError, ConflictError


class UserController:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UserRepository(session)

    def _validate_required_fields(self, data: dict):
        required_fields = ["name", "lastname", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise BadRequestError(f"{field} is required")

    def _validate_email_format(self, email: str):
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, email):
            raise BadRequestError("Invalid email format")

    def create_user(self, data: dict) -> User:
        self._validate_required_fields(data)
        self._validate_email_format(data["email"])

        if self.repo.get_by_email(data["email"]):
            raise ConflictError("Email already exists")

        user = User(**data)
        self.repo.add(user)

        self.session.commit()
        self.session.refresh(user)

        return user

    def update_user(self, user_id: int, data: dict) -> User:
        if not user_id:
            raise BadRequestError("user_id is required")

        if not data:
            raise BadRequestError("The payload is empty")

        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        self._validate_required_fields(data)
        self._validate_email_format(data["email"])

        existing = self.repo.get_by_email(data["email"])
        if existing and existing.id != user_id:
            raise ConflictError("Email already exists")

        updated_user = self.repo.update(user_id, data)

        self.session.commit()
        self.session.refresh(updated_user)

        return updated_user

    def delete_user(self, user_id: int) -> None:
        deleted = self.repo.delete(user_id)
        if not deleted:
            raise NotFoundError("User not found")

        self.session.commit()

    def get_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def list_users(
        self,
        page: int | None = None,
        limit: int | None = None,
        email: str | None = None,
    ):
        if (page is None) ^ (limit is None):
            raise BadRequestError("Both page and limit must be provided together")

        if page is not None:
            if page <= 0:
                raise BadRequestError("page must be greater than 0")
            if limit is not None and limit <= 0:
                raise BadRequestError("limit must be greater than 0")
            if limit is not None and limit > 100:
                raise BadRequestError("limit cannot exceed 100")

        users, total = self.repo.get_all(page=page, limit=limit, email=email)

        if page is not None:
            total_pages = math.ceil(total / limit) if limit else 1

            return {
                "data": users,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": total_pages,
                },
            }

        return {
            "data": users,
            "meta": {
                "total": total,
            },
        }
