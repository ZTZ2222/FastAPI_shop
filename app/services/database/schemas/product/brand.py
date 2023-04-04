from typing import Any, Optional
from pydantic import BaseModel


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


class BrandResponse(BrandDTO):
    products: list[Any]
