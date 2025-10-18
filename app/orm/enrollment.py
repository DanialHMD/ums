from datetime import datetime
from typing import Optional

from .offering import CourseOffering
from .base import Base
from .student import Student
from .course import Course
from sqlalchemy.orm import Mapped, relationship, mapped_column

class Enrollment(Base):

    id: Mapped[str] = mapped_column(default=None, primary_key=True)  # uuid str
    student_id: Mapped[str] = mapped_column(foreign_key="students.id")
    course_id: Mapped[str] = mapped_column(foreign_key="courses.id")
    enrollment_date: Mapped[datetime] = mapped_column(default_factory=datetime.now)

    student: Mapped[Student] = relationship(back_populates="enrollments")
    course: Mapped[Course] = relationship(back_populates="enrollments")
    offering: Mapped[Optional[CourseOffering]] = relationship(back_populates="enrollments")
