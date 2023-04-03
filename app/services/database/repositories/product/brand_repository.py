from app.services.database.models import Brand
from app.services.database.schemas.product import BrandDTO
from ..base import BaseRepository


class BrandRepository(BaseRepository):
    model = Brand

    async def create_brand(self, brand: BrandDTO) -> Brand:
        return await self._insert(**brand.dict(exclude_unset=True, exclude_none=True))

    async def get_brand_by_id(self, id: int) -> Brand:
        return await self._select_one(Brand.id == id)

    async def get_brand_by_name(self, name: str) -> Brand:
        return await self._select_one(Brand.name == name)

    async def get_all_brands(self) -> list[Brand]:
        return await self._select_all()

    async def update_brand(self, brand: BrandDTO) -> Brand:
        brand_data = brand.dict(exclude_unset=True, exclude_none=True)
        return await self._update(Brand.id == brand.id, **brand_data)

    async def delete_brand(self, id: int) -> Brand:
        return await self._delete(Brand.id == id)
