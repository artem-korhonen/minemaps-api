from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class Register(BaseSchema):
    name: str = Field(min_length=2, max_length=64)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class Login(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=2, max_length=64)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserOut(BaseSchema):
    name: str
    created_at: datetime
    followers_count: int
    following_count: int
    is_following: bool | None = None
    profile_image_url: str | None


class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class MapCreate(BaseSchema):
    name: str
    description: str
    is_published: bool


class MapUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    is_published: bool | None = None


class MapOut(BaseSchema):
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    favourites_count: int
