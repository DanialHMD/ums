from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy import create_engine
from typing import Generator



@contextmanager
def get_db() -> Generator[Session, None, None]:
    DATABASE_URL = "postgresql:///./test.db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
