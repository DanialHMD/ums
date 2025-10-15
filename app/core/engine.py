from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy import create_engine
from typing import Generator

class Engine:
    def __init__(self) -> None:
        database_url = "postgresql:///./test.db"
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
