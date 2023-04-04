from fastapi import APIRouter

from app.api.endpoints import users
from app.api.endpoints import products
from app.api.endpoints import brand
from app.api.endpoints import category
from app.api.endpoints import auth

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(brand.router)
api_router.include_router(category.router)
api_router.include_router(auth.router)
