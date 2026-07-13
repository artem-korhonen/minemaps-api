from datetime import datetime, timezone

from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.map import FavouriteMap, Map


class MapRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    

    async def create(self, name: str, description: str, owner_id: int, is_published: bool) -> Map:
        map_obj = Map(
            name=name,
            description=description,
            owner_id=owner_id,
            is_published=is_published
        )

        self.session.add(map_obj)

        try:
            await self.session.commit()
            await self.session.refresh(map_obj)
        except Exception:
            await self.session.rollback()
            raise

        return map_obj

    
    async def get_by_id(self, map_id: int) -> Map | None:
        result = await self.session.execute(
            select(Map)
            .where(
                Map.id == map_id,
                Map.deleted_at.is_(None)
            )
        )

        return result.scalar_one_or_none()
    

    async def update(self, map_id: int, name: str | None, description: str | None, is_published: bool | None) -> Map | None:
        map_obj: Map = await self.get_by_id(map_id)
        if map_obj is None or map_obj.deleted_at is not None:
            return None
        
        if name is not None:
            map_obj.name = name
        if description is not None:
            map_obj.description = description
        if is_published is not None:
            map_obj.is_published = is_published
        
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return map_obj
    

    async def delete(self, map_id: int) -> bool:
        result = await self.session.execute(
            update(Map)
            .where(
                Map.id == map_id
            )
            .values(
                deleted_at=datetime.now(timezone.utc)
            )
        )

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return result.rowcount > 0


    async def favourite(self, map_id: int, user_id: int) -> None:
        favourite_map = FavouriteMap(
            map_id=map_id,
            user_id=user_id
        )

        self.session.add(favourite_map)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
    

    async def unfavourite(self, map_id: int, user_id: int) -> bool:
        result = await self.session.execute(
            delete(FavouriteMap)
            .where(
                FavouriteMap.map_id == map_id,
                FavouriteMap.user_id == user_id
            )
        )

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return result.rowcount > 0


    async def is_favourite(self, map_id: int, user_id: int) -> bool:
        result = await self.session.execute(
            select(
                exists()
                .where(
                    FavouriteMap.map_id == map_id,
                    FavouriteMap.user_id == user_id
                )
            )
        )

        return result.scalar()