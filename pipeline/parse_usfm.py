"""Parse USFM files (ebible.org downloads) into normalized Verse records.

Handles the WEB-style USFM found in eng-web_usfm.zip:
  \\c N            chapter marker
  \\v N text       verse marker (verse text may span multiple lines/paragraphs)
  \\w word|attrs\\w*  word-level markup (Strong's numbers) -> keep the word
  \\f ... \\f*      footnotes -> dropped
  \\x ... \\x*      cross-references -> dropped
  paragraph/poetry markers (\\p, \\q1, \\m, ...) -> treated as soft breaks
"""
from __future__ import annotations

import re
from pathlib import Path

from common import Verse

_FOOTNOTE_RE = re.compile(r"\\f\s.*?\\f\*", re.DOTALL)
_XREF_RE = re.compile(r"\\x\s.*?\\x\*", re.DOTALL)
_WORD_RE = re.compile(r"\\\+?w\s([^|\\]*)(?:\|[^\\]*)?\\\+?w\*")
_CHAR_PAIRED_RE = re.compile(r"\\\+?(wj|add|nd|qt|sls|tl|em|bd|it|bdit|sc)\s(.*?)\\\+?\1\*", re.DOTALL)
_LEFTOVER_MARKER_RE = re.compile(r"\\[a-z0-9]+\*?")
_WS_RE = re.compile(r"\s+")


def _clean(text: str) -> str:
    text = _FOOTNOTE_RE.sub("", text)
    text = _XREF_RE.sub("", text)
    text = _WORD_RE.sub(r"\1", text)
    # paired character markers can nest once (\+w inside \add); run twice
    for _ in range(2):
        text = _CHAR_PAIRED_RE.sub(r"\2", text)
    text = _LEFTOVER_MARKER_RE.sub(" ", text)
    return _WS_RE.sub(" ", text).strip()


def parse_usfm(
    path: Path,
    *,
    tradition: list[str],
    collection: str,
    book_id: str,
    book_title: str,
    translation: str,
) -> list[Verse]:
    raw = path.read_text(encoding="utf-8-sig")
    verses: list[Verse] = []
    chapter = 0
    cur_verse: int | None = None
    cur_text: list[str] = []

    def flush() -> None:
        nonlocal cur_verse, cur_text
        if cur_verse is not None:
            text = _clean(" ".join(cur_text))
            if text:
                verses.append(
                    Verse(
                        tradition=tradition,
                        collection=collection,
                        book_id=book_id,
                        book_title=book_title,
                        translation=translation,
                        chapter=chapter,
                        verse=cur_verse,
                        text=text,
                    )
                )
        cur_verse, cur_text = None, []

    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("\\"):
            if cur_verse is not None and line:
                cur_text.append(line)
            continue
        marker = line.split(None, 1)[0]
        rest = line[len(marker):].strip()
        if marker == "\\c":
            flush()
            chapter = int(rest.split()[0])
        elif marker == "\\v":
            flush()
            m = re.match(r"(\d+)(?:-(\d+))?\s*(.*)", rest, re.DOTALL)
            if not m:
                continue
            cur_verse = int(m.group(1))  # verse ranges collapse to first number
            cur_text = [m.group(3)]
        elif marker in ("\\id", "\\ide", "\\h", "\\toc1", "\\toc2", "\\toc3",
                        "\\mt1", "\\mt2", "\\mt3", "\\s1", "\\s2", "\\r", "\\d",
                        "\\rem", "\\sts", "\\cl", "\\cp"):
            continue  # headings/metadata: never verse text
        else:
            # paragraph-level marker (\p, \q1, \m, \pi, \b ...): keep trailing text
            if cur_verse is not None and rest:
                cur_text.append(rest)

    flush()
    return verses
