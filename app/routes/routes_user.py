from fastapi import APIRouter, Depends
from sqlmodel import Session
from core.auth_utils import required_role

from models.database import engine
from models.models import User, Role

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def read_current_user(current_user: User = Depends(required_role("admin", "staff", "system", "student"))):
    return current_user

@router.patch("/me/password")
def change_password(new_password: str, current_user: User = Depends(required_role("admin", "staff", "system", "student")), db: Session = Depends(lambda: Session(engine))):
    from core.auth_utils import hash_password
    current_user.hashed_password = hash_password(new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"msg": "Password updated successfully"}

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "staff", "system"))):
    user = db.get(User, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}")
def update_user():
    pass  # Implementation for updating user details by admin/staff/system

@router.delete("/{user_id}")
def delete_user():
    pass  # Implementation for deleting a user by admin/staff/system


@router.delete("/{user_id}/roles")
def delete_role(user_id: int, session: Session = Depends(lambda: Session(engine)), current_user: User = Depends(required_role("admin", "system"))):
    role = session.get(Role, user_id)
    if not role:
        return {"error": "Role not found"}
    
    session.delete(role)
    session.commit()
    return {"message": "Role deleted successfully"}