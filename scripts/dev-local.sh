#!/usr/bin/env bash
# Khởi động AMS + theo dõi log (Ctrl+C chỉ thoát tail — frontend/backend vẫn chạy)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEV_DIR="$ROOT/.dev"

bash "$ROOT/scripts/dev-up.sh"
open_browser

echo "Theo dõi log (Ctrl+C không dừng web — dùng npm run dev:stop)"
tail -f "$DEV_DIR/frontend.log" "$DEV_DIR/backend.log" 2>/dev/null
