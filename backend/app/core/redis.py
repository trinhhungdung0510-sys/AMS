from functools import lru_cache

from redis import Redis

from app.core.config import get_settings


@lru_cache
def get_redis_client() -> Redis:
    settings = get_settings()
    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=2,
        retry_on_timeout=True,
    )


def check_redis_connection() -> bool:
    try:
        return bool(get_redis_client().ping())
    except Exception:
        return False
