"""Fetch and parse Jubilees (R.H. Charles translation) from sacred-texts.com.

Source: https://sacred-texts.com/bib/jub/ — "The Book of Jubilees", R.H.
Charles (Oxford, 1902; the same translation reprinted in his 1913 APOT
vol. 2 and the 1917 SPCK edition). Public domain (pre-1930 publication).

Page format: thematic sections (jub12.htm .. jub87.htm, covering chapters
i-l consecutively), each announcing its verse range in a "(xvii. 15-18:
cf. ...)" line, usually inside the page's own <h3> heading. Verses appear
inline as "N. text" runs, as in the Book of Enoch pages. Quirks handled:
  - the verse-range numbers are occasionally given in lowercase roman
    instead of arabic (e.g. "(xx. i-ii)" on jub44.htm) -> _RANGE_RE accepts
    either and converts
  - EVERY chapter-opening page except the very first (jub12, chapter i)
    marks verse 1 with the chapter's own UPPERCASE roman numeral instead
    of "1." (e.g. chapter ii opens "II. And the angel..."), apparently a
    typographic convention carried over from the original edition ->
    detected and stripped before the normal arabic-marker split runs
  - Anno Mundi margin dates in right-aligned <table> elements -> stripped
  - superscript footnote links and a "Footnotes" tail section -> stripped
  - the unversified front matter and Prologue pages are skipped by only
    walking jub12.htm..jub87.htm (the versified chapters i-l)
"""
from __future__ import annotations

import html as _html
import re

from common import RAW_DIR, Verse, fetch
from parse_enoch import _SIGLA_RE, _TAG_RE, _WS_RE, _VERSE_MARK_RE, roman_to_int

BASE = "https://sacred-texts.com/bib/jub/"
CACHE = RAW_DIR / "sacred-texts" / "jub"

FIRST_PAGE, LAST_PAGE = "jub12.htm", "jub87.htm"

_ROMAN_TOKEN = r"[ivxlc]+"
_RANGE_RE = re.compile(
    rf"\(({_ROMAN_TOKEN})\.\s*(\d+|{_ROMAN_TOKEN})(?:[-–](\d+|{_ROMAN_TOKEN}))?",
    re.IGNORECASE,
)
_ROMAN_INTS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def _num(token: str) -> int:
    """A range endpoint that's either arabic digits or lowercase roman."""
    return int(token) if token.isdigit() else roman_to_int(token.upper())


def _int_to_roman(n: int) -> str:
    table = [(50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"),
             (4, "IV"), (1, "I")]
    out = []
    for value, sym in table:
        count, n = divmod(n, value)
        out.append(sym * count)
    return "".join(out)


def _content_pages() -> list[str]:
    index_html = fetch(BASE + "index.htm", CACHE / "index.htm").decode("utf-8", "replace")
    pages: list[str] = []
    for fname in re.findall(r'<A HREF="(jub\d+\.htm)"', index_html, re.IGNORECASE):
        if fname not in pages:
            pages.append(fname)
    return pages[pages.index(FIRST_PAGE): pages.index(LAST_PAGE) + 1]


def _extract_title(page_html: str) -> str:
    m = re.search(r"<h3[^>]*>(.*?)</h3>", page_html, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    title = _TAG_RE.sub(" ", m.group(1))
    return _WS_RE.sub(" ", _html.unescape(_html.unescape(title))).strip()


def _extract_body(page_html: str) -> str:
    m = re.search(r"<h3[^>]*>.*?</h3>(.*?)<div class=\"filenav\">",
                  page_html, re.DOTALL | re.IGNORECASE)
    if not m:
        m = re.search(r"<h3[^>]*>.*?</h3>(.*)", page_html, re.DOTALL | re.IGNORECASE)
    body = m.group(1) if m else ""
    body = re.split(r"<h3[^>]*>\s*Footnotes", body, flags=re.IGNORECASE)[0]
    body = re.sub(r"<table.*?</table>", " ", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<a\s+(?:name|href)=\"[^\"]*(?:fn|fr)[^\"]*\"[^>]*>.*?</a>", " ",
                  body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<a name=\"page_\d+\"[^>]*>.*?</a>", " ", body,
                  flags=re.DOTALL | re.IGNORECASE)
    text = _TAG_RE.sub(" ", body)
    text = _html.unescape(_html.unescape(text))
    text = _SIGLA_RE.sub("", text)
    return _WS_RE.sub(" ", text).strip()


def _split_from(text: str, start: int) -> list[tuple[int, str]]:
    """Split on 'N.' markers ascending from `start` (missing numbers folded
    into the previous verse, as in the Enoch parser)."""
    marks: list[tuple[int, re.Match]] = []
    last = start - 1
    for m in _VERSE_MARK_RE.finditer(text):
        n = int(m.group(1))
        if last < n <= last + 3:
            marks.append((n, m))
            last = n
    out: list[tuple[int, str]] = []
    for i, (n, m) in enumerate(marks):
        end = marks[i + 1][1].start() if i + 1 < len(marks) else len(text)
        seg = text[m.end(): end].strip()
        if seg:
            out.append((n, seg))
    return out


def _split_chapter(body: str, chapter: int, start: int) -> list[tuple[int, str]]:
    """Split a chapter-opening page's body, handling the roman-numeral
    verse-1 marker (every chapter opening except chapter i)."""
    if start == 1 and chapter > 1:
        roman = _int_to_roman(chapter)
        m = re.search(rf"(?<!\S){re.escape(roman)}\.\s+", body)
        if m and m.start() < 60:
            rest = body[m.end():]
            first_mark = next(
                (mm for mm in _VERSE_MARK_RE.finditer(rest)
                 if 2 <= int(mm.group(1)) <= 4), None)
            v1_end = first_mark.start() if first_mark else len(rest)
            out = [(1, rest[:v1_end].strip())]
            out += _split_from(rest, 2)
            return [v for v in out if v[1]]
    return _split_from(body, start)


def parse_jubilees() -> list[Verse]:
    by_ref: dict[tuple[int, int], str] = {}
    chapter, next_verse = 1, 1
    for fname in _content_pages():
        page = fetch(BASE + fname, CACHE / fname).decode("utf-8", "replace")
        title = _extract_title(page)
        body = _extract_body(page)
        rng = _RANGE_RE.search(title)
        claimed = (
            (roman_to_int(rng.group(1).upper()), _num(rng.group(2))) if rng else None
        )
        if claimed in ((chapter, next_verse), (chapter + 1, 1)):
            chapter, start = claimed
        else:
            # no usable range in the title: infer from the first verse
            # marker actually present (roman-numeral verse-1 markers are
            # not arabic digits, so a chapter-opening page like this shows
            # its first *arabic* marker as "2")
            first = _VERSE_MARK_RE.search(body)
            first_n = int(first.group(1)) if first else 1
            if first_n == next_verse:
                start = next_verse
            elif first_n in (1, 2):
                chapter, start = chapter + 1, 1
            else:
                raise ValueError(
                    f"{fname}: cannot place page (claimed {claimed}, "
                    f"expected {chapter}:{next_verse}, first marker {first_n})")
        for vnum, vtext in _split_chapter(body, chapter, start):
            ref = (chapter, vnum)
            if ref in by_ref:
                print(f"  warning: duplicate Jubilees {chapter}:{vnum} on {fname}")
                continue
            by_ref[ref] = vtext
            next_verse = vnum + 1
    return [
        Verse(
            tradition=["ethiopian", "pseudepigrapha"],
            collection="ot_pseudepigrapha",
            book_id="JUB",
            book_title="Jubilees",
            translation="R.H. Charles (1902)",
            chapter=ch,
            verse=v,
            text=text,
        )
        for (ch, v), text in sorted(by_ref.items())
    ]


if __name__ == "__main__":
    vs = parse_jubilees()
    chapters = {v.chapter for v in vs}
    missing = sorted(set(range(1, 51)) - chapters)
    print(f"Jubilees: {len(vs)} verses across {len(chapters)} chapters"
          f" (missing: {missing or 'none'})")
