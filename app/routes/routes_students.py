from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from core.auth_utils import required_role
from models.database import engine
from models.models import Student, User

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/")
def create_student(student: Student, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/")
def list_students(db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    students = db.exec(select(Student)).all()
    return students

@router.get("/{student_id}")
def get_student_by_id(student_id: int, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}")
def update_student(student_id: int, student_data: Student, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "system"))):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.get("/{student_id}/courses")
def get_student_courses(student_id: int, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.courses

@router.post("/{student_id}/gpa")
def calculate_student_gpa(student_id: int, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    # Placeholder logic for GPA calculation
    return {"gpa": None}

@router.post("/{student_id}/bulk_import")
def bulk_import_students(students: list[Student], db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "system"))):
    for student in students:
        db.add(student)
    db.commit()
    return {"message": f"Imported {len(students)} students successfully"}

@router.get("/export")
def export_students(db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    students = db.exec(select(Student)).all()
    # Placeholder logic for exporting students
    return {"students": students}