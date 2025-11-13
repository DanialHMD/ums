from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth_utils import required_role
from models.database import engine
from models.models import Student, User

router = APIRouter(prefix="/students", tags=["students"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/")
def create_student(student: Student, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system"))):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@router.put("/{student_id}")
def update_student(student_id: int, updated_student: Student, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system"))):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.first_name = updated_student.first_name
    student.last_name = updated_student.last_name
    student.email = updated_student.email
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system"))):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}

@router.get("/")
def list_students(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    return students

@router.get("/{student_id}/courses")
def get_student_courses(student_id: int, session: Session = Depends(get_session), current_user: User = Depends(required_role("admin", "staff", "system"))):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Gather course info from enrollments
    courses = [
        {"course_id": e.course_id, "course_name": e.course.name, "grade": e.grade}
        for e in student.enrollments
    ]
    return {"student": f"{student.first_name} {student.last_name}", "courses": courses}

@router.get("/{student_id}/gpa")
def get_student_gpa(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    enrollments = student.enrollments
    valid = [e for e in enrollments if e.grade is not None]
    if not valid:
        return {"student": student.first_name, "gpa": None, "message": "No grades yet"}

    total_points = 0
    total_credits = 0
    for e in valid:
        total_points += e.course.credits * e.grade
    total_credits += e.course.credits

    gpa = total_points / total_credits
    return {
        "student": f"{student.first_name} {student.last_name}",
        "gpa": round(gpa, 2),
        "courses_counted": len(valid)
    }
