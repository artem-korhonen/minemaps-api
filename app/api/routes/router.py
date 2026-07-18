from fastapi import APIRouter

from app.api.routes.auth import auth_router
from app.api.routes.users import users_router
from app.api.routes.maps import maps_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(maps_router)
