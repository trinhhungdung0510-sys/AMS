# AMS — Environment Recovery (macOS / Homebrew Python)

**Date:** 2026-06-28  
**Machine:** macOS 26.2 (arm64), Homebrew 6.0.5, Docker Desktop OK  
**Scope:** Local dev environment only — **no AMS application code changes required**

---

## Symptoms

| Check | Status |
|-------|--------|
| Backend tests (`pytest`) | 82/82 pass |
| Frontend tests (`vitest`) | 51/51 pass |
| `python -m venv .venv` | **Fails** at `ensurepip` |
| `uvicorn app.main:app` | **Cannot start** (broken/missing venv) |
| Old `backend/.venv` | Python **3.9** (too old for AMS; needs **3.11+**) |

### Error observed

```
ImportError: dlopen(.../pyexpat.cpython-312-darwin.so, 0x0002):
Symbol not found: _XML_SetAllocTrackerActivationThreshold
  Referenced from: .../pyexpat.cpython-312-darwin.so
  Expected in:     /usr/lib/libexpat.1.dylib
```

Same failure affects **Homebrew `python@3.12` and `python@3.14`**.

---

## Root cause

This is **not an AMS bug**. It is a **dynamic library mismatch** on macOS 26 between:

1. **Homebrew Python bottles** — the built-in `pyexpat` extension was compiled against **Expat 2.8.x**, which exports new symbols such as `_XML_SetAllocTrackerActivationThreshold`.
2. **macOS system `libexpat`** at `/usr/lib/libexpat.1.dylib` — still an **older Expat** on macOS 26.2 and does **not** export those symbols.

Evidence from this machine:

```bash
# pyexpat is linked to the system library
otool -L "$(python3.12 -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR"))')/lib-dynload/pyexpat.cpython-312-darwin.so"
# → /usr/lib/libexpat.1.dylib

# Homebrew expat 2.8.2 DOES have the symbol
nm -gU /opt/homebrew/opt/expat/lib/libexpat.1.dylib | grep XML_SetAllocTrackerActivationThreshold
# → _XML_SetAllocTrackerActivationThreshold

# System path used at runtime does NOT
python3.12 -c "from pyexpat import *"
# → ImportError (symbol not found)
```

### Why `ensurepip` fails

`python -m venv` bootstraps pip via `ensurepip`. That path imports `pip` → `pip._internal` → `xmlrpc.client` → `pyexpat`. Because `pyexpat` cannot load, **venv creation fails before pip exists**.

### Why reinstalling the bottle alone does not fix it

```bash
brew reinstall expat
brew reinstall python@3.12
```

was tested on this machine — **still broken**. Homebrew’s bottled Python on macOS 26 continues to load `/usr/lib/libexpat.1.dylib` at runtime.

### Why `--build-from-source` failed here

```bash
brew reinstall python@3.12 --build-from-source
```

failed during install with:

```
install: Modules/pyexpat.cpython-312-darwin.so: No such file or directory
```

Homebrew documents source builds as unsupported; treat this as **non-reliable** on macOS 26 until Homebrew ships a fixed bottle.

---

## Minimum repair (recommended for this machine)

Use Homebrew’s **Expat 2.8.2** at runtime instead of the system library. This is the smallest change that restores `venv`, `pip`, and `uvicorn`.

### Step 0 — Ensure Homebrew Python 3.12 is linked

```bash
brew install python@3.12 expat
brew link python@3.12
/opt/homebrew/bin/python3.12 --version   # expect Python 3.12.13
```

### Step 1 — Export Expat library path (current shell)

```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
```

Verify:

```bash
python3.12 -c "from pyexpat import *; print('pyexpat OK')"
python3.12 -m pip --version
```

### Step 2 — Make the fix persistent (zsh)

Add to `~/.zshrc`:

```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
```

Then:

```bash
source ~/.zshrc
```

> **Note:** macOS may restrict `DYLD_*` for some hardened/signed apps. Homebrew `python3.12` in a normal Terminal session works with this setting (verified).

### Step 3 — Recreate the AMS backend virtualenv

```bash
cd ~/Documents/AMS/backend
rm -rf .venv

python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Verify:

```bash
python -c "import app.main; print('app.main OK')"
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

In another terminal:

```bash
curl http://127.0.0.1:8000/api/health
```

### Step 4 — Infrastructure (unchanged)

```bash
cd ~/Documents/AMS/backend
docker compose up -d    # Postgres + Redis
```

---

## Verification checklist

Run after repair (with `DYLD_LIBRARY_PATH` set):

| # | Command | Expected |
|---|---------|----------|
| 1 | `python3.12 -c "from pyexpat import *"` | `no error` |
| 2 | `python3.12 -m venv /tmp/venv-test` | creates venv |
| 3 | `/tmp/venv-test/bin/pip --version` | pip version printed |
| 4 | `/tmp/venv-test/bin/pip install uvicorn` | installs OK |
| 5 | `cd backend && source .venv/bin/activate && uvicorn app.main:app --port 8000` | `Application startup complete` |

**Verified on this machine (2026-06-28):** items 1–4 pass with `DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib`.

---

## Alternative permanent fixes (pick one)

Use these if you prefer **not** to rely on `DYLD_LIBRARY_PATH`.

### Option A — Repoint `pyexpat` to Homebrew Expat (one-time, local)

Patches the Homebrew Python module to load Homebrew’s Expat instead of `/usr/lib/libexpat.1.dylib`:

```bash
PYEXPAT="$(python3.12 -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR"))')/lib-dynload/pyexpat.cpython-312-darwin.so"

install_name_tool \
  -change /usr/lib/libexpat.1.dylib \
  /opt/homebrew/opt/expat/lib/libexpat.1.dylib \
  "$PYEXPAT"

python3.12 -c "from pyexpat import *; print('pyexpat OK')"
```

Repeat after every `brew reinstall python@3.12`.

### Option B — Official Python.org installer

Download **Python 3.12 macOS installer** from https://www.python.org/downloads/  
It bundles its own dependencies and avoids the system `libexpat` mismatch.

Then:

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m venv ~/Documents/AMS/backend/.venv
```

### Option C — Wait for Homebrew bottle update

Track Homebrew issues for **macOS 26 (Tahoe) + python@3.12 + expat**. When a fixed bottle is published:

```bash
brew update
brew upgrade expat python@3.12
python3.12 -c "from pyexpat import *"
```

Remove `DYLD_LIBRARY_PATH` from `~/.zshrc` once this passes without it.

---

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Old `backend/.venv` (Python 3.9) | Delete and recreate with 3.12+ |
| `python3.12 not found` after failed brew build | `brew install python@3.12 && brew link python@3.12` |
| Wrong Python on PATH | Prefer `/opt/homebrew/bin/python3.12` when creating venv |
| Using Python 3.14 as default | Same `pyexpat` issue on this machine — use **3.12** for AMS |
| Tests pass but server won’t start | Tests may use a different interpreter/venv than your shell |

---

## Summary

| Layer | Finding |
|-------|---------|
| AMS code | OK (tests green) |
| Docker | OK |
| Homebrew Python | **Broken `pyexpat` → `ensurepip` → `venv`** |
| Cause | Python bottle expects Expat 2.8 symbols; macOS 26 system `libexpat` is older |
| Minimum fix | Point runtime to `/opt/homebrew/opt/expat/lib` via `DYLD_LIBRARY_PATH`, then recreate `.venv` |
| Long-term fix | Repoint `pyexpat`, use python.org build, or upgrade when Homebrew fixes macOS 26 bottles |

---

## Quick copy-paste recovery

**Khuyến nghị hàng ngày (một lệnh, tránh quên chạy backend/frontend):**

```bash
cd ~/Documents/AMS
npm run dev:local    # Docker + backend + frontend + mở trình duyệt
# Dừng: npm run dev:stop
```

**Khôi phục môi trường Python lần đầu:**

```bash
# 1) Fix Expat loading for this shell + future shells
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
grep -q 'opt/expat/lib' ~/.zshrc || echo 'export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"' >> ~/.zshrc

# 2) Ensure Python 3.12
brew install python@3.12 expat
brew link python@3.12

# 3) Recreate AMS backend venv
cd ~/Documents/AMS/backend
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4) Start stack
docker compose up -d
npm run dev:local
```
