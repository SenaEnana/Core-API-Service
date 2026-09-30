from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: bool | None = False


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True