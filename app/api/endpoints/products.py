from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.database import DatabaseManager
from app.config.settings import settings
from app.services.database.repositories.product.product_repository import ProductRepository
from app.services.database.schemas.product.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
db = DatabaseManager()
db.initialize(settings)


@router.post("/create", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(db.get_db_session)):

    product_crud = ProductRepository(session)
    try:
        result = await product_crud.create_product(product)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.put("/update", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(product: ProductUpdate, session: AsyncSession = Depends(db.get_db_session)):

    product_crud = ProductRepository(session)
    try:
        result = await product_crud.update_product(product)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.get("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(id: int, session: AsyncSession = Depends(db.get_db_session)):

    product_crud = ProductRepository(session)
    result = await product_crud.get_product_by_id(id=id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with key id: {id} does not exists"
        )
    return result


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_product(product: ProductUpdate, session: AsyncSession = Depends(db.get_db_session)):

    product_crud = ProductRepository(session)
    deleted_product = await product_crud.delete_product(product.id)
    if not deleted_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Product has been not found")
    return {"detail": f"Product with id: {deleted_product.id} has been successfully deleted"}
