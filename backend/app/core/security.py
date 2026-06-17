import base64
import hashlib
import hmac
import json
import time
import uuid
from typing import Any, Optional

from app.core.config import get_settings


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    salt = uuid.uuid4().hex
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        algorithm, salt, digest = hashed_password.split("$", 2)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return hmac.compare_digest(candidate.hex(), digest)


def create_access_token(subject: str, role: str) -> tuple[str, int, str]:
    settings = get_settings()
    now = int(time.time())
    exp = now + settings.access_token_expire_minutes * 60
    jti = uuid.uuid4().hex
    header = {"alg": settings.jwt_algorithm, "typ": "JWT"}
    payload = {"sub": subject, "role": role, "iat": now, "exp": exp, "jti": jti}

    signing_input = (
        f"{_b64encode(json.dumps(header, separators=(',', ':')).encode())}."
        f"{_b64encode(json.dumps(payload, separators=(',', ':')).encode())}"
    )
    signature = hmac.new(
        settings.jwt_secret_key.encode(),
        signing_input.encode(),
        hashlib.sha256,
    ).digest()
    return f"{signing_input}.{_b64encode(signature)}", exp, jti


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    settings = get_settings()
    try:
        header_part, payload_part, signature_part = token.split(".")
    except ValueError:
        return None

    signing_input = f"{header_part}.{payload_part}"
    expected_signature = hmac.new(
        settings.jwt_secret_key.encode(),
        signing_input.encode(),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_b64encode(expected_signature), signature_part):
        return None

    try:
        payload = json.loads(_b64decode(payload_part))
    except (json.JSONDecodeError, ValueError):
        return None

    if int(payload.get("exp", 0)) < int(time.time()):
        return None

    return payload
