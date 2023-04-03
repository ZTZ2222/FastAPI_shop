from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel

from . import CategoryDTO, BrandDTO, RatingDTO


class SizeDTO(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True


class ColorDTO(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    base_price: Optional[float]
    sale_price: Optional[float]
    description: Optional[str]
    in_stock: Optional[bool]
    category_id: Optional[int]
    brand_id: Optional[int]
    color_id: Optional[int]
    size_id: Optional[int]
    quantity: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    name: str = "Unnamed product"
    base_price: float
    category_id: int
    quantity: int

    class Config:
        schema_extra = {
            "name": "Product name",
            "base_price": 12345,
            "description": "A text description",
            "category_id": 1,
            "brand_id": 1,
            "in_stock": True,
            "size_id": 3,
            "color_id": 4,
            "quantity": 5
        }
        keep_untouched = ()


class ProductUpdate(ProductBase):
    id: int

    class Config:
        schema_extra = {
            "id": 15,
            "quantity": 10
        }


class ProductResponse(ProductBase):
    category: CategoryDTO
    brand: Optional[BrandDTO]
    color: Optional[ColorDTO]
    size: Optional[SizeDTO]
    ratings: Optional[Sequence[RatingDTO]]

    class Config:
        schema_extra = {
            "id": 15
        }
