from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.database import DatabaseManager
from app.config.settings import settings
from app.services.database.repositories.product import BrandRepository
from app.services.database.schemas.product import BrandDTO, BrandResponse
from app.services.database.models import User
from app.services.security.oauth2 import get_current_user
from app.services.security.dependencies import admin_only

router = APIRouter(
    prefix="/brands",
    tags=["Brands"]
)
db = DatabaseManager()
db.initialize(settings)


@router.post("/create", response_model=BrandDTO, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
async def create_new_brand(brand: BrandDTO, session: AsyncSession = Depends(db.get_db_session)):

    brand_crud = BrandRepository(session)

    brand_exists = await brand_crud.get_brand_by_name(name=brand.name)
    if brand_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This brand name is already registered.")
    new_brand = await brand_crud.create_brand(brand)
    return new_brand


@router.put("/update", response_model=BrandDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def brand_update(brand: BrandDTO, session: AsyncSession = Depends(db.get_db_session)):

    brand_crud = BrandRepository(session)

    brand_db = await brand_crud.get_brand_by_id(id=brand.id)

    if not brand_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand with id: {brand.id} does not exist")

    updated_brand = await brand_crud.update_brand(brand)

    return updated_brand


@router.delete("/delete", response_model=BrandDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def brand_delete(brand: BrandDTO, session: AsyncSession = Depends(db.get_db_session)):

    brand_crud = BrandRepository(session)

    brand_db = await brand_crud.get_brand_by_id(id=brand.id)

    if not brand_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand with id: {brand.id} does not exist")

    deleted_brand = await brand_crud.delete_brand(id=brand.id)

    return Response(status_code=status.HTTP_200_OK, content=f"Brand with id: {deleted_brand.id} has been deleted")


@router.get("/{name}", response_model=BrandResponse, status_code=status.HTTP_200_OK)
async def brand_get_by_id(name: str, offset: int = 0, limit: int = 20, session: AsyncSession = Depends(db.get_db_session)):

    name = name.title().replace("-", " ")

    brand_crud = BrandRepository(session)

    brand_db = await brand_crud.get_brand_with_products(brand_name=name, offset=offset, limit=limit)

    if not brand_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand: {name} does not exist")

    return brand_db


@router.get("/", response_model=Sequence[BrandDTO], status_code=status.HTTP_200_OK)
async def brand_get_all(session: AsyncSession = Depends(db.get_db_session)):

    brand_crud = BrandRepository(session)

    brands = await brand_crud.get_all_brands()

    if not brands:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No brand found")

    return brands
