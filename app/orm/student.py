from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from .user import User
from .base import Base
from .enrollment import Enrollment

class Student(Base, table=True):
    
    id: Mapped[str] = mapped_column(default=None, primary_key=True)  # same UUID as user
    student_number: Mapped[str] = mapped_column(unique=True, index=True)
    enrollment_year: Mapped[Optional[int]] = mapped_column()
    program: Mapped[Optional[str]] = mapped_column()
    user: Mapped[Optional[User]] = relationship()

    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="student")