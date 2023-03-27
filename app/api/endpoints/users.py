from fastapi import APIRouter, Depends, HTTPException
from app.services.database.repositories.user.user_repository import UserRepository

from app.services.database.schemas.user import User
from app.services.database.session import get_async_session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{email}", response_model=User)
async def get_user(email: str, user_crud: UserRepository = Depends(get_async_session)):
    user = await user_crud.get_by_email(email)
    return user
