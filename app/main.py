from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.models import ItemModel

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: bool | None = False

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes: True

@app.get("/")
def read_root():
    return {"message": "Welcome to the Core API Service"}


@app.post(
    f"{settings.API_PREFIX}/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Item"]
)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(
        name=item.name, price=item.price, is_offer=item.is_offer
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get(
        f"{settings.API_PREFIX}/items/search/",
        response_model=ItemResponse,
        tags=["Item"],
)
def search_items_by_name(q: str, db: Session = Depends(get_db)):
    results = (
        db.query(ItemModel)
        .filter(ItemModel.name.contains(q))
        .all()
    )
    return results

@app.get(
    f"{settings.API_PREFIX}/items",
    response_model=list[ItemResponse],
    tags=["Item"]
)
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ItemModel).offset(skip).limit(limit).all()

@app.get(
        f"{settings.API_PREFIX}/items/{{item_id}}",
        response_model=ItemResponse,
        tags=["Item"],
)
def search_item(item_id: int, db: Session = Depends(get_db)):
    db_item=(
        db.query(ItemModel).filter(ItemModel.id == item_id).first()
    )
    if db_item is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Item {item_id} could not be found"
            )
    return db_item


@app.get(
    f"{settings.API_PREFIX}/items/{{item_id}}",
    response_model=ItemResponse,
    tags=["Item"],
)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item= (
        db.query(ItemModel).filter(ItemModel.id == item_id).first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put(
    f"{settings.API_PREFIX}/items/{{item_id}}",
    response_model=ItemResponse,
    tags=["Item"],
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

@app.delete(
        f"{settings.API_PREFIX}/items/{{item_id}}", 
        tags=["Item"]
        )
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = (
        db.query(ItemModel).filter(ItemModel.id == item_id).first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully", "id": item_id}


@app.get("/health", tags=["API Health Check"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }