from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.redis import check_redis_connection


def check_database(db: Session) -> str:
    db.execute(text("SELECT 1"))
    return "ok"


def check_redis() -> str:
    return "ok" if check_redis_connection() else "unavailable"
