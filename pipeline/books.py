"""Book registry for the Canon corpus.

Tradition tags drive the UI filters. The protestant/catholic/orthodox tags
follow those churches' published canons; "ethiopian" is a best-effort mapping
of the Ethiopian Orthodox Tewahedo 81-book broader canon onto available books
(their canon also contains books with no public domain English translation —
see CORPUS.md). NT books are shared by all four traditions.
"""
from __future__ import annotations

ALL4 = ["protestant", "catholic", "orthodox", "ethiopian"]
CATH_ORTH_ETH = ["catholic", "orthodox", "ethiopian"]
CATH_ORTH = ["catholic", "orthodox"]
ORTH = ["orthodox"]
ORTH_ETH = ["orthodox", "ethiopian"]

# (usfm_file_prefix, book_id, title, collection, traditions, extra_aliases)
WEB_BOOKS: list[tuple[str, str, str, str, list[str], list[str]]] = [
    # --- Old Testament (39) ---
    ("02-GEN", "GEN", "Genesis", "ot", ALL4, ["gen", "ge", "gn"]),
    ("03-EXO", "EXO", "Exodus", "ot", ALL4, ["exo", "ex", "exod"]),
    ("04-LEV", "LEV", "Leviticus", "ot", ALL4, ["lev", "lv"]),
    ("05-NUM", "NUM", "Numbers", "ot", ALL4, ["num", "nm", "nu", "numb"]),
    ("06-DEU", "DEU", "Deuteronomy", "ot", ALL4, ["deu", "deut", "dt"]),
    ("07-JOS", "JOS", "Joshua", "ot", ALL4, ["jos", "josh"]),
    ("08-JDG", "JDG", "Judges", "ot", ALL4, ["jdg", "judg", "jgs"]),
    ("09-RUT", "RUT", "Ruth", "ot", ALL4, ["rut", "ru"]),
    ("10-1SA", "1SA", "1 Samuel", "ot", ALL4, ["1sa", "1 sam", "1sam", "1 sm"]),
    ("11-2SA", "2SA", "2 Samuel", "ot", ALL4, ["2sa", "2 sam", "2sam", "2 sm"]),
    ("12-1KI", "1KI", "1 Kings", "ot", ALL4, ["1ki", "1 kgs", "1kgs", "1 kings"]),
    ("13-2KI", "2KI", "2 Kings", "ot", ALL4, ["2ki", "2 kgs", "2kgs", "2 kings"]),
    ("14-1CH", "1CH", "1 Chronicles", "ot", ALL4, ["1ch", "1 chr", "1 chron", "1chr"]),
    ("15-2CH", "2CH", "2 Chronicles", "ot", ALL4, ["2ch", "2 chr", "2 chron", "2chr"]),
    ("16-EZR", "EZR", "Ezra", "ot", ALL4, ["ezr"]),
    ("17-NEH", "NEH", "Nehemiah", "ot", ALL4, ["neh"]),
    ("18-EST", "EST", "Esther", "ot", ALL4, ["est", "esth"]),
    ("19-JOB", "JOB", "Job", "ot", ALL4, ["jb"]),
    ("20-PSA", "PSA", "Psalms", "ot", ALL4, ["psa", "psalm", "ps", "pss"]),
    ("21-PRO", "PRO", "Proverbs", "ot", ALL4, ["pro", "prov", "prv"]),
    ("22-ECC", "ECC", "Ecclesiastes", "ot", ALL4, ["ecc", "eccl", "qoheleth"]),
    ("23-SNG", "SNG", "Song of Solomon", "ot", ALL4,
     ["sng", "song of songs", "song", "canticles", "sos"]),
    ("24-ISA", "ISA", "Isaiah", "ot", ALL4, ["isa", "is"]),
    ("25-JER", "JER", "Jeremiah", "ot", ALL4, ["jer"]),
    ("26-LAM", "LAM", "Lamentations", "ot", ALL4, ["lam"]),
    ("27-EZK", "EZK", "Ezekiel", "ot", ALL4, ["ezk", "ezek", "eze"]),
    ("28-DAN", "DAN", "Daniel", "ot", ALL4, ["dan", "dn"]),
    ("29-HOS", "HOS", "Hosea", "ot", ALL4, ["hos"]),
    ("30-JOL", "JOL", "Joel", "ot", ALL4, ["jol", "joel", "jl"]),
    ("31-AMO", "AMO", "Amos", "ot", ALL4, ["amo", "amos", "am"]),
    ("32-OBA", "OBA", "Obadiah", "ot", ALL4, ["oba", "obad", "ob"]),
    ("33-JON", "JON", "Jonah", "ot", ALL4, ["jon", "jonah"]),
    ("34-MIC", "MIC", "Micah", "ot", ALL4, ["mic"]),
    ("35-NAM", "NAM", "Nahum", "ot", ALL4, ["nam", "nah", "nahum"]),
    ("36-HAB", "HAB", "Habakkuk", "ot", ALL4, ["hab"]),
    ("37-ZEP", "ZEP", "Zephaniah", "ot", ALL4, ["zep", "zeph"]),
    ("38-HAG", "HAG", "Haggai", "ot", ALL4, ["hag"]),
    ("39-ZEC", "ZEC", "Zechariah", "ot", ALL4, ["zec", "zech"]),
    ("40-MAL", "MAL", "Malachi", "ot", ALL4, ["mal"]),
    # --- Deuterocanon / Apocrypha (15) ---
    ("41-TOB", "TOB", "Tobit", "deuterocanon", CATH_ORTH_ETH, ["tob", "tobias", "tb"]),
    ("42-JDT", "JDT", "Judith", "deuterocanon", CATH_ORTH_ETH, ["jdt", "jth"]),
    ("43-ESG", "ESG", "Esther (Greek)", "deuterocanon", CATH_ORTH,
     ["esg", "greek esther", "esther greek", "esther lxx"]),
    ("45-WIS", "WIS", "Wisdom of Solomon", "deuterocanon", CATH_ORTH_ETH,
     ["wis", "wisdom", "ws"]),
    ("46-SIR", "SIR", "Sirach", "deuterocanon", CATH_ORTH_ETH,
     ["sir", "ecclesiasticus", "ben sira"]),
    ("47-BAR", "BAR", "Baruch", "deuterocanon", CATH_ORTH_ETH, ["bar"]),
    ("52-1MA", "1MA", "1 Maccabees", "deuterocanon", CATH_ORTH,
     ["1ma", "1 macc", "1macc", "1 mac"]),
    ("53-2MA", "2MA", "2 Maccabees", "deuterocanon", CATH_ORTH,
     ["2ma", "2 macc", "2macc", "2 mac"]),
    ("54-1ES", "1ES", "1 Esdras", "deuterocanon", ORTH_ETH, ["1es", "1 esd"]),
    ("55-MAN", "MAN", "Prayer of Manasses", "deuterocanon", ORTH_ETH,
     ["man", "prayer of manasseh", "pr man", "manasseh", "manasses"]),
    ("56-PS2", "PS2", "Psalm 151", "deuterocanon", ORTH_ETH, ["ps2", "ps 151", "psalm 151"]),
    ("57-3MA", "3MA", "3 Maccabees", "deuterocanon", ORTH,
     ["3ma", "3 macc", "3macc", "3 mac"]),
    ("58-2ES", "2ES", "2 Esdras", "deuterocanon", ORTH_ETH,
     ["2es", "2 esd", "4 ezra", "ezra sutuel"]),
    ("59-4MA", "4MA", "4 Maccabees", "deuterocanon", ORTH,
     ["4ma", "4 macc", "4macc", "4 mac"]),
    ("66-DAG", "DAG", "Daniel (Greek)", "deuterocanon", CATH_ORTH,
     ["dag", "greek daniel", "daniel greek", "daniel lxx"]),
    # --- New Testament (27) ---
    ("70-MAT", "MAT", "Matthew", "nt", ALL4, ["mat", "matt", "mt"]),
    ("71-MRK", "MRK", "Mark", "nt", ALL4, ["mrk", "mk"]),
    ("72-LUK", "LUK", "Luke", "nt", ALL4, ["luk", "lk"]),
    ("73-JHN", "JHN", "John", "nt", ALL4, ["jhn", "jn"]),
    ("74-ACT", "ACT", "Acts", "nt", ALL4, ["act", "ac"]),
    ("75-ROM", "ROM", "Romans", "nt", ALL4, ["rom", "ro", "rm"]),
    ("76-1CO", "1CO", "1 Corinthians", "nt", ALL4, ["1co", "1 cor", "1cor"]),
    ("77-2CO", "2CO", "2 Corinthians", "nt", ALL4, ["2co", "2 cor", "2cor"]),
    ("78-GAL", "GAL", "Galatians", "nt", ALL4, ["gal"]),
    ("79-EPH", "EPH", "Ephesians", "nt", ALL4, ["eph"]),
    ("80-PHP", "PHP", "Philippians", "nt", ALL4, ["php", "phil"]),
    ("81-COL", "COL", "Colossians", "nt", ALL4, ["col"]),
    ("82-1TH", "1TH", "1 Thessalonians", "nt", ALL4, ["1th", "1 thess", "1thess", "1 thes"]),
    ("83-2TH", "2TH", "2 Thessalonians", "nt", ALL4, ["2th", "2 thess", "2thess", "2 thes"]),
    ("84-1TI", "1TI", "1 Timothy", "nt", ALL4, ["1ti", "1 tim", "1tim"]),
    ("85-2TI", "2TI", "2 Timothy", "nt", ALL4, ["2ti", "2 tim", "2tim"]),
    ("86-TIT", "TIT", "Titus", "nt", ALL4, ["tit", "ti"]),
    ("87-PHM", "PHM", "Philemon", "nt", ALL4, ["phm", "phlm"]),
    ("88-HEB", "HEB", "Hebrews", "nt", ALL4, ["heb"]),
    ("89-JAS", "JAS", "James", "nt", ALL4, ["jas", "jam", "jm"]),
    ("90-1PE", "1PE", "1 Peter", "nt", ALL4, ["1pe", "1 pet", "1pet", "1 pt"]),
    ("91-2PE", "2PE", "2 Peter", "nt", ALL4, ["2pe", "2 pet", "2pet", "2 pt"]),
    ("92-1JN", "1JN", "1 John", "nt", ALL4, ["1jn", "1 jn", "1john"]),
    ("93-2JN", "2JN", "2 John", "nt", ALL4, ["2jn", "2 jn", "2john"]),
    ("94-3JN", "3JN", "3 John", "nt", ALL4, ["3jn", "3 jn", "3john"]),
    ("95-JUD", "JUD", "Jude", "nt", ALL4, ["jud", "jude"]),
    ("96-REV", "REV", "Revelation", "nt", ALL4, ["rev", "apocalypse", "rv"]),
]

WEB_SOURCE = "https://ebible.org/Scriptures/eng-web_usfm.zip"
WEB_LICENSE = "Public domain (the WEB is expressly dedicated to the public domain)"
WEB_TRANSLATION = "World English Bible (WEB)"


def registry() -> list[dict]:
    """Full ordered book metadata list for build_db, WEB books then extras."""
    books: list[dict] = []
    for order, (prefix, book_id, title, collection, trads, aliases) in enumerate(
        WEB_BOOKS, start=1
    ):
        books.append(
            {
                "usfm_prefix": prefix,
                "book_id": book_id,
                "book_title": title,
                "collection": collection,
                "translation": WEB_TRANSLATION,
                "traditions": trads,
                "source_url": WEB_SOURCE,
                "license": WEB_LICENSE,
                "aliases": sorted({title.lower(), *aliases}),
                "sort_order": order,
            }
        )
    books.append(
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
            "sort_order": 100,
        }
    )
    books.append(
        {
            "book_id": "JUB",
            "book_title": "Jubilees",
            "collection": "ot_pseudepigrapha",
            "translation": "R.H. Charles (1902)",
            "traditions": ["ethiopian", "pseudepigrapha"],
            "source_url": "https://sacred-texts.com/bib/jub/",
            "license": "Public domain (published 1902, Oxford; pre-1930)",
            "aliases": ["jubilees", "jub", "book of jubilees", "little genesis"],
            "sort_order": 101,
        }
    )
    return books


# WEB's Greek Esther merges the LXX additions into the surrounding verses
# rather than using out-of-order KJV chapter numbers (documented in its \ip
# preface). Recorded per verse so the UI can explain the versification.
ESG_ALT_VERSIFICATION: dict[tuple[int, int], dict[str, str]] = {
    (1, 1): {"lxx": "includes Addition A (KJV 11:2-12:6), merged before 1:1"},
    (3, 13): {"lxx": "includes Addition B (KJV 13:1-7), the king's letter"},
    (4, 17): {"lxx": "includes Addition C (KJV 13:8-14:19), the prayers"},
    (5, 1): {"lxx": "includes Addition D (KJV 15:1-16), Esther before the king"},
    (8, 12): {"lxx": "includes Addition E (KJV 16:1-24), the second letter"},
    (10, 3): {"lxx": "includes Addition F (KJV 10:4-11:1), the epilogue"},
}
