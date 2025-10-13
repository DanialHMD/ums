from dataclasses import Field
from .base import Base 
from .enrollment import Enrollment
from sqlalchemy.orm import Mapped, relationship
from typing import Optional

class Grade(Base):

    id: Mapped[int] = Field(default=None, primary_key=True)
    enrollment_id: Mapped[int] = Field(foreign_key="enrollments.id")
    grade: Mapped[float] = Field(default=0.0)

    enrollment: Mapped[Optional[Enrollment]] = relationship(back_populates="grades")
