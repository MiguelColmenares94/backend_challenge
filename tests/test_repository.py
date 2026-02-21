from app.modules.user.repository.user_repository import UserRepository
from app.modules.user.models.user_model import User


def test_add_user(session):
    repo = UserRepository(session)

    user = User(name="John", lastname="Doe", email="john@test.com")

    repo.add(user)
    session.commit()

    result = repo.get_by_email("john@test.com")

    assert result is not None
    assert result.email == "john@test.com"


def test_email_substring_filter(session):
    repo = UserRepository(session)

    users = [
        User(name="A", lastname="B", email="aaa@test.com"),
        User(name="C", lastname="D", email="bbb@test.com"),
        User(name="E", lastname="F", email="ccc@other.com"),
    ]

    for u in users:
        repo.add(u)

    session.commit()

    result, total = repo.get_all(email="test")

    assert total == 2
    assert all("test" in u.email for u in result)
