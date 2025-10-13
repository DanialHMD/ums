from .base import Base
from .course import Course
from .enrollment import Enrollment
from sqlalchemy.orm import relationship, Mapped
from dataclasses import Field
from typing import List, Optional

class CourseOffering(Base):

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    semester: str
    section: Optional[str]
    professor_id: Optional[str] = Field(foreign_key="user.id")
    capacity: int = 0
    enrolled_count: int = 0

    course: Optional[Course] = relationship(back_populates="offerings")
    enrollments: List[Enrollment] = relationship(back_populates="offering")