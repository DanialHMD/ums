from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from models.database import get_db 
from models.models import Course, Enrollment, Student

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/")
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    course = db.get(Course, course_id)
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.get("/")
def list_enrollments(db: Session = Depends(get_db)):
    enrollments = db.exec(select(Enrollment)).all()
    return enrollments

@router.get("/{id}")
def get_enrollment_by_id(id: int, db: Session = Depends(get_db)):
    enrollment = db.get(Enrollment, id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.patch("/{id}")
def update_enrollment(id: int, enrollment_data: Enrollment, db: Session = Depends(get_db)):
    enrollment = db.get(Enrollment, id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    for key, value in enrollment_data.model_dump(exclude_unset=True).items():
        setattr(enrollment, key, value)
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.delete("/{id}")
def delete_enrollment(id: int, db: Session = Depends(get_db)):
    enrollment = db.get(Enrollment, id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    return {"message": "Enrollment deleted successfully"}

@router.post("/batch")
def batch_enroll(student_ids: list[int], course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollments = []
    for student_id in student_ids:
        student = db.get(Student, student_id)
        if student:
            enrollment = Enrollment(student_id=student_id, course_id=course_id)
            db.add(enrollment)
            enrollments.append(enrollment)
    
    db.commit()
    for enrollment in enrollments:
        db.refresh(enrollment)
    return enrollments