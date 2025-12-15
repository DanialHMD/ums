from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from core.auth_utils import required_role

from models.database import get_db
from models.models import User, Role

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/")
def list_roles(session: Session = Depends(get_db), current_user: User = Depends(required_role("admin", "staff", "system"))):
    roles = session.exec(select(Role)).all()
    return roles

@router.post("/")
def create_role(role: Role, session: Session = Depends(get_db), current_user: User = Depends(required_role("admin", "system"))):
    session.add(role)
    session.commit()
    session.refresh(role)
    return role 

@router.patch("/{id}")
def update_role(id: int, role_data: Role, session: Session = Depends(get_db), current_user: User = Depends(required_role("admin", "system"))):
    role = session.get(Role, id)
    if not role:
        return {"error": "Role not found"}
    
    for key, value in role_data.model_dump(exclude_unset=True).items():
        setattr(role, key, value)
    
    session.add(role)
    session.commit()
    session.refresh(role)
    return role
