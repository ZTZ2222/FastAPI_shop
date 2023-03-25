from dataclasses import dataclass
from typing import Any

from fastapi import Body
from pydantic import BaseModel, EmailStr
from sqlalchemy import true


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
    full_name: str
    email: EmailStr
    address: str
    city: str
    country: str
    telephone: str

    class Config:
        orm_mode = True
        schema_extra = {
            "full_name": "Tilek Zamirov",
            "email": "tilzam@example.com",
            "address": "1790 Broadway, NY 10019",
            "city": "New York",
            "country": "USA",
            "telephone": "+1 (360) 921-2552"
        }
