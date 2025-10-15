from datetime import datetime
from typing import Optional
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)  # uuid str
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    is_active: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[Optional[datetime]]
