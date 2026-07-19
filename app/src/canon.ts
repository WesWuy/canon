import { query } from './db'

export const TRADITIONS = [
  { id: 'protestant', label: 'Protestant' },
  { id: 'catholic', label: 'Catholic' },
  { id: 'orthodox', label: 'Orthodox' },
  { id: 'ethiopian', label: 'Ethiopian' },
  { id: 'pseudepigrapha', label: 'Pseudepigrapha' },
  { id: 'nt_apocrypha', label: 'NT Apocrypha' },
] as const

export interface Book {
  book_id: string
  book_title: string
  collection: string
  translation: string
  aliases: string[]
  traditions: string[]
  max_chapter: number
}

export const COLLECTIONS: Record<string, string> = {
  ot: 'Old Testament',
  deuterocanon: 'Deuterocanon / Apocrypha',
  nt: 'New Testament',
  ot_pseudepigrapha: 'OT Pseudepigrapha',
}

export interface SearchHit {
  book_id: string
  book_title: string
  chapter: number
  verse: number
  snippet: string
  text: string
}

export interface VerseRow {
  id: number
  book_id: string
  book_title: string
  chapter: number
  verse: number
  text: string
}

export async function loadBooks(): Promise<Book[]> {
  const rows = await query<{
    book_id: string
    book_title: string
    collection: string
    translation: string
    aliases: string
    traditions: string
    max_chapter: number
  }>(
    `SELECT b.book_id, b.book_title, b.collection, b.translation, b.aliases,
            (SELECT group_concat(t.tradition) FROM book_traditions t
              WHERE t.book_id = b.book_id) AS traditions,
            (SELECT max(v.chapter) FROM verses v
              WHERE v.book_id = b.book_id) AS max_chapter
       FROM books b ORDER BY b.sort_order`,
  )
  return rows.map((r) => ({
    ...r,
    aliases: JSON.parse(r.aliases) as string[],
    traditions: (r.traditions ?? '').split(','),
  }))
}

/** Escape user input into a safe FTS5 MATCH expression.
 *  Quoted phrases are kept as phrases; everything else becomes AND'd terms. */
export function toFtsQuery(input: string): string | null {
  const parts: string[] = []
  const re = /"([^"]+)"|(\S+)/g
  let m: RegExpExecArray | null
  while ((m = re.exec(input)) !== null) {
    const token = (m[1] ?? m[2]).replace(/"/g, '')
    const words = token.match(/[\p{L}\p{N}’']+/gu)
    if (!words?.length) continue
    parts.push(`"${words.join(' ')}"`) // quoting disables FTS syntax injection
  }
  return parts.length ? parts.join(' ') : null
}

function bookFilterSql(bookIds: string[] | null, traditions: string[] | null) {
  const clauses: string[] = []
  const params: unknown[] = []
  if (bookIds?.length) {
    clauses.push(`v.book_id IN (${bookIds.map(() => '?').join(',')})`)
    params.push(...bookIds)
  }
  if (traditions?.length) {
    clauses.push(
      `v.book_id IN (SELECT book_id FROM book_traditions
         WHERE tradition IN (${traditions.map(() => '?').join(',')}))`,
    )
    params.push(...traditions)
  }
  return { where: clauses.map((c) => ` AND ${c}`).join(''), params }
}

export async function search(
  input: string,
  opts: { bookIds?: string[] | null; traditions?: string[] | null; limit?: number } = {},
): Promise<SearchHit[]> {
  const fts = toFtsQuery(input)
  if (!fts) return []
  const { where, params } = bookFilterSql(
    opts.bookIds ?? null,
    opts.traditions ?? null,
  )
  return query<SearchHit>(
    `SELECT v.book_id, b.book_title, v.chapter, v.verse, v.text,
            snippet(verses_fts, 0, '<mark>', '</mark>', '…', 24) AS snippet
       FROM verses_fts
       JOIN verses v ON v.id = verses_fts.rowid
       JOIN books b ON b.book_id = v.book_id
      WHERE verses_fts MATCH ?${where}
      ORDER BY rank
      LIMIT ?`,
    [fts, ...params, opts.limit ?? 50],
  )
}

/** Fetch a verse plus `radius` verses of surrounding context. */
export async function context(
  bookId: string,
  chapter: number,
  verse: number,
  radius = 2,
): Promise<VerseRow[]> {
  return query<VerseRow>(
    `SELECT v.id, v.book_id, b.book_title, v.chapter, v.verse, v.text
       FROM verses v JOIN books b ON b.book_id = v.book_id
      WHERE v.book_id = ? AND v.chapter = ? AND v.verse BETWEEN ? AND ?
      ORDER BY v.verse`,
    [bookId, chapter, Math.max(1, verse - radius), verse + radius],
  )
}

export interface Reference {
  book: Book
  chapter: number
  verse: number | null
}

/** Parse a direct reference like "1 Enoch 14:8", "Jude 5", "Psalm 151 5".
 *
 * Matches the longest book name/alias prefix, then reads "C", "C:V", or
 * "C.V" from the remainder. A bare number on a single-chapter book is a
 * verse ("Jude 5" -> 1:5). Bare book names are NOT references — they fall
 * through to full-text search. */
export function parseReference(input: string, books: Book[]): Reference | null {
  const q = input.trim().toLowerCase().replace(/\s+/g, ' ')
  const candidates: { book: Book; name: string }[] = []
  for (const book of books) {
    for (const name of [book.book_title.toLowerCase(), ...book.aliases]) {
      if (
        q.startsWith(name) &&
        (q.length === name.length || /[\s:.]/.test(q[name.length]))
      ) {
        candidates.push({ book, name })
      }
    }
  }
  if (!candidates.length) return null
  const { book, name } = candidates.sort(
    (a, b) => b.name.length - a.name.length,
  )[0]
  const rest = q.slice(name.length).trim()
  const m = rest.match(/^(\d+)(?:\s*[:.]\s*(\d+))?$/)
  if (!m) return null
  const first = parseInt(m[1], 10)
  const second = m[2] ? parseInt(m[2], 10) : null
  if (second === null && book.max_chapter === 1) {
    return { book, chapter: 1, verse: first }
  }
  return { book, chapter: first, verse: second }
}

export async function lookupReference(ref: Reference): Promise<VerseRow[]> {
  if (ref.verse !== null) {
    return context(ref.book.book_id, ref.chapter, ref.verse, 0)
  }
  return query<VerseRow>(
    `SELECT v.id, v.book_id, b.book_title, v.chapter, v.verse, v.text
       FROM verses v JOIN books b ON b.book_id = v.book_id
      WHERE v.book_id = ? AND v.chapter = ? ORDER BY v.verse`,
    [ref.book.book_id, ref.chapter],
  )
}
