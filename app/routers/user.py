from ..models.user_model import UserCreate, UserUpdate, UserOut
from ..core.user_management import UserManager
from ..core.engine import get_db

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    user = user_manager.create_user(
        email=user_in.email,
        password=user_in.password,
        first_name=user_in.first_name,
        last_name=user_in.last_name
    )
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    user = user_manager.get_user(user_id=user_id)
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    user = user_manager.get_user(user_id=user_id)
    updated_user = user_manager.update_user(user_id=user_id, user_data=user_in.dict(exclude_unset=True))
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    user_manager.delete_user(user_id=user_id)
