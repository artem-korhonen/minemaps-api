from app.db.base import SessionLocal


async def get_session():
    async with SessionLocal() as session:
        yield session