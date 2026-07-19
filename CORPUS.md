# Canon Corpus Manifest

Every text in the database, its translation, source, and public domain
justification. Regenerate the database with `python pipeline/run.py`
(the book registry lives in `pipeline/books.py`).

## Sources & licensing

| Source | Books | Translation | PD justification |
|--------|-------|-------------|------------------|
| [ebible.org eng-web USFM](https://ebible.org/Scriptures/eng-web_usfm.zip) | 81 (OT 39, Deuterocanon/Apocrypha 15, NT 27) | World English Bible (WEB) | The WEB is expressly dedicated to the public domain by its producers ("The World English Bible is not copyrighted") |
| [sacred-texts.com/bib/boe](https://sacred-texts.com/bib/boe/) | 1 Enoch | R.H. Charles (1917) | Published 1917 (SPCK, London); pre-1930 publication, public domain in the US. Charles' own revision of his translation in *Apocrypha and Pseudepigrapha of the Old Testament* vol. 2 (Oxford, 1913), also public domain |

## Tradition tags

Protestant / Catholic / Orthodox tags follow those churches' published
canons (Orthodox includes the Greek and Slavonic appendix books 3–4
Maccabees, 1–2 Esdras, Prayer of Manasses, Psalm 151). **Ethiopian is a
best-effort mapping** of the Ethiopian Orthodox Tewahedo broader canon onto
the books we have; their canon differs structurally (e.g. Jubilees and
1 Enoch are canonical; Meqabyan replaces Maccabees) and several of its books
have no public domain English translation (see "Pending" below).

## Included books (82)

| Book | ID | Collection | Traditions |
|------|----|-----------|------------|
| Genesis | `GEN` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Exodus | `EXO` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Leviticus | `LEV` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Numbers | `NUM` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Deuteronomy | `DEU` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Joshua | `JOS` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Judges | `JDG` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Ruth | `RUT` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Samuel | `1SA` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Samuel | `2SA` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Kings | `1KI` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Kings | `2KI` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Chronicles | `1CH` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Chronicles | `2CH` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Ezra | `EZR` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Nehemiah | `NEH` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Esther | `EST` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Job | `JOB` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Psalms | `PSA` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Proverbs | `PRO` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Ecclesiastes | `ECC` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Song of Solomon | `SNG` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Isaiah | `ISA` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Jeremiah | `JER` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Lamentations | `LAM` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Ezekiel | `EZK` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Daniel | `DAN` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Hosea | `HOS` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Joel | `JOL` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Amos | `AMO` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Obadiah | `OBA` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Jonah | `JON` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Micah | `MIC` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Nahum | `NAM` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Habakkuk | `HAB` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Zephaniah | `ZEP` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Haggai | `HAG` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Zechariah | `ZEC` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Malachi | `MAL` | Old Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Tobit | `TOB` | Deuterocanon/Apocrypha | Catholic, Orthodox, Ethiopian |
| Judith | `JDT` | Deuterocanon/Apocrypha | Catholic, Orthodox, Ethiopian |
| Esther (Greek) | `ESG` | Deuterocanon/Apocrypha | Catholic, Orthodox |
| Wisdom of Solomon | `WIS` | Deuterocanon/Apocrypha | Catholic, Orthodox, Ethiopian |
| Sirach | `SIR` | Deuterocanon/Apocrypha | Catholic, Orthodox, Ethiopian |
| Baruch | `BAR` | Deuterocanon/Apocrypha | Catholic, Orthodox, Ethiopian |
| 1 Maccabees | `1MA` | Deuterocanon/Apocrypha | Catholic, Orthodox |
| 2 Maccabees | `2MA` | Deuterocanon/Apocrypha | Catholic, Orthodox |
| 1 Esdras | `1ES` | Deuterocanon/Apocrypha | Orthodox, Ethiopian |
| Prayer of Manasses | `MAN` | Deuterocanon/Apocrypha | Orthodox, Ethiopian |
| Psalm 151 | `PS2` | Deuterocanon/Apocrypha | Orthodox, Ethiopian |
| 3 Maccabees | `3MA` | Deuterocanon/Apocrypha | Orthodox |
| 2 Esdras | `2ES` | Deuterocanon/Apocrypha | Orthodox, Ethiopian |
| 4 Maccabees | `4MA` | Deuterocanon/Apocrypha | Orthodox |
| Daniel (Greek) | `DAG` | Deuterocanon/Apocrypha | Catholic, Orthodox |
| Matthew | `MAT` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Mark | `MRK` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Luke | `LUK` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| John | `JHN` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Acts | `ACT` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Romans | `ROM` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Corinthians | `1CO` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Corinthians | `2CO` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Galatians | `GAL` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Ephesians | `EPH` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Philippians | `PHP` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Colossians | `COL` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Thessalonians | `1TH` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Thessalonians | `2TH` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Timothy | `1TI` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Timothy | `2TI` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Titus | `TIT` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Philemon | `PHM` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Hebrews | `HEB` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| James | `JAS` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Peter | `1PE` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 Peter | `2PE` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 John | `1JN` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 2 John | `2JN` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 3 John | `3JN` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Jude | `JUD` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| Revelation | `REV` | New Testament | Protestant, Catholic, Orthodox, Ethiopian |
| 1 Enoch | `1EN` | OT Pseudepigrapha | Ethiopian, Pseudepigrapha |

## Versification notes

- **Greek Esther (`ESG`)**: the WEB merges the six LXX additions into the
  surrounding verses instead of using out-of-order KJV chapter numbers
  (documented in the translation's own preface). The affected verses (1:1,
  3:13, 4:17, 5:1, 8:12, 10:3) carry an `alt_versification` entry mapping
  them to the KJV addition chapters (11–16).
- **Greek Daniel (`DAG`)**: complete Greek Daniel; the Prayer of Azariah and
  Song of the Three appear within chapter 3, Susanna as chapter 13, Bel and
  the Dragon as chapter 14 — matching common English versification, so no
  alt mapping is needed.
- **Psalm 151 (`PS2`)** is stored as its own single-chapter book, per the WEB.
- **LXX vs Masoretic Psalm numbering**: the corpus uses Masoretic numbering
  (WEB). An LXX offset table is planned for `alt_versification` when a
  Septuagint translation (Brenton) is ingested.

## 1 Enoch source notes (Charles 1917 via sacred-texts)

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

## Pending, no public domain source

| Book | Traditions | Status |
|------|-----------|--------|
| 1 Meqabyan | Ethiopian | **pending — no PD source.** No public domain English translation exists; modern translations (e.g. Feqade-Selassie 2008, Curtin 2018-) are copyrighted. Do not ingest. |
| 2 Meqabyan | Ethiopian | **pending — no PD source.** Same as above. |
| 3 Meqabyan | Ethiopian | **pending — no PD source.** Same as above. |

## Planned next (PD sources identified, not yet ingested)

- **Jubilees** (Ethiopian canon; OT pseudepigrapha) — R.H. Charles (1902/1913),
  sacred-texts.com `bib/jub`.
- **Other OT Pseudepigrapha** (Testaments of the Twelve Patriarchs, Letter of
  Aristeas, 2 Baruch, etc.) — R.H. Charles, *Apocrypha and Pseudepigrapha of
  the Old Testament* (Oxford, 1913), public domain.
- **Brenton LXX** (1851, PD) — alternative Greek-based OT translation; would
  activate the LXX Psalm-numbering `alt_versification` table.
- **NT Apocrypha** (Protevangelium of James, Acts of Paul and Thecla, etc.) —
  M.R. James, *The Apocryphal New Testament* (1924): **verify status** —
  published 1924, PD in the US (pre-1930) but still in copyright in the UK
  until 2032 (James d. 1936); or use the older Ante-Nicene Fathers vol. 8
  translations (1886, unambiguously PD). Gospel of Thomas excluded — no PD
  English translation of the Coptic text exists.
