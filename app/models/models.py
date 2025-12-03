from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class RolePermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    users: List["User"] = Relationship(back_populates="role")
    permissions: List["Permission"] = Relationship(back_populates="roles",
                                                   link_model=RolePermission)


class Enrollment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    grade: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    student: Optional["Student"] = Relationship(back_populates="enrollments")
    course: Optional["Course"] = Relationship(back_populates="enrollments")


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    email: str = Field(index=True)
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    department: str
    entry_year: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    enrollments: List[Enrollment] = Relationship(back_populates="student")


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(index=True, unique=True)
    name: str
    credits: int
    department: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    enrollments: List[Enrollment] = Relationship(back_populates="course")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    role: Optional["Role"] = Relationship(back_populates="users")


class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    head_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    head: Optional["User"] = Relationship(back_populates="department")
    students: List["Student"] = Relationship(back_populates="dept")


class Semester(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    start_date: datetime
    end_date: datetime
    is_active: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    enrollments: List["Enrollment"] = Relationship(back_populates="semester")


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None

    roles: List["Role"] = Relationship(back_populates="permissions",
                                       link_model=RolePermission)
