from app.services.database.models import Category
from app.services.database.schemas.product import CategoryDTO
from ..base import BaseRepository


class CategoryRepository(BaseRepository):
    model = Category

    async def create_category(self, category: CategoryDTO) -> Category:
        return await self._insert(**category.dict(exclude_unset=True, exclude_none=True))

    async def get_category_by_id(self, id: int) -> Category:
        return await self._select_one(Category.id == id)

    async def get_category_by_name(self, name: str) -> Category:
        return await self._select_one(Category.name == name)

    async def get_all_categories(self) -> list[Category]:
        return await self._select_all()

    async def update_category(self, category: CategoryDTO) -> Category:
        category_data = category.dict(exclude_unset=True, exclude_none=True)
        return await self._update(Category.id == category.id, **category_data)

    async def delete_category(self, id: int) -> Category:
        return await self._delete(Category.id == id)

    async def get_category_products(self):
        pass
