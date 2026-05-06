# Batched Embeddings (large-vault optimization)

The indexing loop in `SKILL.md` Step 6 embeds one chunk at a time. For large vaults (>500 files, >5k
chunks), this is slow and — for OpenAI — more expensive than it needs to be. Switch to batching.

## OpenAI

`/v1/embeddings` accepts an array for `input` and returns embeddings in the same order. Up to 2048
inputs per request; up to ~300k tokens per request. Group chunks into batches of ~100.

```bash
rag_embed_batch_openai() {
  # stdin: JSONL of {chunk_text, ...}; stdout: JSONL of {..., embedding: [...]}
  python3 - <<'PY'
import sys, json, os, urllib.request
MODEL = os.environ.get("RAG_EMBEDDING_MODEL", "text-embedding-3-small")
KEY = os.environ["OPENAI_API_KEY"]
BATCH = 100
rows = [json.loads(line) for line in sys.stdin]
for i in range(0, len(rows), BATCH):
    batch = rows[i:i+BATCH]
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=json.dumps({"model": MODEL, "input": [r["chunk_text"] for r in batch]}).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    for row, emb in zip(batch, resp["data"]):
        row["embedding"] = emb["embedding"]
        print(json.dumps(row, ensure_ascii=False))
PY
}
```

## Ollama

Ollama's `/api/embeddings` is single-prompt only in older versions, but `/api/embed` (newer) accepts
`input: [...]`. Check with `curl $OLLAMA_URL/api/version`.

## LM Studio

OpenAI-compatible — use the same batch shape as OpenAI against `$LMSTUDIO_URL/embeddings`.

## Cost Estimates (OpenAI, April 2026 pricing)

- `text-embedding-3-small` — $0.02 / 1M tokens
- Typical wiki page: ~500 tokens per chunk, ~3 chunks per page
- 1000 pages ≈ 1.5M tokens ≈ $0.03 for a full reindex

Delta reindex usually re-embeds <5% of chunks per run, so steady-state cost is negligible.
