#!/usr/bin/env bash
# Shared helpers for AMS dev scripts (source only — do not execute directly)
dev_lib_root() {
  local lib_dir
  lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  echo "$(cd "$lib_dir/.." && pwd)"
}

wait_for_http() {
  local url="$1"
  local label="$2"
  local attempts="${3:-45}"

  for _ in $(seq 1 "$attempts"); do
    if curl -sf "$url" >/dev/null 2>&1; then
      echo "  ✓ $label sẵn sàng"
      return 0
    fi
    sleep 1
  done

  echo "  ✗ $label không phản hồi sau ${attempts}s"
  return 1
}

port_pids() {
  local port="$1"
  lsof -ti tcp:"$port" -sTCP:LISTEN 2>/dev/null || true
}

backend_health_ffmpeg() {
  curl -sf "http://127.0.0.1:8000/api/health" 2>/dev/null \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('ffmpeg',{}).get('ffmpeg',''))" 2>/dev/null \
    || true
}

is_docker_backend_healthy() {
  local backend_dir="$1"
  (cd "$backend_dir" && docker compose ps backend 2>/dev/null | grep -q "(healthy)")
}

stop_host_uvicorn() {
  local pid cmd
  for pid in $(port_pids 8000); do
    cmd="$(ps -p "$pid" -o command= 2>/dev/null || true)"
    if [[ "$cmd" == *"uvicorn app.main"* ]] || [[ "$cmd" == *"multiprocessing.spawn"* ]]; then
      echo "  ! Dừng uvicorn local (PID $pid) — tránh trùng port với Docker backend"
      kill "$pid" 2>/dev/null || true
    fi
  done
  sleep 1
}

stop_pid_file() {
  local pid_file="$1"
  if [[ -f "$pid_file" ]]; then
    local pid
    pid="$(cat "$pid_file" 2>/dev/null || true)"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
    fi
    rm -f "$pid_file"
  fi
}

ensure_docker() {
  local backend_dir="$1"
  if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: Docker chưa cài. Mở Docker Desktop rồi chạy lại."
    exit 1
  fi

  if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker Desktop chưa chạy. Khởi động Docker Desktop rồi thử lại."
    exit 1
  fi

  echo "==> Docker (postgres + redis + backend + vision)"
  (cd "$backend_dir" && docker compose up -d)
}

ensure_backend_env() {
  local backend_dir="$1"
  if [[ -f "$backend_dir/.env" ]]; then
    return 0
  fi

  echo "==> Tạo backend/.env từ mẫu local"
  cat >"$backend_dir/.env" <<'EOF'
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://ams:ams_password@127.0.0.1:5432/ams
REDIS_URL=redis://127.0.0.1:6379/0
JWT_SECRET_KEY=dev-local-jwt-secret-change-before-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174
FFPROBE_PATH=ffprobe
FFMPEG_PATH=ffmpeg
CAMERA_RTSP_TEST_TIMEOUT_SECONDS=15
CAMERA_SNAPSHOT_TIMEOUT_SECONDS=20
UPLOADS_ROOT=uploads
DEMO_MODE=false
DEMO_AUTO_START=true
DEMO_SEED_ON_STARTUP=true
DEMO_SEED_COUNT=12
DEMO_INTERVAL_SECONDS=20
STRESS_TEST_ENABLED=false
EOF
}

start_backend() {
  local root="$1"
  local backend_dir="$2"
  local dev_dir="$3"
  local backend_log="$dev_dir/backend.log"
  local backend_pid="$dev_dir/backend.pid"

  stop_host_uvicorn

  if is_docker_backend_healthy "$backend_dir"; then
    echo "==> Backend Docker (ams-backend, http://127.0.0.1:8000)"
    if wait_for_http "http://127.0.0.1:8000/api/health" "Docker Backend" 60; then
      local ffmpeg_path
      ffmpeg_path="$(backend_health_ffmpeg)"
      if [[ "$ffmpeg_path" == /usr/bin/* ]]; then
        echo "  → Dùng container ams-backend"
        return 0
      fi
      echo "  ! Port 8000 không phải Docker backend — dừng uvicorn local"
      stop_host_uvicorn
    fi
  fi

  local existing
  existing="$(port_pids 8000)"
  if [[ -n "$existing" ]]; then
    if wait_for_http "http://127.0.0.1:8000/api/health" "Backend (port 8000)" 5; then
      echo "  → Backend đã chạy sẵn trên port 8000"
      return 0
    fi
    stop_host_uvicorn
  fi

  if [[ ! -x "$backend_dir/.venv/bin/uvicorn" ]]; then
    echo "ERROR: Thiếu backend/.venv — chạy: cd backend && python3 -m venv .venv && pip install -r requirements.txt"
    echo "       Hoặc chỉ dùng Docker: npm run dev:up"
    exit 1
  fi

  echo "==> Backend local (http://127.0.0.1:8000)"
  : >"$backend_log"
  (
    cd "$backend_dir"
    export DYLD_LIBRARY_PATH="${DYLD_LIBRARY_PATH:-}"
    exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ) >>"$backend_log" 2>&1 &

  echo $! >"$backend_pid"

  if ! wait_for_http "http://127.0.0.1:8000/api/health" "Backend" 45; then
    echo "--- backend.log (20 dòng cuối) ---"
    tail -20 "$backend_log" || true
    exit 1
  fi
}

start_frontend() {
  local root="$1"
  local dev_dir="$2"
  local frontend_pid="$dev_dir/frontend.pid"
  local frontend_log="$dev_dir/frontend.log"

  local existing
  existing="$(port_pids 5173)"
  if [[ -n "$existing" ]]; then
    if wait_for_http "http://127.0.0.1:5173/" "Frontend (port 5173)" 5; then
      echo "  → Frontend đã chạy sẵn (http://localhost:5173)"
      return 0
    fi
    echo "  ! Port 5173 bị chiếm nhưng không phản hồi — dừng process cũ"
    kill $existing 2>/dev/null || true
    sleep 1
  fi

  echo "==> Frontend (http://localhost:5173)"
  : >"$frontend_log"
  (
    cd "$root"
    exec npm run dev -- --host 0.0.0.0 --port 5173
  ) >>"$frontend_log" 2>&1 &

  echo $! >"$frontend_pid"

  if ! wait_for_http "http://127.0.0.1:5173/" "Frontend" 30; then
    echo "--- frontend.log (20 dòng cuối) ---"
    tail -20 "$frontend_log" || true
    exit 1
  fi
}

print_dev_ready() {
  cat <<'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AMS đã sẵn sàng

  Giao diện web:  http://localhost:5173
  API health:     http://127.0.0.1:8000/api/health

  Login: admin@ams.local / admin123

  Khởi động lại:  npm run dev:up
  Dừng web local: npm run dev:stop
  Log frontend:   tail -f .dev/frontend.log
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
}

open_browser() {
  if [[ "$(uname -s)" == "Darwin" ]] && command -v open >/dev/null 2>&1; then
    open "http://localhost:5173/" >/dev/null 2>&1 || true
  fi
}
