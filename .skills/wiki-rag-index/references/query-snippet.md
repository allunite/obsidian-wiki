# ClickHouse RAG Query Snippet

Reused by `wiki-query`, `wiki-ingest`, `data-ingest`, and the history-ingest skills. This is the one
place where the ClickHouse query shape lives — if the schema in `SKILL.md` changes, update this file.

## Inputs

- `$QUESTION` — the user's natural-language query (or for ingest skills: the topic/thesis of the source)
- `$COLLECTION` — `"$RAG_WIKI_COLLECTION"` for compiled pages, `"$RAG_PAPERS_COLLECTION"` for raw sources
- `$TOP_K` — number of results to return (default 10; use 5 for fast paths)

## Guard

If `$CLICKHOUSE_URL` is empty, **skip this query entirely** and fall through to the next retrieval tier
(QMD if configured, otherwise Grep).

## Hybrid Lex + Vec Query

Run two queries and merge client-side. Keyword lookup catches exact names, file paths, and error
strings; vector lookup catches concepts and paraphrases.

```bash
# 1. Embed the question (see wiki-rag-index/SKILL.md Step 3 for the rag_embed function)
QVEC=$(rag_embed "$QUESTION")

# 2. Vector search (top K by cosine distance)
curl -sS "$CLICKHOUSE_URL/?database=$CLICKHOUSE_DATABASE" \
  ${CLICKHOUSE_USER:+-u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD"} \
  --data-binary "
    SELECT vault_path, heading_path, chunk_text,
           cosineDistance(embedding, $QVEC) AS dist,
           tags
    FROM rag_chunks
    WHERE collection = '$COLLECTION'
    ORDER BY dist ASC
    LIMIT $TOP_K
    FORMAT JSON" > /tmp/rag_vec.json

# 3. Lexical search (token bloom filter; fast substring-like match)
curl -sS "$CLICKHOUSE_URL/?database=$CLICKHOUSE_DATABASE" \
  ${CLICKHOUSE_USER:+-u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD"} \
  --data-binary "
    SELECT vault_path, heading_path, chunk_text, 0.0 AS dist, tags
    FROM rag_chunks
    WHERE collection = '$COLLECTION'
      AND hasToken(lower(chunk_text), lower('$LEX_TERM'))
    LIMIT $TOP_K
    FORMAT JSON" > /tmp/rag_lex.json
```

## Rank Merging

Deduplicate by `vault_path`, keeping the best (lowest `dist`) chunk for each page, and boost pages that
appear in both result sets:

```python
import json, collections
vec = json.load(open("/tmp/rag_vec.json"))["data"]
lex = json.load(open("/tmp/rag_lex.json"))["data"]
scores = collections.defaultdict(lambda: {"dist": 2.0, "chunk": None, "in_lex": False})
for r in vec:
    s = scores[r["vault_path"]]
    if r["dist"] < s["dist"]:
        s["dist"] = r["dist"]; s["chunk"] = r
for r in lex:
    s = scores[r["vault_path"]]
    s["in_lex"] = True
    if s["chunk"] is None: s["chunk"] = r
ranked = sorted(
    ({"path": p, **s} for p, s in scores.items()),
    key=lambda x: (x["dist"] - (0.1 if x["in_lex"] else 0.0))
)
```

## Visibility Filtering

When the caller is in **filtered mode** (e.g. "public only"), extend the WHERE clause:

```sql
AND NOT has(tags, 'visibility/internal')
AND NOT has(tags, 'visibility/pii')
```

## What to Do With the Results

The results are **pre-read section summaries**, not the final answer. The calling skill should:

1. Use `vault_path` to pick which pages to open in its next tier (section grep or full read).
2. Cite pages by converting `vault_path` to `[[page-name]]` (strip `.md`, last path segment).
3. Treat `chunk_text` as a confidence signal — if the chunks clearly answer the question, skip the
   next tier entirely.
