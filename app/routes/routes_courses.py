from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from core.auth_utils import required_role

from models.database import engine
from models.models import Course, User

router = APIRouter(prefix="/courses", tags=["courses"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/")
def create_course(course: Course, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin"))):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@router.get("/")
def list_courses(session: Session = Depends(get_session)):
    courses = session.exec(select(Course)).all()
    return courses
