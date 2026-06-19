from pathlib import Path
import re

API_DIR = Path("backend/app/api")

SKIP = {
    "auth.py",
    "health.py",
    "__init__.py",
    "deps.py",
}

for file in API_DIR.glob("*.py"):
    if file.name in SKIP:
        continue

    text = file.read_text(encoding="utf-8")

    # đã khóa rồi thì bỏ qua
    if "Depends(get_current_user)" in text:
        print(f"SKIP {file.name}")
        continue

    changed = False

    # thêm import
    if "from app.api.deps import get_current_user" not in text:
        text = (
            "from app.api.deps import get_current_user\n"
            + text
        )
        changed = True

    # APIRouter nhiều dòng
    pattern_multiline = r"router\s*=\s*APIRouter\((.*?)\)"
    m = re.search(pattern_multiline, text, re.S)

    if m and "dependencies=" not in m.group(1):
        router_block = m.group(0)

        new_block = router_block[:-1] + (
            ",\n    dependencies=[Depends(get_current_user)]\n)"
        )

        text = text.replace(router_block, new_block, 1)
        changed = True

    if changed:
        file.write_text(text, encoding="utf-8")
        print(f"UPDATED {file.name}")
    else:
        print(f"NOCHANGE {file.name}")

print("DONE")
