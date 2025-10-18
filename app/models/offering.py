from typing import Optional

from pydantic import BaseModel


class CreateCourseOffering(BaseModel):
    course_id: int
    semester: str
    section: Optional[str]
    professor_id: Optional[str]
    capacity: int
    enrolled_count: int

class UpdateCourseOffering(BaseModel):
    course_id: int
    semester: str
    section: Optional[str]
    professor_id: Optional[str]
    capacity: int
    enrolled_count: int

class DeleteCourseOffering(BaseModel):
    course_id: int
    semester: str
    section: Optional[str]
    professor_id: Optional[str]

class GetCourseOffering(BaseModel):
    course_id: int
    semester: str
    section: Optional[str]
    professor_id: Optional[str]
    capacity: int
    enrolled_count: int
    