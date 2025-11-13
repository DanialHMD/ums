from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from models.database import engine
from models.models import Course, Enrollment, Student

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/")
def create_enrollment(enrollment: Enrollment, session: Session = Depends(get_session)):
    # Check if student and course exist
    student = session.get(Student, enrollment.student_id)
    course = session.get(Course, enrollment.course_id)
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or course not found")

    # Check duplicate enrollment
    existing = session.exec(
        select(Enrollment)
        .where(Enrollment.student_id == enrollment.student_id)
        .where(Enrollment.course_id == enrollment.course_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment

@router.get("/")
def list_enrollments(session: Session = Depends(get_session)):
    enrollments = session.exec(select(Enrollment)).all()
    return enrollments
