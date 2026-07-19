import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  COLLECTIONS,
  TRADITIONS,
  loadBooks,
  lookupReference,
  parseReference,
  search,
  context,
  type Book,
  type SearchHit,
  type VerseRow,
} from './canon'

type Status = 'loading' | 'ready' | 'error'

function refLabel(hit: { book_title: string; chapter: number; verse: number }) {
  return `${hit.book_title} ${hit.chapter}:${hit.verse}`
}

function ResultCard({ hit }: { hit: SearchHit }) {
  const [ctx, setCtx] = useState<VerseRow[] | null>(null)
  const [busy, setBusy] = useState(false)

  const toggle = useCallback(async () => {
    if (ctx) {
      setCtx(null)
      return
    }
    setBusy(true)
    try {
      setCtx(await context(hit.book_id, hit.chapter, hit.verse, 2))
    } finally {
      setBusy(false)
    }
  }, [ctx, hit])

  return (
    <li className="rounded-lg border border-stone-200 bg-white p-4 shadow-sm">
      <div className="mb-1 flex items-baseline justify-between gap-2">
        <span className="font-semibold text-stone-900">{refLabel(hit)}</span>
        <button
          onClick={toggle}
          disabled={busy}
          className="shrink-0 text-sm text-amber-700 hover:text-amber-900 hover:underline disabled:opacity-50"
        >
          {ctx ? 'Hide context' : 'Show context'}
        </button>
      </div>
      {ctx ? (
        <div className="space-y-1">
          {ctx.map((v) => (
            <p
              key={v.id}
              className={
                v.verse === hit.verse
                  ? 'rounded bg-amber-50 p-1 text-stone-900'
                  : 'p-1 text-stone-600'
              }
            >
              <sup className="mr-1 font-semibold text-stone-400">{v.verse}</sup>
              {v.text}
            </p>
          ))}
        </div>
      ) : (
        <p
          className="text-stone-700"
          dangerouslySetInnerHTML={{ __html: hit.snippet }}
        />
      )}
    </li>
  )
}

export default function App() {
  const [status, setStatus] = useState<Status>('loading')
  const [error, setError] = useState('')
  const [books, setBooks] = useState<Book[]>([])
  const [input, setInput] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [traditions, setTraditions] = useState<string[]>([])
  const [bookId, setBookId] = useState('')
  const [hits, setHits] = useState<SearchHit[]>([])
  const [refRows, setRefRows] = useState<VerseRow[] | null>(null)
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    loadBooks()
      .then((b) => {
        setBooks(b)
        setStatus('ready')
      })
      .catch((e) => {
        setError(String(e))
        setStatus('error')
      })
  }, [])

  const visibleBooks = useMemo(
    () =>
      traditions.length
        ? books.filter((b) => b.traditions.some((t) => traditions.includes(t)))
        : books,
    [books, traditions],
  )

  const runSearch = useCallback(
    async (q: string) => {
      setSubmitted(q)
      setRefRows(null)
      setHits([])
      if (!q.trim()) return
      setSearching(true)
      try {
        const reference = parseReference(q, books)
        if (reference) {
          setRefRows(await lookupReference(reference))
        } else {
          setHits(
            await search(q, {
              bookIds: bookId ? [bookId] : null,
              traditions: traditions.length ? traditions : null,
            }),
          )
        }
      } catch (e) {
        setError(String(e))
        setStatus('error')
      } finally {
        setSearching(false)
      }
    },
    [books, bookId, traditions],
  )

  const toggleTradition = (t: string) =>
    setTraditions((cur) =>
      cur.includes(t) ? cur.filter((x) => x !== t) : [...cur, t],
    )

  return (
    <div className="min-h-screen bg-stone-100 text-stone-900">
      <div className="mx-auto max-w-3xl px-4 py-10">
        <header className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Canon</h1>
          <p className="mt-1 text-stone-500">
            Full-text search across biblical &amp; parabiblical literature. Try
            a keyword (<em>watchers</em>), a phrase (
            <em>&quot;clouds invited me&quot;</em>), or a reference (
            <em>John 3:16</em>, <em>1 Enoch 14:8</em>).
          </p>
        </header>

        <form
          onSubmit={(e) => {
            e.preventDefault()
            runSearch(input)
          }}
          className="mb-4 flex gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Search the corpus…"
            aria-label="Search query"
            className="w-full rounded-lg border border-stone-300 bg-white px-4 py-2 shadow-sm outline-none focus:border-amber-600 focus:ring-2 focus:ring-amber-200"
          />
          <button
            type="submit"
            disabled={status !== 'ready' || searching}
            className="rounded-lg bg-amber-700 px-5 py-2 font-medium text-white shadow-sm hover:bg-amber-800 disabled:opacity-50"
          >
            {searching ? '…' : 'Search'}
          </button>
        </form>

        <div className="mb-6 flex flex-wrap items-center gap-2">
          {TRADITIONS.map((t) => (
            <button
              key={t.id}
              onClick={() => toggleTradition(t.id)}
              className={`rounded-full border px-3 py-1 text-sm ${
                traditions.includes(t.id)
                  ? 'border-amber-700 bg-amber-700 text-white'
                  : 'border-stone-300 bg-white text-stone-600 hover:border-stone-400'
              }`}
            >
              {t.label}
            </button>
          ))}
          <select
            value={bookId}
            onChange={(e) => setBookId(e.target.value)}
            aria-label="Filter by book"
            className="ml-auto rounded-lg border border-stone-300 bg-white px-3 py-1.5 text-sm"
          >
            <option value="">All books</option>
            {Object.entries(COLLECTIONS).map(([coll, label]) => {
              const group = visibleBooks.filter((b) => b.collection === coll)
              return group.length ? (
                <optgroup key={coll} label={label}>
                  {group.map((b) => (
                    <option key={b.book_id} value={b.book_id}>
                      {b.book_title}
                    </option>
                  ))}
                </optgroup>
              ) : null
            })}
          </select>
        </div>

        {status === 'loading' && (
          <p className="text-stone-500">Loading database…</p>
        )}
        {status === 'error' && (
          <p className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">
            {error}
          </p>
        )}

        {refRows && (
          <section>
            <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-stone-500">
              {refRows.length
                ? `${refRows[0].book_title} ${refRows[0].chapter}`
                : 'Reference not found'}
            </h2>
            <div className="rounded-lg border border-stone-200 bg-white p-4 shadow-sm">
              {refRows.length === 0 && (
                <p className="text-stone-500">
                  That reference does not exist in the corpus.
                </p>
              )}
              {refRows.map((v) => (
                <p key={v.id} className="mb-2">
                  <sup className="mr-1 font-semibold text-stone-400">
                    {v.verse}
                  </sup>
                  {v.text}
                </p>
              ))}
            </div>
          </section>
        )}

        {!refRows && submitted && !searching && (
          <p className="mb-3 text-sm text-stone-500">
            {hits.length
              ? `${hits.length}${hits.length === 50 ? '+' : ''} result${
                  hits.length === 1 ? '' : 's'
                } for “${submitted}”`
              : `No results for “${submitted}”`}
          </p>
        )}
        {!refRows && hits.length > 0 && (
          <ul className="space-y-3">
            {hits.map((h) => (
              <ResultCard
                key={`${h.book_id}-${h.chapter}-${h.verse}`}
                hit={h}
              />
            ))}
          </ul>
        )}

        <footer className="mt-12 border-t border-stone-200 pt-4 text-sm text-stone-400">
          {books.length ? `${books.length} books · ` : ''}World English Bible
          (OT · Deuterocanon · NT) and R.H. Charles' 1 Enoch (1917) &amp;
          Jubilees (1902). All texts public domain —{' '}
          <a
            className="underline hover:text-stone-600"
            href="https://github.com/WesWuy/canon/blob/main/CORPUS.md"
          >
            corpus manifest
          </a>
          .
        </footer>
      </div>
    </div>
  )
}
