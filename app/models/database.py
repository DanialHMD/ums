import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from models.models import (
    Course, 
    Enrollment, 
    Student, 
    User, 
    Role, 
    RolePermission, 
    Permission, 
    Department, 
    Semester)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    try:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database tables: {e}")

def get_db():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e