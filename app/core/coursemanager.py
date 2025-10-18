from fastapi import HTTPException

from ..models.course import CreateCourse, DeleteCourse, GetCourse, UpdateCourse
from ..models.offering import (CreateCourseOffering, DeleteCourseOffering,
                               UpdateCourseOffering, GetCourseOffering)
from .engine import Engine
from .security import Security


class CourseManager:
    def __init__(self):
        self.security = Security()
        self.engine = Engine()

    def create_course(self, *kargs: CreateCourse) -> HTTPException:
        course = CreateCourse(
            code=kargs[0],
            title=kargs[1],
            description=kargs[2],
            credits=kargs[3],
            department_id=kargs[4]
        )
        with self.engine.get_db() as db:
            try:
                db.add(course)
                db.commit()
                db.refresh(course)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=500, detail=str(e))

        return HTTPException(status_code=200, detail=f"Course {course.title} created")

    def update_course(self, *kargs: UpdateCourse) -> HTTPException:
        course = UpdateCourse(
            code=kargs[0],
            title=kargs[1],
            description=kargs[2],
            credits=kargs[3],
            department_id=kargs[4]
        )
        with self.engine.get_db() as db:
            try:
                db.merge(course)
                db.commit()
                return HTTPException(status_code=200, detail=f"Course {course.title} updated")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

    def remove_course(self, title: str) -> HTTPException:
        with self.engine.get_db() as db:
            course = db.query(DeleteCourse).filter(DeleteCourse.title == title).first()
            if course:
                db.delete(course)
                db.commit()
                return HTTPException(status_code=204, detail="Course deleted")
            else:
                return HTTPException(status_code=404, detail="Course not found")

    def get_courses(self, *kargs: GetCourse) -> list[GetCourse]:
        with self.engine.get_db() as db:
            return db.query(GetCourse).all()

    def create_course_offering(self, *kargs: CreateCourseOffering) -> HTTPException:
        course_offering = CreateCourseOffering(
            code=kargs[0],
            title=kargs[1],
            description=kargs[2],
            credits=kargs[3],
            department_id=kargs[4]
        )
        with self.engine.get_db() as db:
            try:
                db.add(course_offering)
                db.commit()
                db.refresh(course_offering)
            except Exception as e:
                db.rollback()
                return HTTPException(status_code=500, detail=str(e))

        return HTTPException(status_code=200, detail=f"Course offering for {course_offering.title} created")

    def update_course_offering(self, *kargs: UpdateCourseOffering) -> HTTPException:
        course_offering = UpdateCourseOffering(
            course_id=kargs[0],
            semester=kargs[1],
            section=kargs[2],
            professor_id=kargs[3],
            capacity=kargs[4],
            enrolled_count=kargs[5]
        )
        with self.engine.get_db() as db:
            try:
                db.merge(course_offering)
                db.commit()
                return HTTPException(status_code=200, detail=f"Course offering for {course_offering.title} updated")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

    def delete_course_offering(self, *kargs: DeleteCourseOffering) -> HTTPException:
        course_offering = DeleteCourseOffering(
            course_id=kargs[0],
            semester=kargs[1],
            section=kargs[2],
            professor_id=kargs[3]
        )
        with self.engine.get_db() as db:
            try:
                db.delete(course_offering)
                db.commit()
                return HTTPException(status_code=204, detail="Course offering deleted")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

    def get_course_offering(self, *kargs: GetCourseOffering) -> HTTPException:
        with self.engine.get_db() as db:
            course_offering = db.query(GetCourseOffering).filter(
                GetCourseOffering.course_id == kargs[0],
                GetCourseOffering.semester == kargs[1],
                GetCourseOffering.section == kargs[2],
                GetCourseOffering.professor_id == kargs[3]
            ).first()
            if course_offering:
                return course_offering
            else:
                return HTTPException(status_code=404, detail="Course offering not found")