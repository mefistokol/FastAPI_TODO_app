import json
from functools import lru_cache
from typing import Any
from redis import Redis



class RedisCachedBackend:
    def __init__(self, redis_url: str, cached_ttl_seconds: int | None = None):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.cached_ttl_seconds = cached_ttl_seconds

    def set(self, key: str, value: Any) -> None:
        self.redis.set(key, json.dumps(value), ex=self.cached_ttl_seconds)
    
    def get(self, key: str) -> Any | None:
        value = self.redis.get(key)
        if value is not None:
            return json.loads(value)

    def delete(self, key: str) -> None:
        self.redis.delete(key)


@lru_cache
def get_redis_cache() -> RedisCachedBackend:
    from app.core.config import get_settings
    settings = get_settings()
    return RedisCachedBackend(settings.redis_url, settings.cached_ttl_seconds)