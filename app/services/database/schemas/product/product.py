from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Any

from fastapi import Body
from pydantic import BaseModel


@dataclass
class ProductBodySpec:
    item: Any = Body(
        ...,
        example={
            "name": "Apple MacBook 15",
            "base_price": 7000,
            "description": "Light and fast laptop, Light and fast laptop, Light and fast laptop, Light and fast laptop",
            "category_id": 1,
            "brand_id": 1,
        },
    )


class ProductDTO(BaseModel):
    id: Optional[int] = None
    name: str
    base_price: float
    sale_price: Optional[float] = None
    description: str
    created_at: Optional[datetime] = None
    category_id: int
    brand_id: Optional[int] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Apple MacBook 15",
            "base_price": 7000,
            "description": "Light and fast laptop",
            "category_id": 1,
            "brand_id": 1,
        }
        keep_untouched = ()


class ProductUpdate(BaseModel):
    name: str
    base_price: float
    sale_price: Optional[float] = None
    description: str
    category_id: int
    brand_id: Optional[int] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Apple MacBook 15",
            "base_price": 7000,
            "sale_price": 5000,
            "description": "Light and fast laptop",
            "category_id": 1,
            "brand_id": 1,
        }
