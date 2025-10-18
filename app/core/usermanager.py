from typing import Any, Dict

from .engine import Engine
from fastapi import HTTPException
from .security import Security
from app.orm.user import User


class UserManager:
    def __init__(self) -> None:
        self.security = Security()


    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> User:
        
        hashed_pw = self.security.get_password_hash(password)

        new_user = User(
            email=email,
            hashed_password=hashed_pw,
            first_name=first_name,
            last_name=last_name
        )

        with Engine().get_db() as self.db:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

        return HTTPException(status_code=201, detail=f"User {new_user.email} created")


    def get_user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return HTTPException(status_code=200, detail=f"User {user.email} retrieved")


    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> None:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            for key, value in user_data.items():
                setattr(user, key, value)

            self.db.commit()
            self.db.refresh(user)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))


    def delete_user(self, user_id: int) -> None:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
