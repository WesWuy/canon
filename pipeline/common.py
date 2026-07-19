"""Shared helpers for the Canon corpus pipeline."""
from __future__ import annotations

import dataclasses
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
BUILD_DIR = ROOT / "data" / "build"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


@dataclasses.dataclass
class Verse:
    """One verse in the normalized corpus schema."""

    tradition: list[str]
    collection: str
    book_id: str
    book_title: str
    translation: str
    chapter: int
    verse: int
    text: str
    alt_versification: dict[str, str] = dataclasses.field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), ensure_ascii=False)


def fetch(url: str, cache_path: Path, delay: float = 0.5) -> bytes:
    """Download url to cache_path unless already cached; return the bytes."""
    if cache_path.exists() and cache_path.stat().st_size > 0:
        return cache_path.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(data)
    time.sleep(delay)  # be polite to the source host on cold fetches
    return data


def write_jsonl(verses: list[Verse], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for v in verses:
            f.write(v.to_json() + "\n")
