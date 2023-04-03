
from fastapi import HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import lazyload, selectinload
from sqlalchemy.orm.interfaces import MapperOption
from app.services.database.models import Product, Color, Size
from ..base import BaseRepository
from app.services.database.schemas.product import ProductCreate, ProductUpdate, ProductResponse


class ProductRepository(BaseRepository):
    model = Product

    async def create_product(self, product: ProductCreate) -> Product:
        new_product = await self._insert(**product.dict(exclude_unset=True, exclude_none=True))
        return await self.get_product_by_id(id=new_product.id)

    async def get_product_by_id(self, id: int) -> ProductResponse:
        async with self.session as session:
            stmt = select(Product).where(Product.id == id).options(selectinload(Product.category), selectinload(
                Product.brand), selectinload(Product.color), selectinload(Product.size), selectinload(Product.ratings))
            result = await session.scalar(stmt)
        return result

    async def get_product_by_name(self, name: str):
        async with self.session as session:
            stmt = select(Product).where(Product.name == name).options(selectinload(Product.category), selectinload(
                Product.brand), selectinload(Product.color), selectinload(Product.size), selectinload(Product.ratings))
            result = await session.scalar(stmt)
        return result

    async def update_product(self, product: ProductUpdate):
        product_data = product.dict(exclude_unset=True, exclude_none=True)
        updated_product = await self._update(Product.id == product.id, **product_data)
        return await self.get_product_by_id(id=updated_product.id)

    async def delete_product(self, id: int):
        return await self._delete(Product.id == id)
