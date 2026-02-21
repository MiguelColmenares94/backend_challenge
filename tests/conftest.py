import pytest
from app import create_app
from app.shared.db import db, Base


@pytest.fixture(scope="session")
def app():
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URL": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        Base.metadata.create_all(db.engine)
        yield app
        Base.metadata.drop_all(db.engine)


@pytest.fixture(scope="function")
def session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    Session = db.SessionLocal
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
