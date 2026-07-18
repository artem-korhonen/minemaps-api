from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_current_user,
    get_current_user_optional,
    get_map_service,
)
from app.db.models.user import User
from app.schemas.schemas import MapCreate, MapOut, MapUpdate
from app.services.map import MapService

maps_router = APIRouter(prefix="/maps", tags=["maps"])


@maps_router.post("/")
async def create_map(
    data: MapCreate,
    current_user: User = Depends(get_current_user),
    service: MapService = Depends(get_map_service),
):
    return await service.create_map(data, current_user.id)


@maps_router.get("/{map_id}")
async def get_map(
    map_id: int,
    current_user: int | None = Depends(get_current_user_optional),
    service: MapService = Depends(get_map_service),
) -> MapOut:
    return await service.get_map(
        map_id, current_user.id if current_user is not None else None
    )


@maps_router.put("/{map_id}")
async def update_map(
    map_id: int,
    data: MapUpdate,
    current_user: User = Depends(get_current_user),
    service: MapService = Depends(get_map_service),
):
    return await service.update_map(map_id, data, current_user.id)


@maps_router.delete("/{map_id}")
async def delete_map(
    map_id: int,
    current_user: User = Depends(get_current_user),
    service: MapService = Depends(get_map_service),
):
    return await service.delete_map(map_id, current_user.id)


@maps_router.post("/{map_id}/favourite")
async def favourite_map(
    map_id: int,
    current_user: User = Depends(get_current_user),
    service: MapService = Depends(get_map_service),
) -> bool:
    return await service.favourite_map(map_id, current_user.id)


@maps_router.delete("/{map_id}/favourite")
async def unfavourite_map(
    map_id: int,
    current_user: User = Depends(get_current_user),
    service: MapService = Depends(get_map_service),
) -> bool:
    return await service.unfavourite_map(map_id, current_user.id)
