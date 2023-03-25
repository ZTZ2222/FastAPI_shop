from dataclasses import dataclass
from typing import Any

from fastapi import Body
from pydantic import BaseModel


@dataclass
class CommentBodySpec:
    item: Any = Body(
        ...,
        example={
            "product_id": 1,
            "text": "Bad sensor, my broke after 1 month",
            "rating": 0,
        },
    )


class CommentDTO(BaseModel):
    product_id: int
    text: str
    rating: int

    class Config:
        orm_mode = True
        schema_extra = {
            "product_id": 1,
            "text": "Good CPU and performance",
            "rating": 5,
        }
