import uvicorn
from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routes.router import router
from app.db.init_db import init_db


async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="MineMaps API", version="0.1.0", lifespan=lifespan)

app.include_router(router)
register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run(app)
