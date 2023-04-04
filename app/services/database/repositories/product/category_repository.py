from sqlalchemy.orm import joinedload
from app.services.database.models import Category
from app.services.database.models import Product
from app.services.database.schemas.product import CategoryDTO
from ..base import BaseRepository
from sqlalchemy import select


class CategoryRepository(BaseRepository):
    model = Category

    async def create_category(self, category: CategoryDTO) -> Category:
        return await self._insert(**category.dict(exclude_unset=True, exclude_none=True))

    async def get_category_by_id(self, id: int) -> Category:
        return await self._select_one(Category.id == id)

    async def get_category_by_name(self, category_name: str) -> Category:
        async with self.session as session:
            stmt = select(Category).where(Category.name == category_name)
            result = await session.scalar(stmt)
        return result

    async def get_all_categories(self) -> list[Category]:
        return await self._select_all()

    async def update_category(self, category: CategoryDTO) -> Category:
        category_data = category.dict(exclude_unset=True, exclude_none=True)
        return await self._update(Category.id == category.id, **category_data)

    async def delete_category(self, id: int) -> Category:
        return await self._delete(Category.id == id)

    async def get_category_with_products(self, category_name: str, offset: int, limit: int):
        async with self.session as session:
            stmt = select(Category).where(Category.name == category_name).options(
                joinedload(Category.products)
                .joinedload(Product.color),
                joinedload(Category.products)
                .joinedload(Product.size),
                joinedload(Category.products)
                .joinedload(Product.ratings)
            ).offset(offset).limit(limit)
            result = await session.scalar(stmt)
        return result
