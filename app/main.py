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

# @app.post(
#     f"{settings.API_PREFIX}/items",
#     response_model=ItemResponse,
#     status_code=status.HTTP_201_CREATED,
#     tags=["Item"],
# )
# def create_item(item: ItemCreate, db: Session = Depends(get_db)):
#     db_item = ItemModel(
#         name=item.name, price=item.price, is_offer=item.is_offer
#     )
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# @app.get("/health", tags=["API Health Check"])
# async def health_check():
#     return {
#         "status": "healthy",
#         "service": settings.PROJECT_NAME,
#         "version": settings.VERSION,
#     }

# @app.get(f"{settings.API_PREFIX}/ping", tags=["API Health Check"])
# async def ping():
#     return {"message": "pong"}


# @app.post(f"{settings.API_PREFIX}/items", tags=["Item"])
# async def add_item(item: Item):
#     return {"message": "Item added successfully", "data": item}

# @app.post(f"{settings.API_PREFIX}/items/{{item_id}}", tags=["Item"])
# async def search_item(item_id: int, item: Item):
#     if item_id == Item:
#         return{item_id: "Item", "message" : "Found Successfully"}
#     return {item_id: "item_id", "message": "Couldn't be found in the", item: "Item"}


# @app.get(f"{settings.API_PREFIX}/items", tags=["Item"])
# def list_items(q: str | None = None):
#     return {"query": q, "items": []}


# @app.get(f"{settings.API_PREFIX}/items/{{item_id}}", tags=["Item"])
# def get_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}


# @app.put(f"{settings.API_PREFIX}/items/{{item_id}}", tags=["Item"])
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


# @app.delete(f"{settings.API_PREFIX}/items/{{item_id}}", tags=["Item"])
# def delete_item(item_id: int):
#     return {"item_id": item_id, "message": "Item deleted successfully"}
