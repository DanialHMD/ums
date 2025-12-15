from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from core.auth_utils import required_role

from models.database import get_db as get_session
from models.models import Course, User

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/")
def create_course(course: Course, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system"))):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@router.get("/")
def list_courses(session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system", "student"))):
    courses = session.exec(select(Course)).all()
    return courses

@router.get("/{course_id}")
def get_course_by_id(course_id: int, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system", "student"))):
    course = session.get(Course, course_id)
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}")
def update_course(course_id: int, course_data: Course, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system"))):
    course = session.get(Course, course_id)
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_course(course_id: int, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "system"))):
    course = session.get(Course, course_id)
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    
    session.delete(course)
    session.commit()
    return {"message": "Course deleted successfully"}