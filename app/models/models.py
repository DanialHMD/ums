from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    users: List["User"] = Relationship(back_populates="role")

class Enrollment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    grade: Optional[float] = None

    student: Optional["Student"] = Relationship(back_populates="enrollments")
    course: Optional["Course"] = Relationship(back_populates="enrollments")


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    department: str
    entry_year: int

    enrollments: List[Enrollment] = Relationship(back_populates="student")


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(index=True, unique=True)
    name: str
    credits: int
    department: str

    enrollments: List[Enrollment] = Relationship(back_populates="course")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    hashed_salt: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    
    role: Optional["Role"] = Relationship(back_populates="users")
