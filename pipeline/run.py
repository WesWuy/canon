"""Canon pipeline entry point: fetch -> parse -> normalize -> build SQLite.

v1 test corpus: Jude (WEB, ebible.org) + 1 Enoch (Charles 1917, sacred-texts).
Add new books by extending BOOKS and wiring a parser in main().
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import BUILD_DIR, RAW_DIR, write_jsonl
from build_db import build_db
from parse_enoch import parse_enoch
from parse_usfm import parse_usfm

BOOKS = [
    {
        "book_id": "JUD",
        "book_title": "Jude",
        "collection": "nt",
        "translation": "World English Bible (WEB)",
        "traditions": ["protestant", "catholic", "orthodox", "ethiopian"],
        "source_url": "https://ebible.org/Scriptures/eng-web_usfm.zip",
        "license": "Public domain (WEB is dedicated to the public domain)",
        "aliases": ["jude", "jud"],
        "sort_order": 100,
    },
    {
        "book_id": "1EN",
        "book_title": "1 Enoch",
        "collection": "ot_pseudepigrapha",
        "translation": "R.H. Charles (1917)",
        "traditions": ["ethiopian", "pseudepigrapha"],
        "source_url": "https://sacred-texts.com/bib/boe/",
        "license": "Public domain (published 1917; Charles' translation, "
                   "revised from Charles 1913 APOT vol. 2)",
        "aliases": ["1 enoch", "1enoch", "1en", "enoch", "ethiopic enoch"],
        "sort_order": 200,
    },
]


def main() -> None:
    jude_usfm = (RAW_DIR / "ebible" / "eng-web_usfm" / "95-JUDeng-web.usfm")
    jude_meta = next(b for b in BOOKS if b["book_id"] == "JUD")
    jude = parse_usfm(
        jude_usfm,
        tradition=jude_meta["traditions"],
        collection=jude_meta["collection"],
        book_id="JUD",
        book_title="Jude",
        translation=jude_meta["translation"],
    )
    print(f"Jude: {len(jude)} verses")

    enoch = parse_enoch()
    chapters = {v.chapter for v in enoch}
    print(f"1 Enoch: {len(enoch)} verses across {len(chapters)} chapters")

    all_verses = jude + enoch
    write_jsonl(all_verses, BUILD_DIR / "corpus.jsonl")
    db_path = build_db(all_verses, BOOKS)
    print(f"Built {db_path} ({db_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
