from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from app.core.settings import settings
from app.core.security import check_password, create_access_token, hash_password
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.errors.storage import FileTooLargeError, IncorrectFileError
from app.errors.user import (
    FollowNotFoundError,
    FollowUserConflictError,
    FollowUserError,
    InvalidCredentialsError,
    ProfileImageUpdateError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.schemas.schemas import Login, Register, Token, UserOut, UserUpdate
from app.services.storage import StorageService


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, data: Register) -> Token:
        try:
            password_hash = hash_password(data.password)
            user = await self.repository.create(data.name, data.email, password_hash)
            return Token(access_token=create_access_token(user.id))
        except IntegrityError:
            raise UserAlreadyExistsError()

    async def login_user(self, data: Login) -> Token:
        user: User = await self.repository.get_by_email(data.email)
        if not user or not check_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        return Token(access_token=create_access_token(user.id))

    async def get_user(
        self, user_id: int, current_user_id: int | None = None
    ) -> UserOut:
        user: User = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        is_following = None
        if current_user_id is not None and current_user_id != user_id:
            is_following = await self.repository.is_following(user_id, current_user_id)

        return UserOut(
            name=user.name,
            created_at=user.created_at,
            followers_count=user.followers_count,
            following_count=user.following_count,
            is_following=is_following,
            profile_image_url=settings.S3_PUBLIC_URL + "/" + user.profile_image_key
        )

    async def get_user_model(self, user_id: int) -> User | None:
        user: User = await self.repository.get_by_id(user_id)
        return user

    async def delete_user(self, user_id: int) -> bool:
        deleted: bool = await self.repository.delete(user_id)
        if not deleted:
            raise UserNotFoundError()

        return deleted

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        try:
            user: User = await self.repository.update(
                user_id,
                data.name,
                data.email,
                None if not data.password else hash_password(data.password),
            )
        except IntegrityError:
            raise UserAlreadyExistsError()

        if user is None:
            raise UserNotFoundError()

        return user

    async def follow_user(self, followed_user_id: int, follower_id: int) -> bool:
        if followed_user_id == follower_id:
            raise FollowUserConflictError()

        user: User = await self.repository.get_by_id(followed_user_id)
        if not user:
            raise UserNotFoundError()

        try:
            await self.repository.follow(followed_user_id, follower_id)
        except IntegrityError:
            raise FollowUserError()

        return True

    async def unfollow_user(self, followed_user_id: int, follower_id: int) -> bool:
        unfollowed: bool = await self.repository.unfollow(followed_user_id, follower_id)

        if not unfollowed:
            raise FollowNotFoundError()

        return unfollowed

    async def update_image(
        self, user_id: int, file: UploadFile, storage: StorageService
    ) -> bool:
        if not file.size:
            raise IncorrectFileError()

        if file.content_type not in ["image/png", "image/jpeg", "image/webp"]:
            raise IncorrectFileError()

        if file.size > settings.MAX_IMAGE_SIZE:
            raise FileTooLargeError()

        key = f"users/{user_id}.webp"
        await storage.upload_image(file, key)

        try:
            updated = await self.repository.update_profile_image(user_id, key)
        except Exception:
            await storage.delete_image(key)
            raise ProfileImageUpdateError()

        if not updated:
            await storage.delete_image(key)
            raise UserNotFoundError()

        return True
