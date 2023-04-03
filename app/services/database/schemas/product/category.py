from dataclasses import dataclass
from typing import Any, Optional

from fastapi import Body
from pydantic import BaseModel


@dataclass
class CategoryBodySpec:
    item: Any = Body(
        ...,
        example={
            "name": "Clothing and Accessories"
        },
    )


class CategoryDTO(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Clothing and Accessories"
        }
