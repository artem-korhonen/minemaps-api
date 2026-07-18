from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token, oauth2_scheme
from app.db.models.user import User, UserRole
from app.db.repositories.map import MapRepository
from app.db.session import get_session
from app.db.repositories.user import UserRepository
from app.errors.auth import ForbiddenError
from app.errors.user import UserNotFoundError
from app.services.map import MapService
from app.services.storage import StorageService
from app.services.user import UserService


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)


def get_map_repository(session: AsyncSession = Depends(get_session)) -> MapRepository:
    return MapRepository(session)


def get_map_service(
    repository: MapRepository = Depends(get_map_repository),
) -> MapService:
    return MapService(repository)


def get_storage_service(request: Request) -> StorageService:
    return request.app.state.storage


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    return decode_access_token(token)


def get_current_user_id_optional(
    token: str | None = Depends(oauth2_scheme),
) -> int | None:
    if token is None:
        return None

    return decode_access_token(token)


async def _get_user_or_none(user_id: int | None, service: UserService) -> User | None:
    if user_id is None:
        return None

    user = await service.get_user_model(user_id)

    if user is None or user.deleted_at is not None:
        return None

    return user


async def get_current_user(
    current_user_id: int = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
) -> User:
    user = await _get_user_or_none(current_user_id, service)
    if user is None:
        raise UserNotFoundError()

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError()

    return current_user


async def get_current_user_optional(
    current_user_id: int | None = Depends(get_current_user_id_optional),
    service: UserService = Depends(get_user_service),
) -> User | None:
    return await _get_user_or_none(current_user_id, service)
