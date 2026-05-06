---
name: wiki-query
description: >
  Answer questions by searching the compiled Obsidian wiki. Use this skill when the user asks a question
  about their knowledge base, wants to find information across their wiki, asks "what do I know about X",
  "find everything related to Y", or wants synthesized answers with citations from their wiki pages.
  Also use when the user wants to explore connections between topics in their wiki. Works from any project.
  Includes an index-only fast mode triggered by "quick answer", "just scan", "don't read the pages",
  "fast lookup" — returns answers from page summaries and frontmatter without reading page bodies.
---

# Wiki Query — Knowledge Retrieval

You are answering questions against a compiled Obsidian wiki, not raw source documents. The wiki contains pre-synthesized, cross-referenced knowledge.

## Before You Start

1. Read `~/.obsidian-wiki/config` to get `OBSIDIAN_VAULT_PATH` (works from any project). Fall back to `.env` if you're inside the obsidian-wiki repo.
2. Read `$OBSIDIAN_VAULT_PATH/index.md` to understand the wiki's scope and structure

## Visibility Filter (optional)

By default, **all pages are returned** regardless of visibility tags. This preserves existing behavior — nothing changes unless the user asks for it.

If the user's query includes phrases like **"public only"**, **"user-facing"**, **"no internal content"**, **"as a user would see it"**, or **"exclude internal"**, activate **filtered mode**:

- Build a **blocked tag set**: `{visibility/internal, visibility/pii}`
- In the Index Pass (Step 2), skip any candidate whose frontmatter tags contain a blocked tag
- In Section/Full Read passes (Steps 3–4), do not read or cite any blocked page
- Synthesize the answer **only from allowed pages** — do not mention that excluded pages exist

Pages with no `visibility/` tag, or tagged `visibility/public`, are always included.

In filtered mode, note the filter in the Step 6 log entry: `mode=filtered`.

## Retrieval Protocol

**Follow the Retrieval Primitives table in `llm-wiki/SKILL.md`.** Reading is the dominant cost of this skill — use the cheapest primitive that answers the question and escalate only when it can't. Never jump straight to full-page reads.

### Step 1: Understand the Question

Classify the query type:
- **Factual lookup** — "What is X?" → Find the relevant page(s)
- **Relationship query** — "How does X relate to Y?" → Find both pages and their cross-references
- **Synthesis query** — "What's the current thinking on X?" → Find all pages that touch X, synthesize
- **Gap query** — "What don't I know about X?" → Find what's missing, check open questions sections

Also decide the **mode**:
- **Index-only mode** — triggered by "quick answer", "just scan", "don't read the pages", "fast lookup". Stops at Step 3. Answers from frontmatter + `index.md` only.
- **Normal mode** — the full tiered pipeline below.

### Step 2: Index Pass (cheap)

Build a candidate set *without opening any page bodies*:

- You've already read `index.md` above — use it as the first filter. It lists every page with a one-line description and tags.
- Use `Grep` to scan page **frontmatter only** for title, tag, alias, and summary matches. A pattern like `^(title|tags|aliases|summary):` scoped to vault `.md` files is far cheaper than content grep.
- Collect the top 5–10 candidate page paths ranked by:
  1. Exact title or alias match
  2. Tag match
  3. Summary field contains the query term
  4. `index.md` entry contains the query term

If you're in **index-only mode**, stop here. Answer from `summary:` fields, titles, and `index.md` descriptions only. Label the answer clearly: **"(index-only answer — page bodies not read; facts below are from page summaries and may miss nuance)"**. Then skip to Step 5.

### Step 2a: ClickHouse RAG Semantic Pass (optional — requires `CLICKHOUSE_URL` in `.env`)

**GUARD: If `$CLICKHOUSE_URL` is empty or unset, skip this step and try Step 2b (QMD).**

> **No ClickHouse?** Skip to Step 2b. If QMD is also unavailable, skip to Step 3 and grep directly. See `.env.example` for ClickHouse + RAG setup, and run `wiki-rag-index` to populate the table.

If `CLICKHOUSE_URL` is set and the index pass didn't produce clear candidates — or the question requires semantic matching rather than exact terms — query the RAG table:

```bash
# See .skills/wiki-rag-index/references/query-snippet.md for the canonical form.
# Embed the question, then run hybrid vec+lex against rag_chunks.
QVEC=$(rag_embed "$QUESTION")
curl -sS "$CLICKHOUSE_URL/?database=$CLICKHOUSE_DATABASE" \
  ${CLICKHOUSE_USER:+-u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD"} \
  --data-binary "
    SELECT vault_path, heading_path, chunk_text,
           cosineDistance(embedding, $QVEC) AS dist, tags
    FROM rag_chunks
    WHERE collection = '${RAG_WIKI_COLLECTION:-wiki}'
    ORDER BY dist ASC
    LIMIT 10
    FORMAT JSON"
```

Run a parallel lexical query (`hasToken(lower(chunk_text), lower('<key-term>'))`) and merge by `vault_path`, boosting pages that appear in both result sets. See `wiki-rag-index/references/query-snippet.md` for the full merge recipe and the `rag_embed` helper.

The returned chunks act as pre-read section summaries. If they answer the question fully, skip Step 3 and go straight to Step 4 (reading only the pages ClickHouse ranked highest). Otherwise, use the ranked `vault_path` list to guide Step 3's grepping.

**Also search the `papers` collection when the question may have source material in `_raw/`:**

If `RAG_PAPERS_COLLECTION` is set and the user is asking about a topic likely covered by ingested papers (research, theory, background), run the same query with `collection = '$RAG_PAPERS_COLLECTION'` and cite raw sources separately from compiled wiki pages.

**Filtered mode:** when active, add `AND NOT has(tags, 'visibility/internal') AND NOT has(tags, 'visibility/pii')` to each WHERE clause.

**Stale index check:** if ClickHouse returns empty or very low-quality matches for a topic you're sure exists in the vault, the index may be stale. Suggest the user run `wiki-rag-index` and proceed with Step 2b/3 for now.

### Step 2b: QMD Semantic Pass (fallback — requires `QMD_WIKI_COLLECTION` in `.env`)

**GUARD: If Step 2a found good matches, skip this step. If `$QMD_WIKI_COLLECTION` is empty, skip to Step 3.**

> QMD is kept as a secondary semantic tier for setups that haven't migrated to ClickHouse RAG yet. New installs should prefer `wiki-rag-index`.

If `QMD_WIKI_COLLECTION` is set and neither the index pass nor ClickHouse produced clear candidates, use QMD:

```
mcp__qmd__query:
  collection: <QMD_WIKI_COLLECTION>
  intent: <the user's question>
  searches:
    - type: lex
      query: <key terms>
    - type: vec
      query: <question rephrased as a description>
```

The returned snippets act as pre-read section summaries. If they answer the question fully, skip Step 3 and go straight to Step 4. Otherwise, use the ranked file list to guide which files to grep or read in Step 3.

**Also search `papers` when the question may have source material in `_raw/`:** if `QMD_PAPERS_COLLECTION` is set and the topic is likely in ingested papers, run a parallel search against that collection.

### Step 3: Section Pass (medium cost — only if Steps 2/2a/2b are inconclusive)

For each of the top candidates, pull the relevant section *without reading the whole page*:

- Use `Grep -A 10 -B 2 "<query-term>" <candidate-file>` to get just the lines around the match.
- This usually returns 15–30 lines per hit instead of 100–500.
- If the section grep gives a clear answer, go straight to Step 5.

### Step 4: Full Read (expensive — last resort)

Only when Steps 2 and 3 don't answer the question:

- `Read` the top **3** candidates in full.
- Follow at most one hop of `[[wikilinks]]` from those pages if the answer requires cross-references.
- Check "Open Questions" sections for known gaps.
- If you're still short, **then** fall back to a broad content grep across the vault. Tell the user you escalated — this is the expensive path and they should know.

### Step 5: Synthesize an Answer

Compose your answer from wiki content:
- Cite specific wiki pages using `[[page-name]]` notation
- Note which step the answer came from ("found in summary" vs "grepped section" vs "full page read") — helps the user understand confidence
- If the wiki has contradictions, present both sides
- If the wiki doesn't cover something, say so explicitly
- Suggest which sources might fill the gap

### Step 6: Log the Query

Append to `log.md`:
```
- [TIMESTAMP] QUERY query="the user's question" result_pages=N mode=normal|index_only|filtered escalated=true|false
```

## Answer Format

Structure answers like this:

> **Based on the wiki:**
>
> [Your synthesized answer with [[wikilinks]] to source pages]
>
> **Pages consulted:** [[page-a]], [[page-b]], [[page-c]]
>
> **Gaps:** [What the wiki doesn't cover that might be relevant]
