from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def init_app(self, db_url: str):
        self.engine = create_engine(
            db_url,
            echo=False,
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_session(self):
        return self.SessionLocal()

    def create_tables(self):
        Base.metadata.create_all(self.engine)


db = Database()
