from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.models.database import engine
from app.models.models import Course

router = APIRouter(prefix="/courses", tags=["courses"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/")
def create_course(course: Course, session: Session = Depends(get_session)):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@router.get("/")
def list_courses(session: Session = Depends(get_session)):
    courses = session.exec(select(Course)).all()
    return courses
