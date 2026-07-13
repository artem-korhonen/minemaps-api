from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_service
from app.schemas.schemas import Login, Register, Token, UserOut
from app.services.user import UserService


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(data: Register, service: UserService = Depends(get_user_service)) -> Token:
    return await service.create_user(data)


# @auth_router.post("/login")
# async def login(data: Login, service: UserService = Depends(get_user_service)) -> Token:
#     return await service.login_user(data)


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)) -> Token:
    data = Login(email=form_data.username, password=form_data.password)
    return await service.login_user(data)