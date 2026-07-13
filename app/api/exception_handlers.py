from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors.auth import ForbiddenError, InvalidTokenError, UnauthorizedError
from app.errors.map import FavouriteMapError, FavouriteNotFoundError, MapNotFoundError
from app.errors.user import FollowNotFoundError, FollowUserConflictError, FollowUserError, InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
    app.add_exception_handler(FollowUserConflictError, follow_user_conflict_handler)
    app.add_exception_handler(FollowUserError, follow_user_handler)
    app.add_exception_handler(FollowNotFoundError, follow_not_found_handler)
    app.add_exception_handler(ForbiddenError, forbidden_handler)
    app.add_exception_handler(MapNotFoundError, map_not_found_handler)
    app.add_exception_handler(FavouriteMapError, favourite_map_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_handler)
    app.add_exception_handler(FavouriteNotFoundError, favourite_not_found_handler)


async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "User not found"
        }
    )


async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "User with this email or name already exists"
        }
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid Credentials"
        }
    )


async def follow_user_conflict_handler(request: Request, exc: FollowUserConflictError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Follower and Followed User must be different"
        }
    )


async def follow_user_handler(request: Request, exc: FollowUserError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Cannot follow user"
        }
    )


async def follow_not_found_handler(request: Request, exc: FollowNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Follow not found"
        }
    )


async def forbidden_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=403,
        content={
            "detail": "Forbidden"
        }
    )


async def map_not_found_handler(request: Request, exc: MapNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Map not found"
        }
    )


async def favourite_map_handler(request: Request, exc: FavouriteMapError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Cannot favourite map"
        }
    )


async def unauthorized_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Unauthorized"
        }
    )


async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid token"
        }
    )


async def favourite_not_found_handler(request: Request, exc: FavouriteNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Favourite not found"
        }
    )
