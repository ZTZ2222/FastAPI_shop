from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.database import DatabaseManager
from app.config.settings import settings
from app.services.database.repositories.product import ProductRepository, ColorRepository, SizeRepository, RatingRepository
from app.services.database.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ColorDTO, SizeDTO, RatingDTO
from app.services.database.models import User
from app.services.security.oauth2 import get_current_user
from app.services.security.dependencies import admin_only

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
db = DatabaseManager()
db.initialize(settings)


@router.post("/create", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
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


@router.put("/update", response_model=ProductResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
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


@router.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def delete_product(product: ProductUpdate, session: AsyncSession = Depends(db.get_db_session)):

    product_crud = ProductRepository(session)
    deleted_product = await product_crud.delete_product(product.id)
    if not deleted_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Product has been not found")
    return {"detail": f"Product with id: {deleted_product.id} has been successfully deleted"}


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


@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products(offset: int = 0, limit: int = 20, session: AsyncSession = Depends(db.get_db_session)):

    product_crud = ProductRepository(session)
    result = await product_crud.get_all_products(offset=offset, limit=limit)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with key id: {id} does not exists"
        )
    return result


##########################
# BLOCK FOR COLOR ROUTES #
##########################


@router.post("/colors/create", response_model=ColorDTO, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
async def create_new_color(color: ColorDTO, session: AsyncSession = Depends(db.get_db_session)):

    color_crud = ColorRepository(session)

    color_exists = await color_crud.get_product_color_by_name(name=color.name)
    if color_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This color name is already registered.")
    new_color = await color_crud.create_product_color(color)
    return new_color


@router.put("/colors/update", response_model=ColorDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def color_update(color: ColorDTO, session: AsyncSession = Depends(db.get_db_session)):

    color_crud = ColorRepository(session)

    color_db = await color_crud.get_product_color_by_id(id=color.id)

    if not color_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Color with id: {color.id} does not exist")

    updated_color = await color_crud.update_product_color(color)

    return updated_color


@router.delete("/colors/delete", response_model=ColorDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def color_delete(color: ColorDTO, session: AsyncSession = Depends(db.get_db_session)):

    color_crud = ColorRepository(session)

    color_db = await color_crud.get_product_color_by_id(id=color.id)

    if not color_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Color with id: {color.id} does not exist")

    deleted_color = await color_crud.delete_product_color(id=color.id)

    return Response(status_code=status.HTTP_200_OK, content=f"Color with id: {deleted_color.id} has been deleted")


@router.get("/colors/{id}", response_model=ColorDTO, status_code=status.HTTP_200_OK)
async def color_get_by_id(id: int, session: AsyncSession = Depends(db.get_db_session)):

    color_crud = ColorRepository(session)

    color_db = await color_crud.get_product_color_by_id(id=id)

    if not color_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Color with id: {id} does not exist")

    return color_db


@router.get("/colors/", response_model=Sequence[ColorDTO], status_code=status.HTTP_200_OK)
async def color_get_all(session: AsyncSession = Depends(db.get_db_session)):

    color_crud = ColorRepository(session)

    colors = await color_crud.get_all_product_colors()

    if not colors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No color found")

    return colors


#########################
# BLOCK FOR SIZE ROUTES #
#########################


@router.post("/sizes/create", response_model=SizeDTO, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
async def create_new_size(size: SizeDTO, session: AsyncSession = Depends(db.get_db_session)):

    size_crud = SizeRepository(session)

    size_exists = await size_crud.get_product_size_by_name(name=size.name)
    if size_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This product size is already registered.")
    new_size = await size_crud.create_product_size(size)
    return new_size


@router.put("/sizes/update", response_model=SizeDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def size_update(size: SizeDTO, session: AsyncSession = Depends(db.get_db_session)):

    size_crud = SizeRepository(session)

    size_db = await size_crud.get_product_size_by_id(id=size.id)

    if not size_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Size with id: {size.id} does not exist")

    updated_size = await size_crud.update_product_size(size)

    return updated_size


@router.delete("/sizes/delete", response_model=SizeDTO, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def size_delete(size: SizeDTO, session: AsyncSession = Depends(db.get_db_session)):

    size_crud = SizeRepository(session)

    size_db = await size_crud.get_product_size_by_id(id=size.id)

    if not size_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Size with id: {size.id} does not exist")

    deleted_size = await size_crud.delete_product_size(id=size.id)

    return Response(status_code=status.HTTP_200_OK, content=f"Size with id: {deleted_size.id} has been deleted")


@router.get("/sizes/{id}", response_model=SizeDTO, status_code=status.HTTP_200_OK)
async def size_get_by_id(id: int, session: AsyncSession = Depends(db.get_db_session)):

    size_crud = SizeRepository(session)

    size_db = await size_crud.get_product_size_by_id(id=id)

    if not size_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Size with id: {id} does not exist")

    return size_db


@router.get("/sizes/", response_model=Sequence[SizeDTO], status_code=status.HTTP_200_OK)
async def size_get_all(session: AsyncSession = Depends(db.get_db_session)):

    size_crud = SizeRepository(session)

    sizes = await size_crud.get_all_product_sizes()

    if not sizes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No size found")

    return sizes


###########################
# BLOCK FOR RATING ROUTES #
###########################


@router.post("/ratings/create", response_model=RatingDTO, status_code=status.HTTP_201_CREATED)
async def create_new_rating(rating: RatingDTO, session: AsyncSession = Depends(db.get_db_session), cur_user: User = Depends(get_current_user)):
    rating.user_id = cur_user.id

    rating_crud = RatingRepository(session)
    new_rating = await rating_crud.create_rating(rating)

    return new_rating


@router.put("/ratings/update", response_model=RatingDTO, status_code=status.HTTP_200_OK)
async def rating_update(rating: RatingDTO, session: AsyncSession = Depends(db.get_db_session), cur_user: User = Depends(get_current_user)):

    rating_crud = RatingRepository(session)

    rating_db = await rating_crud.get_rating_by_id(id=rating.id)

    if not rating_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rating with id: {rating.id} does not exist")

    if not rating_db.user_id == cur_user.id and not cur_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    updated_rating = await rating_crud.update_rating(rating)

    return updated_rating


@router.delete("/ratings/delete", response_model=RatingDTO, status_code=status.HTTP_200_OK)
async def rating_delete(rating: RatingDTO, session: AsyncSession = Depends(db.get_db_session), cur_user: User = Depends(get_current_user)):

    rating_crud = RatingRepository(session)

    rating_db = await rating_crud.get_rating_by_id(id=rating.id)

    if not rating_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rating with id: {rating.id} does not exist")

    if not rating_db.user_id == cur_user.id and not cur_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    deleted_rating = await rating_crud.delete_rating(id=rating.id)

    return Response(status_code=status.HTTP_200_OK, content=f"Rating with id: {deleted_rating.id} has been deleted")


@router.get("/ratings/{id}", response_model=RatingDTO, status_code=status.HTTP_200_OK)
async def rating_get_by_id(id: int, session: AsyncSession = Depends(db.get_db_session)):

    rating_crud = RatingRepository(session)

    rating_db = await rating_crud.get_rating_by_id(id=id)

    if not rating_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rating with id: {id} does not exist")

    return rating_db


@router.get("/ratings/", response_model=Sequence[RatingDTO], status_code=status.HTTP_200_OK)
async def rating_get_all(session: AsyncSession = Depends(db.get_db_session)):

    rating_crud = RatingRepository(session)

    ratings = await rating_crud.get_all_ratings()

    if not ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No rating found")

    return ratings
