from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.models import User
from models.database import get_db
from core.auth_utils import hash_password, verify_password, create_access_token
from core.redis_client import get_redis_client

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def user_register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = hash_password(form_data.password)
    new_user = User(username=form_data.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    redis_client = get_redis_client()
    if redis_client:
        redis_client.setex(f"token:{access_token}", 3600, "active")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(current_user: User = Depends(get_db)):
    access_token = create_access_token(data={"sub": current_user.username})
    redis_client = get_redis_client()
    if redis_client:
        redis_client.setex(f"token:{access_token}", 3600, "active")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def user_logout(current_user: User = Depends(get_db), token: str = Depends(OAuth2PasswordRequestForm)):
    #check for valid user and token and then invalidate the token
    redis_client = get_redis_client()
    if redis_client:
        redis_client.delete(f"token:{token}")
    return {}

