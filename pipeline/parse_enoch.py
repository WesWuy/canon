"""Fetch and parse 1 Enoch (R.H. Charles translation) from sacred-texts.com.

Source: https://sacred-texts.com/bib/boe/ — "The Book of Enoch", R.H. Charles,
SPCK 1917 (Charles' own translation, revised from his 1913 Pseudepigrapha
volume). Public domain (pre-1930 publication).

Page format: roughly one chapter per page (boe004.htm .. boe112.htm).
Verses appear inline as "N. text" runs inside <p> blocks. Complications:
  - the site index mislabels some chapters, so the chapter number is read
    from each page's own <h3>CHAPTER <roman>.</h3> heading
  - chapter 91 is split across two pages (Charles prints the Apocalypse of
    Weeks in his reconstructed order: 91:1-11,18-19 ... 93 ... 91:12-17)
  - page-number paragraphs ("p. 41") interleaved with text
  - Charles' critical sigla (corner brackets, daggers; sometimes
    double-escaped as &amp;#8224;) -> stripped
  - footnote markers as superscript anchor links -> stripped
  - occasional missing verse numbers in the source (that text folds into
    the previous verse, e.g. 14:10)
"""
from __future__ import annotations

import html
import re

from common import RAW_DIR, Verse, fetch

BASE = "https://sacred-texts.com/bib/boe/"
CACHE = RAW_DIR / "sacred-texts" / "boe"

_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

# Typos in the source pages' own <h3> headings, verified against content:
# boe081.htm says "CHAPTER LXXVII" but contains 78:1ff ("names of the sun")
_HEADING_CORRECTIONS = {"boe081.htm": 78}

# Charles' critical sigla and footnote daggers
_SIGLA_RE = re.compile(r"[⌈⌉⌊⌋†‡]")
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def roman_to_int(s: str) -> int:
    total = 0
    for i, ch in enumerate(s):
        val = _ROMAN[ch]
        if i + 1 < len(s) and _ROMAN[s[i + 1]] > val:
            total -= val
        else:
            total += val
    return total


def _page_files() -> list[str]:
    """All boeNNN.htm pages linked from the index, in reading order."""
    index_html = fetch(BASE + "index.htm", CACHE / "index.htm").decode("utf-8", "replace")
    seen: list[str] = []
    for fname in re.findall(r'<A HREF="(boe\d+\.htm)"', index_html, re.IGNORECASE):
        if fname not in seen:
            seen.append(fname)
    return seen


def _page_chapter(page_html: str) -> int | None:
    """Chapter number from the page's own heading; None for front matter."""
    m = re.search(r"<h3[^>]*>\s*CHAPTER\s+([IVXLCDM]+)\.?\s*</h3>",
                  page_html, re.IGNORECASE)
    return roman_to_int(m.group(1).upper()) if m else None


def _extract_body(page_html: str) -> str:
    """Return the chapter's text content with tags stripped."""
    m = re.search(r"<h3[^>]*>.*?</h3>(.*?)<p>\s*<div class=\"filenav\">",
                  page_html, re.DOTALL | re.IGNORECASE)
    if not m:
        m = re.search(r"<h3[^>]*>.*?</h3>(.*)", page_html, re.DOTALL | re.IGNORECASE)
    body = m.group(1) if m else ""
    # drop the footnotes section if present
    body = re.split(r"<h[34][^>]*>\s*Footnotes", body, flags=re.IGNORECASE)[0]
    # drop page-number paragraphs and footnote anchor markers
    body = re.sub(r"<p><a name=\"page_\d+\">.*?</a>\.?</p>", " ", body,
                  flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<a\s+(?:name|href)=\"[^\"]*fn[^\"]*\"[^>]*>.*?</a>", " ", body,
                  flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<a name=\"page_\d+\"[^>]*>.*?</a>", " ", body,
                  flags=re.DOTALL | re.IGNORECASE)
    text = _TAG_RE.sub(" ", body)
    text = html.unescape(html.unescape(text))  # some pages are double-escaped
    text = _SIGLA_RE.sub("", text)
    return _WS_RE.sub(" ", text).strip()


_VERSE_MARK_RE = re.compile(r"(?<![\dA-Za-z,.:])(\d{1,3})\.\s+")


def _split_verses(text: str) -> list[tuple[int, str]]:
    """Split chapter text on 'N.' markers, requiring ascending verse numbers.

    The first marker may start mid-chapter (continuation pages); later
    markers must ascend with a bounded gap (missing numbers happen, and
    91:11 -> 91:18 is the largest legitimate jump in the corpus).
    """
    marks: list[tuple[int, re.Match]] = []
    last = 0
    for m in _VERSE_MARK_RE.finditer(text):
        n = int(m.group(1))
        if not marks:
            if 1 <= n <= 120:
                marks.append((n, m))
                last = n
        elif last < n <= last + 10:
            marks.append((n, m))
            last = n
    if not marks:
        return [(1, text)] if text else []
    out: list[tuple[int, str]] = []
    lead = text[: marks[0][1].start()].strip()
    if lead and marks[0][0] in (2, 3, 4):
        out.append((1, lead))  # unmarked verse 1 before the first marker
    for i, (n, m) in enumerate(marks):
        end = marks[i + 1][1].start() if i + 1 < len(marks) else len(text)
        seg = text[m.end(): end].strip()
        if seg:
            out.append((n, seg))
    return out


def parse_enoch() -> list[Verse]:
    by_ref: dict[tuple[int, int], str] = {}
    for fname in _page_files():
        page = fetch(BASE + fname, CACHE / fname).decode("utf-8", "replace")
        chapter = _HEADING_CORRECTIONS.get(fname) or _page_chapter(page)
        if chapter is None:
            continue  # title page, preface, introduction, symbols
        for vnum, vtext in _split_verses(_extract_body(page)):
            ref = (chapter, vnum)
            if ref in by_ref:
                print(f"  warning: duplicate 1 Enoch {chapter}:{vnum} "
                      f"on {fname}; keeping first occurrence")
                continue
            by_ref[ref] = vtext
    return [
        Verse(
            tradition=["ethiopian", "pseudepigrapha"],
            collection="ot_pseudepigrapha",
            book_id="1EN",
            book_title="1 Enoch",
            translation="R.H. Charles (1917)",
            chapter=ch,
            verse=v,
            text=text,
        )
        for (ch, v), text in sorted(by_ref.items())
    ]


if __name__ == "__main__":
    vs = parse_enoch()
    chapters = {v.chapter for v in vs}
    missing = sorted(set(range(1, 109)) - chapters)
    print(f"1 Enoch: {len(vs)} verses across {len(chapters)} chapters"
          f" (missing: {missing or 'none'})")
