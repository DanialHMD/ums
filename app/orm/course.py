from .base import Base
from .offering import CourseOffering
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List


class Course(Base):

    id: Mapped[str] = mapped_column(default=None, primary_key=True)  # uuid str
    code: Mapped[str] = mapped_column(max_length=10, unique=True, index=True)
    title: Mapped[str] = mapped_column(max_length=255)
    description: Mapped[Optional[str]] = mapped_column()
    credits: Mapped[int] = mapped_column(default=0)
    department_id: Mapped[Optional[str]] = mapped_column(foreign_key="departments.id")

    offerings: Mapped[List[CourseOffering]] = relationship(back_populates="course")
