import { createDbWorker, type WorkerHttpvfs } from 'sql.js-httpvfs'
// worker + wasm shipped by sql.js-httpvfs; ?url makes Vite emit them as assets
import workerUrl from 'sql.js-httpvfs/dist/sqlite.worker.js?url'
import wasmUrl from 'sql.js-httpvfs/dist/sql-wasm.wasm?url'

let workerPromise: Promise<WorkerHttpvfs> | null = null

/** Database size via a 1-byte range request. Some hosts (GitHub Pages)
 *  gzip plain GET/HEAD responses, hiding the true Content-Length — but a
 *  206 response always reports the full size in Content-Range. */
async function fetchFileLength(url: string): Promise<number> {
  const resp = await fetch(url, { headers: { Range: 'bytes=0-0' } })
  const range = resp.headers.get('Content-Range') // "bytes 0-0/417792"
  const m = range?.match(/\/(\d+)\s*$/)
  if (m) return parseInt(m[1], 10)
  const len = resp.headers.get('Content-Length')
  if (resp.ok && !resp.headers.get('Content-Encoding') && len) {
    return parseInt(len, 10) // server ignored Range but gave a real length
  }
  throw new Error(`Cannot determine size of ${url} (HTTP ${resp.status})`)
}

export function getDb(): Promise<WorkerHttpvfs> {
  // "chunked" mode (single chunk canon.db.000) rather than "full": full mode
  // learns the file size from a HEAD Content-Length, which gzipping hosts
  // like GitHub Pages don't expose; chunked mode takes the size up front and
  // then only ever issues Range requests, which are never gzipped.
  workerPromise ??= (async () => {
    const urlPrefix = new URL('canon.db.', document.baseURI).toString()
    const length = await fetchFileLength(urlPrefix + '000')
    return createDbWorker(
      [
        {
          from: 'inline',
          config: {
            serverMode: 'chunked',
            urlPrefix,
            suffixLength: 3,
            serverChunkSize: length, // one chunk = the whole file
            databaseLengthBytes: length,
            requestChunkSize: 4096, // matches the db's page_size
          },
        },
      ],
      new URL(workerUrl, document.baseURI).toString(),
      new URL(wasmUrl, document.baseURI).toString(),
    )
  })()
  return workerPromise
}

export async function query<T = Record<string, unknown>>(
  sql: string,
  params: unknown[] = [],
): Promise<T[]> {
  const db = await getDb()
  return (await db.db.query(sql, params)) as T[]
}
