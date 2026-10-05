from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, UserRole
from app.schemas import UserResponse
from app.routers.auth import get_current_user, require_admin

