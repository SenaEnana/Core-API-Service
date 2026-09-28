from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from pydantic import BaseModel

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Welcome to the Core API Service"}

@app.get("/health", tags=["API Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }

@app.get(f"{settings.API_PREFIX}/ping", tags=["Health Check"])
async def ping():
    return {"message": "pong"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
