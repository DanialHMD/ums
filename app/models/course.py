from pydantic import BaseModel
from datetime import datetime

class CreateCourse(BaseModel):
    code: str
    title: str
    description: str
    credits: int
    department_id: str

class UpdateCourse(BaseModel):
    code: str
    title: str
    description: str
    credits: int
    department_id: str

class DeleteCourse(BaseModel):
    title: str

class GetCourse(BaseModel):
    id: int
    code: str
    title: str
    description: str
    credits: int
    department_id: str
