import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    redis_url: str
    cached_ttl_seconds: int
    cached_task_key: str
    cached_category_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres",
        ),
        redis_url=os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0",
        ),
        cached_ttl_seconds=3600,
        cached_task_key="cache:tasks_list",
        cached_category_key="cache:categories_list",
    )
