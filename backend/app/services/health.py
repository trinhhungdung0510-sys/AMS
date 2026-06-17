from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings


def check_database(db: Session) -> str:
    db.execute(text("SELECT 1"))
    return "ok"


def check_redis() -> str:
    settings = get_settings()
    client = Redis.from_url(settings.redis_url, socket_connect_timeout=1)
    try:
        return "ok" if client.ping() else "unavailable"
    finally:
        client.close()
