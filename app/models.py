import enum
from sqlalchemy import Boolean, Column, Float, Integer, String
from app.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)
