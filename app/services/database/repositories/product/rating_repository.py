from app.services.database.models import Rating
from app.services.database.schemas.product import RatingDTO
from ..base import BaseRepository


class RatingRepository(BaseRepository):
    model = Rating

    async def create_rating(self, rating: RatingDTO) -> Rating:
        return await self._insert(**rating.dict(exclude_unset=True, exclude_none=True))

    async def get_rating_by_id(self, id: int) -> Rating:
        return await self._select_one(Rating.id == id)

    async def get_rating_by_name(self, name: str) -> Rating:
        return await self._select_one(Rating.name == name)

    async def get_all_ratings(self) -> list[Rating]:
        return await self._select_all()

    async def update_rating(self, rating: RatingDTO) -> Rating:
        rating_data = rating.dict(exclude_unset=True, exclude_none=True)
        return await self._update(Rating.id == rating.id, **rating_data)

    async def delete_rating(self, id: int) -> Rating:
        return await self._delete(Rating.id == id)
