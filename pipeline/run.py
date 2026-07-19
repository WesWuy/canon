"""Canon pipeline entry point: fetch -> parse -> normalize -> build SQLite.

Corpus: all 81 WEB books (OT + Deuterocanon/Apocrypha + NT, ebible.org)
plus 1 Enoch (Charles 1917, sacred-texts.com).
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from books import ESG_ALT_VERSIFICATION, registry
from build_db import build_db
from common import BUILD_DIR, RAW_DIR, write_jsonl
from parse_enoch import parse_enoch
from parse_usfm import parse_usfm

USFM_DIR = RAW_DIR / "ebible" / "eng-web_usfm"


def usfm_path(prefix: str) -> Path:
    matches = glob.glob(str(USFM_DIR / f"{prefix}*.usfm"))
    if len(matches) != 1:
        raise FileNotFoundError(f"expected exactly one {prefix}*.usfm, got {matches}")
    return Path(matches[0])


def main() -> None:
    books = registry()
    all_verses = []
    for meta in books:
        if meta["book_id"] == "1EN":
            verses = parse_enoch()
        else:
            verses = parse_usfm(
                usfm_path(meta["usfm_prefix"]),
                tradition=meta["traditions"],
                collection=meta["collection"],
                book_id=meta["book_id"],
                book_title=meta["book_title"],
                translation=meta["translation"],
            )
        if meta["book_id"] == "ESG":
            for v in verses:
                alt = ESG_ALT_VERSIFICATION.get((v.chapter, v.verse))
                if alt:
                    v.alt_versification = alt
        if not verses:
            raise RuntimeError(f"no verses parsed for {meta['book_id']}")
        all_verses.extend(verses)

    print(f"{len(books)} books, {len(all_verses)} verses")
    write_jsonl(all_verses, BUILD_DIR / "corpus.jsonl")
    db_path = build_db(all_verses, books)
    print(f"Built {db_path} ({db_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
