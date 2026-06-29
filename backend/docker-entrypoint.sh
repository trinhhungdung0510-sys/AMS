#!/bin/sh
set -e

cd /app

echo "[backend] Waiting for database..."
until python - <<'PY'
import os
import sys
from sqlalchemy import create_engine, text

url = os.environ.get("DATABASE_URL", "")
if not url:
    sys.exit(1)
engine = create_engine(url, pool_pre_ping=True)
with engine.connect() as conn:
    conn.execute(text("SELECT 1"))
PY
do
  sleep 2
done

echo "[backend] Running migrations..."
alembic upgrade head

echo "[backend] Starting AMS API on :8000"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
