import { createDbWorker, type WorkerHttpvfs } from 'sql.js-httpvfs'
// worker + wasm shipped by sql.js-httpvfs; ?url makes Vite emit them as assets
import workerUrl from 'sql.js-httpvfs/dist/sqlite.worker.js?url'
import wasmUrl from 'sql.js-httpvfs/dist/sql-wasm.wasm?url'

let workerPromise: Promise<WorkerHttpvfs> | null = null

export function getDb(): Promise<WorkerHttpvfs> {
  workerPromise ??= createDbWorker(
    [
      {
        from: 'inline',
        config: {
          serverMode: 'full',
          url: new URL('canon.db', document.baseURI).toString(),
          requestChunkSize: 4096, // matches the db's page_size
        },
      },
    ],
    new URL(workerUrl, document.baseURI).toString(),
    new URL(wasmUrl, document.baseURI).toString(),
  )
  return workerPromise
}

export async function query<T = Record<string, unknown>>(
  sql: string,
  params: unknown[] = [],
): Promise<T[]> {
  const db = await getDb()
  return (await db.db.query(sql, params)) as T[]
}
