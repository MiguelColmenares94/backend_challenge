import pytest
from app.modules.user.controllers.user_controller import UserController
from app.shared.exceptions import BadRequestError, NotFoundError


def test_create_user_success(session):
    controller = UserController(session)

    user = controller.create_user(
        {"name": "Jane", "lastname": "Doe", "email": "jane@test.com"}
    )

    assert user.id is not None


def test_invalid_email(session):
    controller = UserController(session)

    with pytest.raises(BadRequestError):
        controller.create_user({"name": "Jane", "lastname": "Doe", "email": "invalid"})


def test_get_user_not_found(session):
    controller = UserController(session)

    with pytest.raises(NotFoundError):
        controller.get_user(999)
