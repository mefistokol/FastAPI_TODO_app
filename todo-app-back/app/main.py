from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router
from app.api.routers.category import cat_router
from app.cache.redis import get_redis_cache


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await get_redis_cache().redis.aclose()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=cat_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)
