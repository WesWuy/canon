"""Build the Canon SQLite database (FTS5) from normalized Verse records.

Layout is tuned for sql.js-httpvfs consumption in the browser:
  - page_size 4096 to match the default HTTP request chunk size
  - verses: one row per verse, rowid referenced by the FTS index
  - verses_fts: contentless-delete=0 external-content FTS5 index over text
  - books / book_traditions: filter metadata for the UI
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from common import BUILD_DIR, Verse

SCHEMA = """
PRAGMA page_size = 4096;
PRAGMA journal_mode = DELETE;

CREATE TABLE books (
    book_id     TEXT PRIMARY KEY,
    book_title  TEXT NOT NULL,
    collection  TEXT NOT NULL,
    translation TEXT NOT NULL,
    source_url  TEXT NOT NULL,
    license     TEXT NOT NULL,
    aliases     TEXT NOT NULL DEFAULT '[]',   -- JSON array for reference lookup
    sort_order  INTEGER NOT NULL
);

CREATE TABLE book_traditions (
    book_id   TEXT NOT NULL REFERENCES books(book_id),
    tradition TEXT NOT NULL,
    PRIMARY KEY (book_id, tradition)
);

CREATE TABLE verses (
    id                INTEGER PRIMARY KEY,
    book_id           TEXT NOT NULL REFERENCES books(book_id),
    chapter           INTEGER NOT NULL,
    verse             INTEGER NOT NULL,
    text              TEXT NOT NULL,
    alt_versification TEXT NOT NULL DEFAULT '{}'
);
CREATE UNIQUE INDEX idx_verses_ref ON verses(book_id, chapter, verse);

CREATE VIRTUAL TABLE verses_fts USING fts5(
    text,
    content='verses',
    content_rowid='id',
    tokenize='porter unicode61'
);
"""


def build_db(
    verses: list[Verse],
    books_meta: list[dict],
    out_path: Path | None = None,
) -> Path:
    out_path = out_path or BUILD_DIR / "canon.db"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    con = sqlite3.connect(out_path)
    con.executescript(SCHEMA)

    for meta in books_meta:
        con.execute(
            "INSERT INTO books VALUES (?,?,?,?,?,?,?,?)",
            (
                meta["book_id"], meta["book_title"], meta["collection"],
                meta["translation"], meta["source_url"], meta["license"],
                json.dumps(meta.get("aliases", [])), meta["sort_order"],
            ),
        )
        for t in meta["traditions"]:
            con.execute("INSERT INTO book_traditions VALUES (?,?)",
                        (meta["book_id"], t))

    order = {m["book_id"]: m["sort_order"] for m in books_meta}
    verses_sorted = sorted(verses, key=lambda v: (order[v.book_id], v.chapter, v.verse))
    for i, v in enumerate(verses_sorted, start=1):
        con.execute(
            "INSERT INTO verses VALUES (?,?,?,?,?,?)",
            (i, v.book_id, v.chapter, v.verse, v.text,
             json.dumps(v.alt_versification, ensure_ascii=False)),
        )
    con.execute("INSERT INTO verses_fts(rowid, text) SELECT id, text FROM verses")
    con.execute("INSERT INTO verses_fts(verses_fts) VALUES ('optimize')")
    con.commit()
    con.execute("VACUUM")
    con.close()
    return out_path
