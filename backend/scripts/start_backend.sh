#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -d /opt/homebrew/opt/expat/lib ]]; then
  export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
fi

if [[ ! -f .env ]]; then
  echo "Thiếu backend/.env — copy từ .env.example và chỉnh DATABASE_URL/REDIS_URL."
  exit 1
fi

if [[ ! -x .venv/bin/uvicorn ]]; then
  echo "Backend chưa sẵn sàng: thiếu .venv hoặc uvicorn."
  echo
  echo "Cài lại môi trường (Python 3.12+):"
  echo "  cd backend"
  echo "  python3.12 -m venv .venv"
  echo "  source .venv/bin/activate"
  echo "  pip install -r requirements.txt"
  echo
  echo "Nếu pip/venv lỗi expat trên macOS, xem ENVIRONMENT_RECOVERY.md"
  exit 1
fi

exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
