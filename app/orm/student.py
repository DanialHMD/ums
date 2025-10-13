from dataclasses import Field
from sqlalchemy.orm import relationship, Mapped
from typing import Optional, List
from .user import User
from .base import Base
from .enrollment import Enrollment

class Student(Base, table=True):
    
    id: Mapped[str] = Field(default=None, primary_key=True)  # same UUID as user
    student_number: Mapped[str] = Field(unique=True, index=True)
    enrollment_year: Mapped[Optional[int]] = None
    program: Mapped[Optional[str]] = None
    user: Mapped[Optional[User]] = relationship()

    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="student")