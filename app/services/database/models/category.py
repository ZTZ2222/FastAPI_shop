from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True)

    products = relationship(
        'Product', back_populates="category", cascade="all, delete-orphan")
