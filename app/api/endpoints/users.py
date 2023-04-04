from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.database import DatabaseManager
from app.config.settings import settings
from app.services.database.repositories.user.user_repository import UserRepository
from app.services.database.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.database.models import User
from app.services.database.schemas.user import GrantSuperUser
from app.services.security.oauth2 import get_current_user
from app.services.security.dependencies import admin_only


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
db = DatabaseManager()
db.initialize(settings)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_credentials: UserCreate, session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    user_exists = await user_crud.get_user_by_email(email=user_credentials.email)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email address is already registered.")
    new_user = await user_crud.create_user(user_credentials)
    return new_user


@router.put("/update", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_update(user_credentials: UserUpdate, session: AsyncSession = Depends(db.get_db_session), cur_user: User = Depends(get_current_user)):

    user_crud = UserRepository(session)

    user = await user_crud.get_user_by_email(email=user_credentials.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {user_credentials.email} does not exist")

    if not user.id == cur_user.id and not cur_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    updated_user = await user_crud.update_user(user_credentials)

    return updated_user


@router.delete("/delete", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_delete(user_credentials: UserUpdate, session: AsyncSession = Depends(db.get_db_session), cur_user: User = Depends(get_current_user)):

    user_crud = UserRepository(session)

    user = await user_crud.get_user_by_id(id=user_credentials.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_credentials.id} does not exist")

    if not user.id == cur_user.id and not cur_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    deleted_user = await user_crud.delete_user(user_credentials)

    return Response(status_code=status.HTTP_200_OK, content=f"User with id: {deleted_user.id} has been deleted")


@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_get_by_id(id: int, session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    user = await user_crud.get_user_by_id(id=id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.get("/", response_model=Sequence[UserResponse], status_code=status.HTTP_200_OK)
async def users_get_all(session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    users = await user_crud.get_all_users()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users found")

    return users


@router.patch("/superuser", status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def grand_admin_privileges(user_credentials: GrantSuperUser, session: AsyncSession = Depends(db.get_db_session)):

    user_crud = UserRepository(session)

    user = await user_crud.get_user_by_email(email=user_credentials.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_credentials.id} does not exist")

    superuser = await user_crud.grant_admin_privileges(user=user_credentials)
    if not superuser.is_superuser:
        return {"detail": f"User {superuser.email} no longer has administrator privileges."}

    return {"detail": f"User {superuser.email} has been updated to have administrator privileges."}
