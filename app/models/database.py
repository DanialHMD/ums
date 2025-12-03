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
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
