from datetime import datetime, timezone

from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import FollowUser, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    

    async def create(self, name: str, email: str, password_hash: str) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        try:
            self.session.add(user)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        await self.session.refresh(user)
        return user
        
    
    async def get_by_id(self, user_id: int) -> User | None:
        print("repository.get_by_id:", user_id)
        
        result = await self.session.execute(
            select(User)
            .where(
                User.id == user_id,
                User.deleted_at.is_(None)
            )
        )

        return result.scalar_one_or_none()


    async def get_by_name(self, name: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .where(
                User.name == name,
                User.deleted_at.is_(None)
            )
        )

        return result.scalar_one_or_none()
    

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .where(
                User.email == email,
                User.deleted_at.is_(None)
            )
        )

        return result.scalar_one_or_none()
    

    async def update(self, user_id: int, name: str | None, email: str | None, password_hash: str | None) -> User | None:
        user: User = await self.get_by_id(user_id)
        if user is None or user.deleted_at is not None:
            return None
        
        if name is not None: 
            user.name = name
        if email is not None: 
            user.email = email
        if password_hash is not None: 
            user.password_hash = password_hash

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


        await self.session.refresh(user)
        return user
    

    async def delete(self, user_id: int) -> bool:
        try:
            result = await self.session.execute(
                update(User)
                .where(
                    User.id == user_id,
                    User.deleted_at.is_(None)
                )
                .values(
                    email=f"deleted_{user_id}@deleted.local",
                    deleted_at=datetime.now(timezone.utc)
                )
            )

            if result.rowcount > 0:
                await self.session.execute(
                    delete(FollowUser)
                    .where(
                        FollowUser.follower_id == user_id
                    )
                )
            
            await self.session.commit()
        
        except Exception:
            await self.session.rollback()
            raise

        return result.rowcount > 0
    

    async def follow(self, followed_user_id: int, follower_id: int) -> None:
        self.session.add(
            FollowUser(
                followed_user_id=followed_user_id,
                follower_id=follower_id
            )
        )

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


    async def unfollow(self, followed_user_id: int, follower_id: int) -> bool:
        result = await self.session.execute(
            delete(FollowUser)
            .where(
                FollowUser.followed_user_id == followed_user_id,
                FollowUser.follower_id == follower_id
            )
        )

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return result.rowcount > 0


    async def is_following(self, followed_user_id: int, follower_id: int) -> bool:
        result = await self.session.execute(
            select(
                exists()
                .where(
                    FollowUser.followed_user_id == followed_user_id,
                    FollowUser.follower_id == follower_id
                )
            )
        )

        return result.scalar()