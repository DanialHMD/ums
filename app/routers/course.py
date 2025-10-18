from ..models.course import (CreateCourse, UpdateCourse, DeleteCourse, GetCourse)
from ..models.offering import (CreateCourseOffering, UpdateCourseOffering, DeleteCourseOffering, GetCourseOffering)
from ..core.coursemanager import CourseManager

from fastapi import APIRouter, status

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CreateCourse)
def create_course(course: CreateCourse):
    course_manager = CourseManager()
    return course_manager.create_course(**course.model_dump())

@router.get("/", response_model=list[GetCourse])
def get_courses():
    course_manager = CourseManager()
    return course_manager.get_courses()
