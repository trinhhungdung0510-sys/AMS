#!/usr/bin/env bash
# Khởi động AMS — Docker backend + frontend (chạy nền, không tắt khi đóng terminal)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/backend"
DEV_DIR="$ROOT/.dev"

mkdir -p "$DEV_DIR"

# shellcheck source=dev-lib.sh
source "$ROOT/scripts/dev-lib.sh"

if [[ -d /opt/homebrew/opt/expat/lib ]]; then
  export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
fi

echo "AMS — khởi động stack dev"
ensure_docker "$BACKEND"
ensure_backend_env "$BACKEND"
start_backend "$ROOT" "$BACKEND" "$DEV_DIR"
start_frontend "$ROOT" "$DEV_DIR"
print_dev_ready
