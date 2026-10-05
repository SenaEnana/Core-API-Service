from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel, OrderModel
from app.schemas import OrderCreate, OrderResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

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
        quantity=order.quantity,
        description=order.description,
        user_id=current_user.id,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order 

@router.get("/my-orders", response_model=list[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get all orders belonging to the logged-in user."""
    orders = db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()
    return orders
