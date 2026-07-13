from sqlalchemy.exc import IntegrityError

from app.db.models.map import Map
from app.db.repositories.map import MapRepository
from app.db.repositories.user import UserRepository
from app.errors.auth import ForbiddenError
from app.errors.map import FavouriteMapError, FavouriteNotFoundError, MapNotFoundError
from app.schemas.schemas import MapCreate, MapOut, MapUpdate


class MapService:
    def __init__(self, repository: MapRepository):
        self.repository = repository
    

    async def create_map(self, data: MapCreate, current_user_id: int) -> Map:
        return await self.repository.create(
            name=data.name,
            description=data.description,
            owner_id=current_user_id,
            is_published=data.is_published
        )

    
    async def get_map(self, map_id: int, current_user_id: int | None) -> MapOut:
        map_obj = await self.repository.get_by_id(map_id)
        if map_obj is None:
            raise MapNotFoundError()
        
        if not map_obj.is_published and map_obj.owner_id != current_user_id:
            raise MapNotFoundError()
        
        return map_obj
    

    async def update_map(self, map_id: int, data: MapUpdate, current_user_id: int):
        map_obj = await self.repository.get_by_id(map_id)

        if map_obj is None:
            raise MapNotFoundError()

        if map_obj.owner_id != current_user_id:
            raise ForbiddenError()
        
        return await self.repository.update(
            map_id=map_id,
            name=data.name,
            description=data.description,
            is_published=data.is_published
        )
    

    async def delete_map(self, map_id: int, current_user_id: int) -> bool:
        map_obj = await self.repository.get_by_id(map_id)

        if map_obj is None:
            raise MapNotFoundError()

        if map_obj.owner_id != current_user_id:
            raise ForbiddenError()

        deleted = await self.repository.delete(map_id)
        return deleted


    async def favourite_map(self, map_id: int, current_user_id: int) -> bool:
        map_obj = await self.repository.get_by_id(map_id)
        if map_obj is None:
            raise MapNotFoundError()
        
        try:
            await self.repository.favourite(map_id, current_user_id)
        except IntegrityError:
            raise FavouriteMapError()
        
        return True


    async def unfavourite_map(self, map_id: int, current_user_id: int) -> bool:
        unfavourited = await self.repository.unfavourite(map_id, current_user_id)
        
        if not unfavourited:
            raise FavouriteNotFoundError()
        
        return True
