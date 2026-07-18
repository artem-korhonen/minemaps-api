from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, String, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app.db.base import Base


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        String(16), server_default=UserRole.USER, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class FollowUser(Base):
    __tablename__ = "users_follows"

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followed_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id])
    followed_user: Mapped["User"] = relationship(
        "User", foreign_keys=[followed_user_id]
    )


User.followers_count = column_property(
    select(func.count(FollowUser.follower_id))
    .where(FollowUser.followed_user_id == User.id)
    .correlate_except(FollowUser)
    .scalar_subquery()
)

User.following_count = column_property(
    select(func.count(FollowUser.followed_user_id))
    .where(FollowUser.follower_id == User.id)
    .correlate_except(FollowUser)
    .scalar_subquery()
)
