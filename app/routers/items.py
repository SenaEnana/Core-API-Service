from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ItemModel
from app.schemas import ItemCreate, ItemResponse

router = APIRouter(
    prefix="/items",
    tags=["Item"],
)


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(
        name=item.name, price=item.price, is_offer=item.is_offer
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get(
    "/search/",
    response_model=list[ItemResponse],
)
def search_items_by_name(q: str, db: Session = Depends(get_db)):
    results = (
        db.query(ItemModel)
        .filter(ItemModel.name.ilike(f"%{q}%"))
        .all()
    )
    return results


@router.get(
    "",
    response_model=list[ItemResponse],
)
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ItemModel).offset(skip).limit(limit).all()


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = (
        db.query(ItemModel).filter(ItemModel.id == item_id).first()
    )
    if db_item is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Item {item_id} could not be found"
        )
    return db_item


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
)
def update_item(
    item_id: int, item_update: ItemCreate, db: Session = Depends(get_db)
):
    db_item = (
        db.query(ItemModel).filter(ItemModel.id == item_id).first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item_update.name
    db_item.price = item_update.price
    db_item.is_offer = item_update.is_offer

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = (
        db.query(ItemModel).filter(ItemModel.id == item_id).first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully", "id": item_id}