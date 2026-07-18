import uvicorn
from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routes.router import router
from app.core.settings import settings
from app.db.init_db import init_db
from app.services.storage import StorageService


async def lifespan(app: FastAPI):
    storage = StorageService(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
        bucket_name=settings.S3_BUCKET_NAME,
    )

    await storage.connect()
    await init_db()

    app.state.storage = storage

    yield

    await storage.close()


app = FastAPI(title="MineMaps API", version="0.1.0", lifespan=lifespan)

app.include_router(router)
register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run(app)
