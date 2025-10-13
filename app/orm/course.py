from .base import Base
from .offering import CourseOffering
from sqlalchemy.orm import relationship, Mapped
from dataclasses import Field
from typing import Optional, List


class Course(Base):

    id: Mapped[str] = Field(default=None, primary_key=True)  # uuid str
    code: Mapped[str] = Field(max_length=10, unique=True, index=True)
    title: Mapped[str] = Field(max_length=255)
    description: Mapped[Optional[str]] = None
    credits: Mapped[int] = Field(default=0)
    department_id: Mapped[Optional[str]] = Field(foreign_key="departments.id")
    
    offerings: Mapped[List[CourseOffering]] = relationship(back_populates="course")
