from dataclasses import Field
from .base import Base 
from .enrollment import Enrollment
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import Optional

class Grade(Base):

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(foreign_key="enrollments.id")
    grade: Mapped[float] = mapped_column(default=0.0)

    enrollment: Mapped[Optional[Enrollment]] = relationship(back_populates="grades")
