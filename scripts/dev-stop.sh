#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEV_DIR="$ROOT/.dev"

# shellcheck source=dev-lib.sh
source "$ROOT/scripts/dev-lib.sh"

stop_pid_file "$DEV_DIR/backend.pid"
stop_pid_file "$DEV_DIR/frontend.pid"
stop_host_uvicorn

if lsof -ti tcp:5173 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Dừng frontend port 5173"
  lsof -ti tcp:5173 -sTCP:LISTEN | xargs kill 2>/dev/null || true
fi

cat <<'EOF'
Đã dừng frontend + uvicorn local.

⚠️  Web http://localhost:5173 sẽ không truy cập được cho đến khi chạy lại:
    npm run dev:up

Docker (postgres, redis, backend, vision) vẫn chạy.
Dừng Docker: cd backend && docker compose down
EOF
