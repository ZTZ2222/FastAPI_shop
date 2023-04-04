from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.services.database.models import Product, Color, Size
from ..base import BaseRepository
from app.services.database.schemas.product import ProductCreate, ProductUpdate, ProductResponse, SizeDTO, ColorDTO


class SizeRepository(BaseRepository):
    model = Size

    async def create_product_size(self, size: SizeDTO) -> Size:
        return await self._insert(**size.dict(exclude_unset=True, exclude_none=True))

    async def get_product_size_by_id(self, id: int) -> Size:
        return await self._select_one(Size.id == id)

    async def get_product_size_by_name(self, name: str) -> Size:
        return await self._select_one(Size.name == name)

    async def get_all_product_sizes(self) -> list[Size]:
        return await self._select_all()

    async def update_product_size(self, size: SizeDTO) -> Size:
        size_data = size.dict(exclude_unset=True, exclude_none=True)
        return await self._update(Size.id == size.id, **size_data)

    async def delete_product_size(self, id: int) -> Size:
        return await self._delete(Size.id == id)


class ColorRepository(BaseRepository):
    model = Color

    async def create_product_color(self, color: ColorDTO) -> Color:
        return await self._insert(**color.dict(exclude_unset=True, exclude_none=True))

    async def get_product_color_by_id(self, id: int) -> Color:
        return await self._select_one(Color.id == id)

    async def get_product_color_by_name(self, name: str) -> Color:
        return await self._select_one(Color.name == name)

    async def get_all_product_colors(self) -> list[Color]:
        return await self._select_all()

    async def update_product_color(self, color: ColorDTO) -> Color:
        color_data = color.dict(exclude_unset=True, exclude_none=True)
        return await self._update(Color.id == color.id, **color_data)

    async def delete_product_color(self, id: int) -> Color:
        return await self._delete(Color.id == id)


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

    async def get_product_by_name(self, name: str) -> Product:
        async with self.session as session:
            stmt = select(Product).where(Product.name == name).options(selectinload(Product.category), selectinload(
                Product.brand), selectinload(Product.color), selectinload(Product.size), selectinload(Product.ratings))
            result = await session.scalar(stmt)
        return result

    async def update_product(self, product: ProductUpdate) -> Product:
        product_data = product.dict(exclude_unset=True, exclude_none=True)
        updated_product = await self._update(Product.id == product.id, **product_data)
        return await self.get_product_by_id(id=updated_product.id)

    async def delete_product(self, id: int) -> Product:
        return await self._delete(Product.id == id)

    async def get_all_products(self, offset: int, limit: int) -> list[Product]:
        async with self.session as session:
            stmt = select(Product).options(
                selectinload(Product.category),
                selectinload(Product.brand),
                selectinload(Product.color),
                selectinload(Product.size),
                selectinload(Product.ratings)
            ).offset(offset).limit(limit)
            result = await session.scalars(stmt)
        return result.all()
