from fastapi import APIRouter

from app.api.endpoints import users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users.router)
