from fastapi import APIRouter

from app.api.endpoints import users
from app.api.endpoints import products

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users.router)
api_router.include_router(products.router)
