from fastapi import FastAPI

from app.models.database import create_db_and_tables
from routes_courses import router as courses_router
from routes_enrollments import router as enrollments_router
from routes_students import router as students_router
from routes_auth import router as auth_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Hello University"}
