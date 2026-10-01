from pydantic import BaseModel, EmailStr
from app.models import UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER  #Optional


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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
