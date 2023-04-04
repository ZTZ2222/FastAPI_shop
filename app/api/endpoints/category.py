from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.database import DatabaseManager
from app.config.settings import settings
from app.services.database.repositories.product import CategoryRepository
from app.services.database.schemas.product import CategoryDTO, CategoryResponse
from app.services.security.dependencies import admin_only


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)
db = DatabaseManager()
db.initialize(settings)


@router.post("/create", response_model=CategoryDTO, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
async def create_new_category(category: CategoryDTO, session: AsyncSession = Depends(db.get_db_session)):

    category_crud = CategoryRepository(session)

    category_exists = await category_crud.get_category_by_name(name=category.name)
    if category_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This category name is already registered.")
    new_category = await category_crud.create_category(category)
    return new_category


@router.put("/update", response_model=CategoryDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def category_update(category: CategoryDTO, session: AsyncSession = Depends(db.get_db_session)):

    category_crud = CategoryRepository(session)

    category_db = await category_crud.get_category_by_id(id=category.id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {category.id} does not exist")

    updated_category = await category_crud.update_category(category)

    return updated_category


@router.delete("/delete", response_model=CategoryDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def category_delete(category: CategoryDTO, session: AsyncSession = Depends(db.get_db_session)):

    category_crud = CategoryRepository(session)

    category_db = await category_crud.get_category_by_id(id=category.id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {category.id} does not exist")

    deleted_category = await category_crud.delete_category(id=category.id)

    return Response(status_code=status.HTTP_200_OK, content=f"Category with id: {deleted_category.id} has been deleted")


@router.get("/{name}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def category_get_by_name(name: str, offset: int = 0, limit: int = 20, session: AsyncSession = Depends(db.get_db_session)):

    name = name.title().replace("-", " ")

    category_crud = CategoryRepository(session)

    category_db = await category_crud.get_category_with_products(category_name=name, offset=offset, limit=limit)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category: '{name}' does not exist")

    return category_db


@router.get("/", response_model=Sequence[CategoryResponse], status_code=status.HTTP_200_OK)
async def category_get_all(session: AsyncSession = Depends(db.get_db_session)):

    category_crud = CategoryRepository(session)

    categories = await category_crud.get_all_categories()

    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No category found")

    return categories
