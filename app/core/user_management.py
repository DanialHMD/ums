from fastapi import HTTPException
from typing import Any, Dict

from .engine import Engine 
# from .security import Security
from ..orm.user import User

class UserManager:
    def __init__(self) -> None:
        pass
        # security = Security()

    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> User:
        hashed_pw = password
        print(hashed_pw)
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
        return new_user

    def get_user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

    def delete_user(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
