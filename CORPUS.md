# Canon Corpus Manifest

Every text in the database, its translation, source, and public domain
justification. Regenerate the database with `python pipeline/run.py`.

## Included (v1 test corpus)

| Book | ID | Collection | Traditions | Translation | Source | PD justification |
|------|----|-----------|------------|-------------|--------|------------------|
| Jude | `JUD` | New Testament | Protestant, Catholic, Orthodox, Ethiopian | World English Bible (WEB) | [ebible.org eng-web USFM](https://ebible.org/Scriptures/eng-web_usfm.zip) | The WEB is expressly dedicated to the public domain by its producers ("The World English Bible is not copyrighted") |
| 1 Enoch | `1EN` | OT Pseudepigrapha | Ethiopian, Pseudepigrapha | R.H. Charles (1917) | [sacred-texts.com/bib/boe](https://sacred-texts.com/bib/boe/) | Published 1917 (SPCK, London); pre-1930 publication, public domain in the US. Charles' own revision of his translation in *Apocrypha and Pseudepigrapha of the Old Testament* vol. 2 (Oxford, 1913), also public domain |

### Source notes — 1 Enoch (Charles 1917 via sacred-texts)

- The sacred-texts index page mislabels two chapters (LV as LIV, LXXXI as
  LXXI); the pipeline reads chapter numbers from each page's own heading.
- Page `boe081.htm`'s heading itself says "CHAPTER LXXVII" but contains
  chapter 78 (verified against content: 78:1 "the names of the sun");
  corrected explicitly in `pipeline/parse_enoch.py`.
- Charles prints the Apocalypse of Weeks in his reconstructed order
  (91:1–11, 18–19 → 92 → 93 → 91:12–17). Verses are stored under their
  canonical chapter:verse numbers regardless of print order.
- Some verse numbers are missing in the source (e.g. 14:10); that text is
  folded into the preceding verse, so verse counts are slightly below
  critical editions (951 verses parsed across all 108 chapters).
- Charles' critical sigla (⌈⌉ emendation brackets, daggers) are stripped;
  his round and square interpolation brackets are retained.

## Planned, pending a public domain source

| Book | Traditions | Status |
|------|-----------|--------|
| 1 Meqabyan | Ethiopian | **pending — no PD source.** No public domain English translation exists; modern translations (e.g. Feqade-Selassie 2008, Curtin 2018-) are copyrighted. Do not ingest. |
| 2 Meqabyan | Ethiopian | **pending — no PD source.** Same as above. |
| 3 Meqabyan | Ethiopian | **pending — no PD source.** Same as above. |

## Planned next (PD sources identified, not yet ingested)

- **Protestant canon (65 remaining books)** — WEB, ebible.org (public domain).
- **Deuterocanon / Apocrypha** (Tobit, Judith, Wisdom, Sirach, Baruch,
  1–2 Maccabees, Greek Esther, Daniel additions, etc.) — WEB Apocrypha
  (ebible.org `eng-web` includes them) or Brenton LXX (1851, PD).
- **Orthodox additions** (3–4 Maccabees, Prayer of Manasseh, Psalm 151,
  1–2 Esdras) — Brenton LXX / KJV Apocrypha (PD).
- **OT Pseudepigrapha** (Jubilees, Testaments of the Twelve Patriarchs,
  Letter of Aristeas, etc.) — R.H. Charles, *Apocrypha and Pseudepigrapha
  of the Old Testament* (Oxford, 1913), public domain.
- **NT Apocrypha** (Gospel of Thomas excluded — no PD English translation
  of the Coptic; Protevangelium of James, Acts of Paul and Thecla, etc.) —
  M.R. James, *The Apocryphal New Testament* (1924): **verify status** —
  published 1924, PD in the US (pre-1930) but still in copyright in the UK
  until 2032 (James d. 1936); or use the older Ante-Nicene Fathers vol. 8
  translations (1886, unambiguously PD).

## Versification

`alt_versification` is a per-verse JSON map reserved for cross-system verse
mappings (LXX vs Masoretic Psalms numbering, Greek Esther additions, Daniel
additions). Empty for the v1 test corpus — neither Jude nor 1 Enoch has a
competing versification system in scope.
