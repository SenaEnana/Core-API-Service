from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, OrderModel
from app.schemas import OrderCreate, OrderResponse
from app.routers.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

class OrderCreate(BaseModel):
    name: str
    order_number: int
    description: str

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
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

@router.get("/my-orders")
def get_my_orders(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all orders belonging to the logged-in user."""
    return db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()
    return {"user": current_user.username, "orders": []}