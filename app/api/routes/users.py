from fastapi import APIRouter, Depends, UploadFile

from app.api.dependencies import get_current_admin, get_current_user, get_current_user_id, get_current_user_id_optional, get_current_user_optional, get_user_service
from app.db.models.user import User
from app.schemas.schemas import UserOut, UserUpdate
from app.services.user import UserService


users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me")
async def get_me(current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.get_user(user_id=current_user.id)


@users_router.patch("/me")
async def update_me(data: UserUpdate, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.update_user(current_user.id, data)


@users_router.delete("/me")
async def delete_me(current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> bool:
    return await service.delete_user(current_user.id)


@users_router.get("/{user_id}")
async def get_user_by_id(user_id: int, current_user: User | None = Depends(get_current_user_optional), service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.get_user(user_id, current_user.id if current_user is not None else None)


@users_router.post("/{user_id}/follow")
async def follow_user(user_id: int, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> bool:
    return await service.follow_user(user_id, current_user.id)


@users_router.delete("/{user_id}/follow")
async def unfollow_user(user_id: int, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> bool:
    return await service.unfollow_user(user_id, current_user.id)




@users_router.patch("/{user_id}")
async def update_user(user_id: int, data: UserUpdate, admin: User = Depends(get_current_admin), service: UserService = Depends(get_user_service)) -> UserOut:
    return await service.update_user(user_id, data)


@users_router.delete("/{user_id}")
async def delete_user(user_id: int, admin: User = Depends(get_current_admin), service: UserService = Depends(get_user_service)) -> bool:
    return await service.delete_user(user_id)
