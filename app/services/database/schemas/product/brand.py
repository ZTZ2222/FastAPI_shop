from dataclasses import dataclass
from typing import Any, Optional

from fastapi import Body
from pydantic import BaseModel


@dataclass
class BrandBodySpec:
    item: Any = Body(
        ...,
        example={
            "name": "Apple",
            "description": "Technology and electronics company.",
        },
    )


class BrandDTO(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Apple",
            "description": "Technology and electronics company.",
        }
