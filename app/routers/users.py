from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, UserRole
from app.schemas import UserResponse
from app.routers.auth import get_current_user, require_admin, db_user

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


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve details for a specific user."""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),  # 🔒 Admin only
):
    """Promote or demote a user's role."""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user

@router.put(
    "{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user_update: db_user,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),  # <-- PROTECTED!
    admin_user: UserModel = Depends(require_admin),  # 🔒 Admin-only!
):
    db_user = (
        db.query(UserModel).filter(UserModel.id == user_id).first()
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.email = user_update.email
    db_user.username = user_update.username
    db_user.hashed_password = user_update.password
    db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user
