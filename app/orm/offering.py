from typing import List, Optional

from sqlalchemy.orm import mapped_column, relationship

from .base import Base
from .course import Course
from .enrollment import Enrollment


class CourseOffering(Base):

    id: Optional[int] = mapped_column(default=None, primary_key=True)
    course_id: int = mapped_column(foreign_key="course.id")
    semester: str = mapped_column()
    section: Optional[str] = mapped_column()
    professor_id: Optional[str] = mapped_column(foreign_key="user.id")
    capacity: int = mapped_column(default=0)
    enrolled_count: int = mapped_column(default=0)

    course: Optional[Course] = relationship(back_populates="offerings")
    enrollments: List[Enrollment] = relationship(back_populates="offering")