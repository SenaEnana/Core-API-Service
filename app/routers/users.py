from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, UserRole
from app.schemas import UserResponse
from app.routers.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),  # 🔒 Admin only
):
    """Retrieve all users in the system."""
    return db.query(UserModel).all()


