from fastapi import APIRouter, Depends
from sqlmodel import Session
from core.auth_utils import required_role

from models.database import get_db
from models.models import Role

router = APIRouter(prefix="/etc", tags=["etc"])

