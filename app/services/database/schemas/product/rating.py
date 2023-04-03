from dataclasses import dataclass
from typing import Any, Optional

from fastapi import Body
from pydantic import BaseModel


@dataclass
class RatingBodySpec:
    item: Any = Body(
        ...,
        example={
            "product_id": 1,
            "comment": "This product exceeded my expectations. Highly recommend it!",
            "stars": 5,
        },
    )


class RatingDTO(BaseModel):
    product_id: int
    stars: float
    comment: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "product_id": 1,
            "comment": "This product exceeded my expectations. Highly recommend it!",
            "stars": 5,
        }
