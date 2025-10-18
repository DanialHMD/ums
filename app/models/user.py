from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime