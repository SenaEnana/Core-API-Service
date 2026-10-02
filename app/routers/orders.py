from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, OrderModel
from app.routers.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

class OrderCreate(BaseModel):
    item_name: str
    quantity: int
    total_price: float

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new order assigned to the authenticated user."""
    new_order = OrderModel(**order_data.model_dump(), user_id=current_user.id)
    db.add(new_order)
    db.commit()
    return {
        "message": "Order created successfully",
        "user_id": current_user.id,
        "order": order_data,
    }
