# Canon

Full-text search across biblical and parabiblical literature — Protestant
canon, Catholic deuterocanon, Orthodox additions, Ethiopian broader canon,
OT pseudepigrapha, and NT apocrypha — using only public domain English
translations. No backend: the SQLite database is served statically and
queried in the browser via HTTP range requests.

**Corpus**: all 81 World English Bible books (Protestant OT/NT + full Deuterocanon/Apocrypha) plus 1 Enoch (R.H. Charles 1917) — 82 books, ~39,000 verses.
See [CORPUS.md](CORPUS.md) for sources and licensing.

## Architecture

```
pipeline/          Python: fetch -> parse -> normalize -> SQLite FTS5
  run.py           entry point + book registry
  common.py        Verse schema, cached fetching
  parse_usfm.py    USFM parser (ebible.org downloads)
  parse_enoch.py   1 Enoch parser (sacred-texts.com, Charles 1917)
  build_db.py      SQLite schema + FTS5 index build
data/raw/          cached source downloads (gitignored)
data/build/        corpus.jsonl + canon.db (gitignored)
app/               Vite + React + TS + Tailwind search UI
  public/canon.db.000  the database (single chunk), fetched via HTTP ranges
```

Every verse is normalized to one schema:

```json
{ "tradition": ["ethiopian", "pseudepigrapha"], "collection": "ot_pseudepigrapha",
  "book_id": "1EN", "book_title": "1 Enoch", "translation": "R.H. Charles (1917)",
  "chapter": 14, "verse": 8, "text": "...", "alt_versification": {} }
```

## Commands

```sh
# rebuild the corpus database (first run downloads sources into data/raw)
python pipeline/run.py
cp data/build/canon.db app/public/canon.db.000

# app
cd app
npm install
npm run dev      # dev server
npx tsc -b       # typecheck
npm run build    # production build (deployable to GitHub Pages as-is)
```

## How browser search works

`canon.db` is built with `page_size=4096` and an FTS5 index
(`porter unicode61` tokenizer). The app loads it with
[sql.js-httpvfs](https://github.com/phiresky/sql.js-httpvfs), which runs
SQLite compiled to WASM in a web worker and fetches only the database pages
a query touches via HTTP range requests — a keyword search transfers a few
hundred KB at most, regardless of corpus size.

## v1 scope

In: keyword search with FTS ranking, tradition + book filters, verse results
with context expansion, direct reference lookup ("1 Enoch 14:8").
Out: user accounts, notes, cross-reference graphs, original languages,
non-English translations.
