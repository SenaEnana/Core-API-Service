from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, OrderModel
from app.schemas import OrderCreate, OrderResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

class OrderCreate(BaseModel):
    name: str
    order_number: int
    description: str

@router.post("/", 
             response_model=OrderResponse, 
             status_code=status.HTTP_201_CREATED
             )
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),  # <-- PROTECTED!
):
    db_order = OrderModel(
        name=order.name,
        order_number=order.order_number,
        description=order.description,
        user_id=current_user.id,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order 
    # return {
    #     "message": "Order created successfully",
    #     "user_id": current_user.id,
    #     "order": order,
    # }

# @router.get("/my-orders")
# def get_my_orders(
#     current_user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """Get all orders belonging to the logged-in user."""
#     return db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()
#     return {"user": current_user.username, "orders": []}