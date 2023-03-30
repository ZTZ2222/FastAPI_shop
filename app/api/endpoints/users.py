from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.database import DatabaseManager
from app.config.settings import settings
from app.services.database.repositories.user.user_repository import UserRepository
from app.services.database.schemas.user import UserCreate, UserResponse, UserUpdate, UserInDBBase

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
db = DatabaseManager()
db.initialize(settings)

# @router.get("/{email}", response_model=User)
# async def get_user(email: str, user_crud: UserRepository = Depends(get_user_repository)):
#     user = await user_crud.get_by_email(email)
#     return user


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def user_signup(user_credentials: UserCreate, session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    user_exists = await user_crud.get_user_by_email(email=user_credentials.email)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email address is already registered by a user.")
    new_user = await user_crud.user_create(user_credentials)
    return new_user


@router.put("/update", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_update(user_credentials: UserUpdate, session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    user = await user_crud.get_user_by_email(email=user_credentials.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {user_credentials.email} does not exist")

    updated_user = await user_crud.user_update(user_credentials)

    return updated_user


@router.delete("/delete", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_delete(user_credentials: UserUpdate, session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    user = await user_crud.get_user_by_email(email=user_credentials.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {user_credentials.email} does not exist")

    deleted_user = await user_crud.user_delete(user_credentials)

    return Response(status_code=status.HTTP_200_OK, content=f"User with email: {deleted_user.email} has been deleted")


# Change Depends of current_user parameter ! ! !


# @router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
# async def user_view(current_user: User = Depends("oauth2.get_current_user"), session: AsyncSession = Depends(db.get_db_session)):

#     user_crud = UserRepository(session)

#     user = await user_crud.get_user_by_email(email=current_user.email)

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with username: {current_user.username} does not exist")

#     return user


# @router.post("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
# async def user_update(new_password: str, session: AsyncSession = Depends(db.get_db_session), current_user: User = Depends("oauth2.get_current_user")):

#     user_crud = UserRepository(session)

#     token_payload = await jwt_service.decode_user_identity_token(token)
#     user = await user_crud.get_user_by_email(token_payload["email"])
#     if user and user.id == token_payload['id']:
#         await user_crud.password_change(user.email, new_password)

#     return
