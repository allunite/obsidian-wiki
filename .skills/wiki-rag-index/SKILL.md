---
name: wiki-rag-index
description: >
  Build and refresh a ClickHouse-backed RAG index over the Obsidian wiki and raw sources. Use this skill
  when the user says "reindex the wiki", "build the RAG index", "refresh embeddings", "index to ClickHouse",
  "/wiki-rag-index", "rebuild semantic search", or "sync the vault to ClickHouse". Also use after a batch
  ingest when the user wants semantic search to see the newly written pages. Supports incremental delta
  reindex (only changed files) and full rebuild. Works with OpenAI (default), Ollama, or LM Studio as the
  embedding provider.
---

# Wiki RAG Index — ClickHouse-backed Semantic Search

You are building or refreshing a ClickHouse table that stores chunked wiki pages and their embeddings.
This index powers the semantic search tier in `wiki-query` and `wiki-ingest`. Without it, those skills
fall back to QMD (if configured) then Grep. With it, concept-level search over the vault is fast.

## Before You Start

1. Read `~/.obsidian-wiki/config` for `OBSIDIAN_VAULT_PATH`. Fall back to `.env` if inside the obsidian-wiki repo.
2. Load RAG config from `.env`:
   - `CLICKHOUSE_URL` (required, e.g. `http://localhost:8123`)
   - `CLICKHOUSE_DATABASE` (default: `obsidian_rag`)
   - `CLICKHOUSE_USER` / `CLICKHOUSE_PASSWORD` (optional)
   - `RAG_EMBEDDING_PROVIDER` — `openai` (default), `ollama`, or `lmstudio`
   - `RAG_EMBEDDING_MODEL` — `text-embedding-3-small` (OpenAI default), `bge-m3` (local default)
   - `RAG_EMBEDDING_DIMS` — `1536` for `text-embedding-3-small`, `1024` for `bge-m3`
   - `RAG_WIKI_COLLECTION` — logical collection name, default `wiki`
   - `RAG_PAPERS_COLLECTION` — logical name for raw sources, default `papers`
   - `OPENAI_API_KEY` — required when provider is `openai`
   - `OLLAMA_URL` — default `http://localhost:11434`
   - `LMSTUDIO_URL` — default `http://localhost:1234/v1`
3. If `CLICKHOUSE_URL` is unset, stop and tell the user to configure it in `.env` (point them at `.env.example`).
4. Determine scope from the user's request:
   - **`wiki`** — index pages under `$OBSIDIAN_VAULT_PATH` (the compiled knowledge base)
   - **`papers`** — index raw sources under `$OBSIDIAN_SOURCES_DIR` and `$OBSIDIAN_VAULT_PATH/$OBSIDIAN_RAW_DIR` (the unprocessed material)
   - **`both`** (default when unspecified) — run one after the other

## Step 1: Health Check

Before doing any indexing work, confirm ClickHouse and the embedding provider are reachable:

```bash
# ClickHouse ping — should return "Ok."
curl -sS --fail "$CLICKHOUSE_URL/ping" \
  ${CLICKHOUSE_USER:+-u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD"}

# Embedding provider ping
case "$RAG_EMBEDDING_PROVIDER" in
  openai)   curl -sS --fail https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY" > /dev/null ;;
  ollama)   curl -sS --fail "${OLLAMA_URL:-http://localhost:11434}/api/tags" > /dev/null ;;
  lmstudio) curl -sS --fail "${LMSTUDIO_URL:-http://localhost:1234/v1}/models" > /dev/null ;;
esac
```

If either check fails, report the error and stop. Don't guess at defaults — the user needs to fix their config.

## Step 2: Bootstrap Schema (idempotent)

Run this SQL via the HTTP interface. `IF NOT EXISTS` means it's safe to re-run every invocation.

```sql
CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DATABASE};

CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DATABASE}.rag_chunks (
  id            UUID DEFAULT generateUUIDv4(),
  collection    LowCardinality(String),
  vault_path    String,
  heading_path  String,
  chunk_index   UInt32,
  chunk_text    String,
  embedding     Array(Float32),
  token_count   UInt32,
  content_hash  String,
  tags          Array(String),
  updated_at    DateTime DEFAULT now(),
  INDEX idx_text chunk_text TYPE tokenbf_v1(32768, 3, 0) GRANULARITY 4
) ENGINE = MergeTree
ORDER BY (collection, vault_path, chunk_index);
```

Post it:

```bash
curl -sS "$CLICKHOUSE_URL/?database=$CLICKHOUSE_DATABASE" \
  ${CLICKHOUSE_USER:+-u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD"} \
  --data-binary @schema.sql
```

**HNSW vector index (optional, ClickHouse 24.x+):** if the user wants ANN speedup on large vaults, add:

```sql
ALTER TABLE {CLICKHOUSE_DATABASE}.rag_chunks
  ADD INDEX IF NOT EXISTS idx_vec embedding TYPE vector_similarity('hnsw', 'cosineDistance') GRANULARITY 1;
```

Gate this on `SET allow_experimental_vector_similarity_index = 1` at session scope. On older ClickHouse versions, brute-force `cosineDistance` on `Array(Float32)` still works — it's just O(n) scans.

## Step 3: Load the Embedding Helper

Paste this shell function into your working shell. It abstracts the three providers behind one call:

```bash
rag_embed() {
  # rag_embed "text to embed" → prints JSON array to stdout
  local text="$1"
  case "${RAG_EMBEDDING_PROVIDER:-openai}" in
    openai)
      curl -sS https://api.openai.com/v1/embeddings \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$(jq -cn --arg m "${RAG_EMBEDDING_MODEL:-text-embedding-3-small}" --arg p "$text" \
              '{model:$m, input:$p}')" \
        | jq -c '.data[0].embedding'
      ;;
    ollama)
      curl -sS "${OLLAMA_URL:-http://localhost:11434}/api/embeddings" \
        -H "Content-Type: application/json" \
        -d "$(jq -cn --arg m "${RAG_EMBEDDING_MODEL:-bge-m3}" --arg p "$text" \
              '{model:$m, prompt:$p}')" \
        | jq -c '.embedding'
      ;;
    lmstudio)
      curl -sS "${LMSTUDIO_URL:-http://localhost:1234/v1}/embeddings" \
        -H "Content-Type: application/json" \
        -d "$(jq -cn --arg m "${RAG_EMBEDDING_MODEL:-bge-m3}" --arg p "$text" \
              '{model:$m, input:$p}')" \
        | jq -c '.data[0].embedding'
      ;;
    *) echo "unknown RAG_EMBEDDING_PROVIDER: $RAG_EMBEDDING_PROVIDER" >&2; return 2 ;;
  esac
}
```

Sanity-check on first run: `rag_embed "hello world" | jq 'length'` — should print the expected dims
(`1536` for OpenAI's `text-embedding-3-small`, `1024` for `bge-m3`). If the length doesn't match
`RAG_EMBEDDING_DIMS`, stop and fix the env.

## Step 4: Chunk Files

For each markdown file in scope, split by heading hierarchy with a ~500-token ceiling. Use the Python
helper below (inlined as a heredoc — no separate script file needed):

```bash
rag_chunk() {
  # rag_chunk <file-path> → prints JSONL chunks to stdout
  # Each line: {"heading_path": "...", "chunk_text": "...", "token_count": N, "chunk_index": I}
  python3 - "$1" <<'PY'
import sys, json, re, pathlib
path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="replace")
# Strip YAML frontmatter (not content — it's indexed as metadata separately)
text = re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.S)

MAX_TOKENS = 500      # word-count approximation, words × 1.3 ≈ tokens
WORDS_PER_CHUNK = int(MAX_TOKENS / 1.3)

stack = ["", "", "", "", "", ""]  # H1..H6
buf, idx = [], 0
def flush():
    global buf, idx
    if not buf: return
    body = "\n".join(buf).strip()
    if not body: buf = []; return
    path_parts = [h for h in stack if h]
    toks = int(len(body.split()) * 1.3)
    print(json.dumps({
        "heading_path": " > ".join(path_parts),
        "chunk_text": body,
        "token_count": toks,
        "chunk_index": idx,
    }, ensure_ascii=False))
    idx += 1
    buf = []

words_in_buf = 0
for line in text.splitlines():
    m = re.match(r'^(#{1,6})\s+(.*)$', line)
    if m:
        flush()
        level = len(m.group(1))
        stack[level-1] = m.group(2).strip()
        for i in range(level, 6): stack[i] = ""
        words_in_buf = 0
        continue
    buf.append(line)
    words_in_buf += len(line.split())
    if words_in_buf >= WORDS_PER_CHUNK:
        flush()
        words_in_buf = 0
flush()
PY
}
```

Empty chunks are silently dropped. Files with no headings produce one flat chunk per 500-word window.

## Step 5: Delta Detection

The manifest at `$OBSIDIAN_VAULT_PATH/manifest.json` is the source of truth for what's been indexed.
Extend its per-file `files` entry with two new keys:

```json
"concepts/rag.md": {
  "sha256": "abc...",
  "size": 12345,
  "mtime": 1714000000,
  "rag_indexed_hash": "abc...",
  "rag_chunk_count": 7
}
```

For each candidate file:

1. Compute current sha256: `sha256sum "$file" | awk '{print $1}'`
2. Read `rag_indexed_hash` for this path from the manifest
3. If current hash == `rag_indexed_hash` → **skip** (unchanged since last index)
4. Otherwise → reindex this file

If the user requests a full rebuild (e.g. "reindex everything", "force reindex"), ignore the hash and
reindex all files. Also truncate the table for each collection first:

```sql
ALTER TABLE rag_chunks DELETE WHERE collection = '{collection}' SETTINGS mutations_sync = 1;
```

## Step 6: Index a Single File

For each changed file (or every file on full rebuild):

1. **Delete existing chunks** for this path before re-inserting (avoids duplicates):
   ```sql
   ALTER TABLE rag_chunks
     DELETE WHERE collection = '{collection}' AND vault_path = '{relative_path}'
     SETTINGS mutations_sync = 1;
   ```

2. **Read the frontmatter** to extract `tags` (and skip the file if `visibility/pii` is present and the
   user has not opted into indexing PII). Default behavior: index everything, since the vault itself is
   the single source of truth; visibility filtering happens at query time.

3. **Chunk** via `rag_chunk "$file"` → JSONL on stdout.

4. **Embed each chunk** — loop over the JSONL, call `rag_embed` for each `chunk_text`, attach the
   result as an `embedding` field. Build a fresh JSONL with the full row shape that matches the table:

   ```json
   {"collection":"wiki","vault_path":"concepts/rag.md","heading_path":"RAG > Chunking",
    "chunk_index":3,"chunk_text":"...","embedding":[0.01,...],
    "token_count":420,"content_hash":"abc...","tags":["rag","nlp"]}
   ```

5. **Insert** via JSONEachRow:
   ```bash
   curl -sS "$CLICKHOUSE_URL/?database=$CLICKHOUSE_DATABASE&query=INSERT+INTO+rag_chunks+FORMAT+JSONEachRow" \
     ${CLICKHOUSE_USER:+-u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD"} \
     --data-binary @chunks-with-embeddings.jsonl
   ```

6. **Update the manifest** — set `rag_indexed_hash` and `rag_chunk_count` for this file.

Batch embedding calls are preferred for OpenAI (up to 2048 inputs per call, much cheaper) — if the user
has a large vault, use the batch form instead of per-chunk calls. See
`references/embedding-batching.md`.

## Step 7: Log and Report

After all files in the scope are processed, append to `$OBSIDIAN_VAULT_PATH/log.md`:

```
- [ISO8601_TIMESTAMP] RAG_INDEX collection=wiki files_scanned=N files_indexed=M chunks_written=K provider=openai model=text-embedding-3-small dims=1536 duration=Xs
```

Then tell the user:
- How many files were scanned vs. reindexed (delta vs. full)
- How many chunks were written
- Total duration and approximate cost (for OpenAI: dims × chunks × model-rate)
- Any files that failed to index (and why)

## Query Contract

Other skills (`wiki-query`, `wiki-ingest`) invoke this index via a short embed+SQL snippet. The canonical
form, reused by every consumer, is documented in `references/query-snippet.md`. If you change the table
schema here, update that file.

## Failure Modes

- **ClickHouse 404 or connection refused** — report and stop. Don't create a local SQLite fallback.
- **Embedding provider returns non-array** — log the raw response and skip the chunk, continue with
  others. Don't let a single bad chunk halt the run.
- **Dims mismatch** — if `rag_embed` returns a different dim count than `RAG_EMBEDDING_DIMS`, stop
  immediately. A mixed-dim table silently breaks vector search.
- **HNSW index build fails** — drop back to brute-force `cosineDistance`. Warn the user once.
