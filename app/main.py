from orm.base import Base
from core.engine import Engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=Engine().get_db())