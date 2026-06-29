#!/usr/bin/env bash
# Docker compose + tự động bật frontend — tránh chỉ có API mà không có web
set -euo pipefail

BACKEND="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$BACKEND/.." && pwd)"

cd "$BACKEND"
docker compose up -d "$@"

echo ""
echo "Docker stack đã chạy. Đang bật frontend web..."
bash "$ROOT/scripts/dev-up.sh"
