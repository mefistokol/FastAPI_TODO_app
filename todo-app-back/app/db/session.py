from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.DATABASE_URL, pool_size=20, max_overflow=10)
sessionlocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with sessionlocal() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
