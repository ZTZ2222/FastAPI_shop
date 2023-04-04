from typing import Any, Optional
from pydantic import BaseModel


class CategoryDTO(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Clothing and Accessories"
        }


class CategoryResponse(CategoryDTO):
    products: list[Any]
