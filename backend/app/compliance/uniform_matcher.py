from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class UniformMatchResult:
    score: float
    matched: bool


def match_uniform(
    person_image: bytes | None,
    template_images: list[str],
    *,
    track_id: int | None = None,
    template_id: str | None = None,
    threshold: float = 0.85,
) -> UniformMatchResult:
    """
    Mock uniform matcher — v1.7 Phase 3.

    Future versions may replace with CLIP / OpenCLIP / embedding search.
    """
    seed = f"{track_id}:{template_id}:{len(template_images)}:{len(person_image or b'')}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 25
    score = round(0.75 + (bucket / 100), 2)
    score = min(max(score, 0.75), 0.99)
    matched = score >= threshold
    return UniformMatchResult(score=score, matched=matched)
