from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, UserRole
from app.schemas import UserCreate, UserResponse 
from app.security import get_password_hash 
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


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update user profile.
    - Regular users can only update their own profile.
    - Admin users can update any user's profile.
    """
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user profile",
        )
    
    target_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Check for email/username uniqueness if changing to values used by someone else
    existing_email = db.query(UserModel).filter(
        UserModel.email == user_update.email, UserModel.id != user_id
    ).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already taken")

    existing_username = db.query(UserModel).filter(
        UserModel.username == user_update.username, UserModel.id != user_id
    ).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # 4. Update fields securely
    target_user.email = user_update.email
    target_user.username = user_update.username
    target_user.hashed_password = get_password_hash(user_update.password)  # Hash password!

    # 5. Only Admins can update the role field
    if current_user.role == UserRole.ADMIN and hasattr(user_update, "role"):
        target_user.role = user_update.role

    db.commit()
    db.refresh(target_user)
    return target_user