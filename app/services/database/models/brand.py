from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)

    products = relationship(
        'Product', back_populates="brand", cascade="all, delete-orphan")
