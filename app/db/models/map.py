from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func, select, text
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.db.base import Base


class Map(Base):
    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(4096), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    is_published: Mapped[bool] = mapped_column(server_default=text("false"))  # creator
    is_visible: Mapped[bool] = mapped_column(server_default=text("true"))  # admin

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class FavouriteMap(Base):
    __tablename__ = "maps_favourites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


Map.favourites_count = column_property(
    select(func.count(FavouriteMap.user_id))
    .where(FavouriteMap.map_id == Map.id)
    .correlate_except(FavouriteMap)
    .scalar_subquery()
)
