from dataclasses import dataclass
from typing import Any, Optional

from fastapi import Body
from pydantic import BaseModel


@dataclass
class OrderBodySpec:
    item: Any = Body(
        ...,
        example={
            "full_name": "Tilek Zamirov",
            "email": "tilzam@example.com",
            "address": "1790 Broadway, NY 10019",
            "city": "New York",
            "country": "USA",
            "telephone": "+1 (360) 921-2552"
        },
    )


class OrderDTO(BaseModel):
    id: Optional[int]
    user_id: int
    status: str
    total_price: float
    address: str
    city: str
    country: str
    telephone: str

    class Config:
        orm_mode = True
        schema_extra = {
            "user_id": 32,
            "status": "Delivered",
            "total_price": 200,
            "address": "1790 Broadway, NY 10019",
            "city": "New York",
            "country": "USA",
            "telephone": "+1 (360) 921-2552"
        }


class OrderItemDTO(BaseModel):
    id: Optional[int]
    name: str
    order_id: int
    color_id: int
    size_id: int
    price: float
    quantity: int
