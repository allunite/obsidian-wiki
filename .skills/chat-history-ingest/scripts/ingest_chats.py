"""
Google Chat ingest agent — drives a local LM Studio model to turn raw Google
Chat exports into merged markdown pages under wiki/chats/, following the
playbook in .skills/chat-history-ingest/SKILL.md.

Output contract (per SKILL.md):
  wiki/
    chats/
      <chapter>/                 # e.g. inventory, recalc, dashboards, campaigns
        <YYYYMM>-<topic>.md      # kebab-case; sessions merged by month+topic
        <YYYYMM>-<topic>-2.md    # split when a single file exceeds ~10 KB
    chat-index.md                # catalog of all chat files, grouped by chapter
    .ingest-state.json           # checkpoint, lets the run be resumed mid-way

Pipeline:
  1. Walk raw/Google Chat/Groups/<chat-id>/group_info.json.
  2. Apply exclusions (space names / DM counterparties / pre-2025 dates) — bail
     BEFORE opening messages.json where possible.
  3. For survivors, load messages.json, strip credentials, drop pre-2025
     messages, segment into sessions by idle-gap, drop trivial ones.
  4. For each remaining session, call LM Studio (OpenAI-compatible) and ask
     for a strict JSON object: topic, topic_slug, chapter, tags, body_markdown,
     decisions, action_items, skip.
  5. Merge the produced section into the right
     wiki/chats/<chapter>/<YYYYMM>-<topic>.md file, splitting if it would
     overflow the size budget. Refresh wiki/chat-index.md.
  6. Checkpoint progress every ~20 written sessions (and on Ctrl-C / errors)
     so a long run can be resumed from where it left off.
"""

from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import time
import urllib.request
import urllib.error
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Playbook constants — kept in code, not config, because changing them alters
# privacy / scope guarantees and should go through review.
# ---------------------------------------------------------------------------

ME_EMAIL = "aka@allunite.com"

EXCLUDED_SPACE_NAMES = {
    "We Are The Robots",
    "Status",
    "Shit Happened",
    "Tower",
    "NOTES",
    "Claude",
    "Кабаны",
}

# DMs where the *other* member is any of these are skipped.
EXCLUDED_DM_COUNTERPARTS = {
    "Esben Elmoe",
    "Deeksha Priyani",
}

# Bot/automation accounts we never count as participants and whose messages
# we drop before segmentation. Compared case-insensitively against the chat
# member name (group_info.json) and the message creator name (messages.json).
EXCLUDED_AUTHORS = {
    "github",
}

# Anything dated before this point is dropped (per SKILL.md and per user
# directive: start from 2025-01-01).
EARLIEST_DATE = datetime(2025, 1, 1, tzinfo=timezone.utc)

# Credentials / secrets we never want to forward to the LLM or write to disk.
SECRET_PATTERNS = [
    re.compile(r"\b[A-Za-z0-9+/]{32,}={0,2}\b"),           # long base64-ish
    re.compile(r"\b(sk|pk|rk|xox[abpr])[-_][A-Za-z0-9\-_]{16,}\b"),
    re.compile(r"\b[A-Za-z0-9]{20,}\.[A-Za-z0-9]{20,}\.[A-Za-z0-9_\-]{20,}\b"),  # JWT-ish
    re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key|bearer)\s*[:=]\s*\S+"),
    re.compile(r"postgres(?:ql)?://[^\s]+"),
    re.compile(r"mongodb(?:\+srv)?://[^\s]+"),
    re.compile(r"https?://[^\s]*[?&](?:key|token|secret|sig)=\S+"),
]

DATE_FMT = "%A, %d %B %Y at %H:%M:%S %Z"     # "Friday, 18 March 2022 at 08:45:53 UTC"

SESSION_GAP = timedelta(hours=4)              # idle threshold = new session
MIN_SESSION_MESSAGES = 3                      # below this, not worth extracting
MAX_SESSION_MESSAGES = 120                    # cap to keep prompts small

# A YYYYMM+topic file overflowing this size triggers a -2/-3 split (per SKILL).
# Set high so concepts collapse into one fat page per topic-month — the goal is
# hundreds of pages total, not thousands of one-session shards.
MAX_FILE_BYTES = 50 * 1024

# Checkpoint cadence — write state to disk after this many new session sections.
CHECKPOINT_EVERY = 20

# Default LM Studio model identifier. Override with --model on the CLI.
DEFAULT_MODEL = "google/gemma-4-e2b"

# Allowed chapter slugs. The LLM is instructed to pick one; anything else falls
# back to "misc". Keep this list in sync with the system prompt.
ALLOWED_CHAPTERS = {
    "inventory",
    "recalc",
    "dashboards",
    "campaigns",
    "analytics",
    "mops",
    "data-science",
    "infra",
    "ops",
    "clients",
    "releases",
    "misc",
}

WIKI_ROOT = Path(__file__).parent / "wiki"
RAW_ROOT = Path(__file__).parent / "raw" / "Google Chat" / "Groups"
CHATS_OUT = WIKI_ROOT / "chats"
INDEX_PATH = WIKI_ROOT / "chat-index.md"
STATE_PATH = WIKI_ROOT / ".ingest-state.json"


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Member:
    name: str
    email: str = ""
    is_me: bool = False


@dataclass
class Group:
    chat_id: str                  # the folder name, minus "DM "/"Space " prefix
    folder: Path
    kind: str                     # "DM" | "Space"
    space_name: str | None        # None for DMs
    members: list[Member]

    @property
    def participant_names(self) -> list[str]:
        names = [m.name for m in self.members
                 if m.name and m.name.strip().lower() not in EXCLUDED_AUTHORS]
        return names or ["(unknown)"]

    @property
    def display_label(self) -> str:
        """Bold-able label used in section headings."""
        if self.kind == "Space":
            return f"Space: {self.space_name or self.chat_id}"
        # DM: identify by the *other* party so the heading is informative.
        others = [m.name for m in self.members
                  if not m.is_me and m.name
                  and m.name.strip().lower() not in EXCLUDED_AUTHORS]
        if others:
            return f"DM with {', '.join(others)}"
        return "DM"


@dataclass
class Session:
    index: int                    # 1-based position within the group
    start: datetime
    end: datetime
    messages: list[dict] = field(default_factory=list)

    @property
    def date_str(self) -> str:
        return self.start.strftime("%Y-%m-%d")

    @property
    def yyyymm(self) -> str:
        return self.start.strftime("%Y%m")


# ---------------------------------------------------------------------------
# Loading + exclusion
# ---------------------------------------------------------------------------


def load_group(folder: Path) -> Group | None:
    """Read group_info.json and decide kind. Returns None if malformed."""
    info_path = folder / "group_info.json"
    if not info_path.exists():
        return None
    try:
        info = json.loads(info_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    raw_members = info.get("members", []) or []
    members = [
        Member(
            name=(m.get("name") or "").strip(),
            email=(m.get("email") or "").strip().lower(),
            is_me=(m.get("email") or "").strip().lower() == ME_EMAIL,
        )
        for m in raw_members
    ]

    name = folder.name
    if name.startswith("DM "):
        chat_id = name[3:]
        return Group(chat_id=chat_id, folder=folder, kind="DM",
                     space_name=None, members=members)
    if name.startswith("Space "):
        chat_id = name[6:]
        return Group(chat_id=chat_id, folder=folder, kind="Space",
                     space_name=(info.get("name") or "").strip() or None,
                     members=members)
    # Unknown prefix — skip rather than guess.
    return None


def should_exclude(group: Group) -> tuple[bool, str]:
    """Apply the playbook's hard exclusions. Returns (excluded, reason)."""
    if group.kind == "Space":
        if group.space_name and group.space_name in EXCLUDED_SPACE_NAMES:
            return True, f"excluded space name: {group.space_name}"
    else:  # DM
        others = [m for m in group.members if not m.is_me]
        for m in others:
            if m.name in EXCLUDED_DM_COUNTERPARTS:
                return True, f"excluded DM counterpart: {m.name}"
    return False, ""


# ---------------------------------------------------------------------------
# Redaction — credentials only. Per the user's directive, participant names
# are NOT scrubbed; the wiki keeps them verbatim.
# ---------------------------------------------------------------------------


def redact_secrets(text: str) -> str:
    if not text:
        return ""
    for pat in SECRET_PATTERNS:
        text = pat.sub("[redacted]", text)
    return text


# ---------------------------------------------------------------------------
# Session segmentation
# ---------------------------------------------------------------------------


def parse_chat_date(s: str) -> datetime | None:
    """Parse 'Friday, 18 March 2022 at 08:45:53 UTC' → aware datetime."""
    try:
        dt = datetime.strptime(s, DATE_FMT)
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def load_messages(group: Group) -> list[dict]:
    """Load + scrub-credentials messages. Returns dicts of {at, author, text}.

    Drops anything dated before EARLIEST_DATE per SKILL.md.
    """
    path = group.folder / "messages.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    out: list[dict] = []
    for m in data.get("messages", []):
        ts = parse_chat_date(m.get("created_date", "") or "")
        if ts is None or ts < EARLIEST_DATE:
            continue
        creator = m.get("creator") or {}
        author = (creator.get("name") or "").strip() or "(unknown)"
        if author.strip().lower() in EXCLUDED_AUTHORS:
            # Bot/automation noise (e.g. GitHub PR notifications) — drop the
            # message so it neither shows up as a participant nor pollutes
            # the LLM context.
            continue
        text = redact_secrets(m.get("text") or "")
        if not text.strip():
            continue
        out.append({"at": ts, "author": author, "text": text})

    out.sort(key=lambda x: x["at"])
    return out


def split_into_sessions(messages: list[dict]) -> list[Session]:
    """Split by idle gap. Each session keeps full messages."""
    sessions: list[Session] = []
    current: list[dict] = []
    idx = 0

    def flush() -> None:
        nonlocal idx, current
        if not current:
            return
        idx += 1
        sessions.append(Session(
            index=idx,
            start=current[0]["at"],
            end=current[-1]["at"],
            messages=current,
        ))
        current = []

    for msg in messages:
        if not current:
            current = [msg]
            continue
        if msg["at"] - current[-1]["at"] > SESSION_GAP:
            flush()
            current = [msg]
        else:
            current.append(msg)
    flush()
    return [s for s in sessions if len(s.messages) >= MIN_SESSION_MESSAGES]


# ---------------------------------------------------------------------------
# LM Studio call
# ---------------------------------------------------------------------------


# JSON Schema for LM Studio's Structured Outputs (response_format=json_schema).
# LM Studio grammar-constrains the model to this schema, so malformed output
# is not possible on supported loaders (llama.cpp / MLX).
EXTRACTION_SCHEMA = {
    "name": "chat_session_extraction",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "topic", "topic_slug", "chapter", "tags",
            "body_markdown", "decisions", "action_items",
            "skip", "skip_reason",
        ],
        "properties": {
            "topic":         {"type": "string"},
            "topic_slug":    {"type": "string"},
            "chapter":       {"type": "string"},
            "tags":          {"type": "array", "items": {"type": "string"}},
            "body_markdown": {"type": "string"},
            "decisions":     {"type": "array", "items": {"type": "string"}},
            "action_items":  {"type": "array", "items": {"type": "string"}},
            "skip":          {"type": "boolean"},
            "skip_reason":   {"type": "string"},
        },
    },
}


SYSTEM_PROMPT = """You are a strict extraction engine for a personal Obsidian wiki at AllUnite (a Digital Out-of-Home advertising analytics company).

Your input is a Google Chat session with real participant names. Names are NOT redacted — keep them as-is when they actually carry information (decision owners, drivers of an action, etc.). The summary should still be about TOPICS AND DECISIONS, not "X said, Y said", so use names sparingly. Credentials and secret URLs already appear as [redacted] — never echo them.

YOUR PRIMARY JOB IS TO REJECT EPHEMERAL CHATTER. Default to skip. Only keep a session if it carries CONCEPTUAL, DURABLE knowledge — something a future-you would want to know about how AllUnite *works* or *why a decision was made*. This includes:
- How a system behaves (recalc, MOPS, ml_traffic_prediction, ClickHouse pipelines, etc.)
- The reasoning behind a non-trivial decision (architecture, data model, methodology, naming, scope)
- Domain rules / business logic (visibility adjustment, dwell time methodology, calibration, sessionization)
- Postmortems, root causes, debugging insights with lasting value
- Definitions, conventions, contracts between systems

SKIP (set "skip": true) when the session is dominated by:
- Logistics: "let's not release today", "moved the deploy to tomorrow", "let's call at 3", "I'm late", scheduling, calendar coordination
- Status pings: "done", "merged", "deployed", "approved", "looks good", "I'm out for lunch", OOO, vacation, sick leave
- One-off file or link sharing without substantive discussion
- Greetings, congratulations, banter, jokes, condolences
- Personal coordination (lunch, transport, who is in the office)
- Mere ticket/PR cross-posting without added reasoning
- Generic acknowledgements
The bar is high: if you cannot articulate one concrete, durable concept the session teaches, set skip: true with a one-phrase reason.

Your output is a SINGLE JSON object matching this schema (no prose, no markdown fences):

{
  "topic":         "VERY BROAD topic phrase, 1-3 generic words. Pick the most general label that still describes the conversation, so MANY sessions in this chapter collapse into the SAME page. Good: 'recalc', 'inventory issues', 'campaigns', 'dashboards', 'release planning', 'JoeAndTheJuice', 'data pipelines'. Bad (too narrow): 'fix off-by-one in March recalc query', 'march dashboard widget bug', 'frame 12345 coordinate fix'. The wiki should grow to HUNDREDS of fat pages — not thousands of narrow shards. If unsure, pick the broader option.",
  "topic_slug":    "kebab-case slug derived from topic, max ~20 chars, no dates, no incident-specifics, no version numbers",
  "chapter":       "ONE OF: inventory, recalc, dashboards, campaigns, analytics, mops, data-science, infra, ops, clients, releases, misc",
  "tags":          ["lowercase kebab-case tags drawn from AllUnite vocabulary: facility, frame, insertion, loop, loop-duration, impression, campaign, inventory, dwell-time, session, mops, analytics, joe-and-the-juice, recalc-ch, etc. Only include tags clearly supported by the conversation."],
  "body_markdown": "Dense factual markdown FOCUSED ON CONCEPTS. Capture: how the system behaves, why a decision was made, definitions, constraints, root causes. Drop scheduling, status, who-said-what. Generic markdown (paragraphs and bullets); do NOT add headings — the host file supplies them. No emojis, no tone filler.",
  "decisions":     ["concrete decisions with LASTING consequences, one per string, short. Skip ephemeral ones like 'release tomorrow instead of today' unless the reason itself is a durable constraint."],
  "action_items":  ["concrete follow-ups that change a system or document, one per string, short. Skip 'I'll call you back', 'will check tomorrow'."],
  "skip":          false,
  "skip_reason":   ""
}

Rules:
- Generalize aggressively: prefer a topic that already exists in spirit over inventing a new narrow one. The wiki should grow HUNDREDS of fat pages, not THOUSANDS of one-session files.
- When in doubt between two topic granularities, pick the broader one.
- Never echo credentials, tokens, or URLs containing secrets.
- Do not copy specific revenue, margin, or other finance figures verbatim — bucket them ("mid-six-figures", "double-digit growth") or omit.
- Client-company names (e.g., Joe&TheJuice) and team names ARE allowed.
- Output MUST be a single valid JSON object and nothing else.
"""


def build_user_prompt(group: Group, session: Session) -> str:
    header = (
        f"Chat kind: {group.kind}\n"
        f"Space name: {group.space_name or 'N/A (DM)'}\n"
        f"Participants: {', '.join(group.participant_names)}\n"
        f"Date range: {session.start.date()} → {session.end.date()}\n"
        f"Messages: {len(session.messages)}\n"
        "----- BEGIN SESSION -----\n"
    )
    # Keep only the most recent MAX_SESSION_MESSAGES to stay within context.
    msgs = session.messages[-MAX_SESSION_MESSAGES:]
    body = "\n".join(
        f"[{m['at'].strftime('%Y-%m-%d %H:%M')}] {m['author']}: {m['text']}"
        for m in msgs
    )
    return header + body + "\n----- END SESSION -----"


def call_lm_studio(endpoint: str, model: str, system: str, user: str,
                   timeout: int = 300) -> dict:
    """POST to /v1/chat/completions; parse JSON from assistant content."""
    url = endpoint.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_schema", "json_schema": EXTRACTION_SCHEMA},
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        # LM Studio returns a JSON error body with the real reason
        # (wrong model id, unsupported response_format, etc.). Surface it.
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise RuntimeError(
            f"LM Studio HTTP {e.code} at {url}: {body[:800] or e.reason}"
        ) from None
    data = json.loads(raw)
    content = data["choices"][0]["message"]["content"]
    # Be forgiving: some models wrap JSON in ```json fences despite response_format.
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.S)
    return json.loads(content)


# ---------------------------------------------------------------------------
# Output: chapter routing, page merging, splitting, index
# ---------------------------------------------------------------------------


_KEBAB_RE = re.compile(r"[^a-z0-9]+")


def kebab(s: str) -> str:
    s = (s or "").lower().strip()
    s = _KEBAB_RE.sub("-", s).strip("-")
    return s or "session"


def normalize_chapter(raw: str) -> str:
    c = kebab(raw)
    return c if c in ALLOWED_CHAPTERS else "misc"


def page_path(chapter: str, yyyymm: str, topic_slug: str, suffix: int) -> Path:
    base = f"{yyyymm}-{topic_slug}"
    if suffix > 1:
        base = f"{base}-{suffix}"
    return CHATS_OUT / chapter / f"{base}.md"


def find_target_page(chapter: str, yyyymm: str, topic_slug: str) -> Path:
    """
    Pick the next page file to append to: the highest existing -N suffix
    that's still under MAX_FILE_BYTES, or a fresh suffix if all are full or
    none exist.
    """
    suffix = 1
    last_existing: Path | None = None
    while True:
        path = page_path(chapter, yyyymm, topic_slug, suffix)
        if not path.exists():
            return last_existing or path
        if path.stat().st_size < MAX_FILE_BYTES:
            return path
        last_existing = path
        suffix += 1


def render_frontmatter(topic: str, tags: list[str], sources: list[str],
                       updated: str) -> str:
    """Minimal frontmatter — title, tags, sources, updated, status only.

    Per user directive: no `type: chat-page`, no `chapter`, no `date_range`,
    no duplicated H1, no chat-id metadata in the body.
    """
    merged_tags = sorted({"chat", *(t for t in tags if t)})
    tag_field = "[" + ", ".join(merged_tags) + "]"
    src_field = "[" + ", ".join(sorted({s for s in sources if s})) + "]"
    return (
        "---\n"
        f"title: {topic}\n"
        f"tags: {tag_field}\n"
        f"sources: {src_field}\n"
        f"updated: {updated}\n"
        "status: active\n"
        "---\n\n"
    )


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (fields, body). Fields are best-effort flat key:value strings."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fields[k.strip()] = v.strip()
    return fields, body


def update_frontmatter(existing: str, *, tags: list[str], sources: list[str],
                       updated: str) -> str:
    """Refresh tags/sources/updated on an existing page. Body untouched."""
    fields, body = parse_frontmatter(existing)

    def merge_list(field_name: str, new_values: list[str]) -> str:
        current = fields.get(field_name, "")
        existing_items = [t.strip() for t in
                          current.strip("[]").split(",") if t.strip()]
        merged = sorted(set(existing_items) | set(new_values))
        return "[" + ", ".join(merged) + "]"

    fields["tags"] = merge_list("tags", ["chat", *tags])
    fields["sources"] = merge_list("sources", sources)
    fields["updated"] = updated

    rebuilt = ["---"]
    order = ["title", "tags", "sources", "updated", "status"]
    seen: set[str] = set()
    for k in order:
        if k in fields:
            rebuilt.append(f"{k}: {fields[k]}")
            seen.add(k)
    for k, v in fields.items():
        if k not in seen:
            rebuilt.append(f"{k}: {v}")
    rebuilt.append("---\n")
    return "\n".join(rebuilt) + body


def render_session_section(group: Group, session: Session,
                           extracted: dict) -> str:
    """A single session, rendered as a markdown section to append.

    Per user directive: no chat-id line. Section header carries the bold
    space-or-DM label, the kind, the participant names, the date range, and
    the long topic.
    """
    label = group.display_label
    body_md = (extracted.get("body_markdown") or "").strip()
    decisions = [d for d in (extracted.get("decisions") or []) if d.strip()]
    actions = [a for a in (extracted.get("action_items") or []) if a.strip()]
    long_topic = (extracted.get("topic") or "").strip()
    participants = ", ".join(group.participant_names)
    date_lo = session.start.strftime("%Y-%m-%d")
    date_hi = session.end.strftime("%Y-%m-%d")

    lines: list[str] = []
    lines.append(f"## **{label}** — {date_lo} → {date_hi}")
    lines.append("")
    meta = [f"**kind:** `{group.kind}`",
            f"**participants:** {participants}"]
    if long_topic:
        meta.append(f"**topic:** {long_topic}")
    lines.append(" · ".join(meta))
    lines.append("")
    if body_md:
        lines.append(body_md)
        lines.append("")
    if decisions:
        lines.append("**Decisions**")
        lines.append("")
        for d in decisions:
            lines.append(f"- {d}")
        lines.append("")
    if actions:
        lines.append("**Action items**")
        lines.append("")
        for a in actions:
            lines.append(f"- {a}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n\n"


def append_session(chapter: str, yyyymm: str, topic_slug: str,
                   topic_long: str, group: Group, session: Session,
                   extracted: dict) -> Path:
    """Append a session into the right page, creating/splitting as needed."""
    target = find_target_page(chapter, yyyymm, topic_slug)
    target.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tags = list(extracted.get("tags") or [])
    sources = [group.chat_id]

    section = render_session_section(group, session, extracted)

    if not target.exists():
        header = render_frontmatter(
            topic=topic_long, tags=tags, sources=sources, updated=today,
        )
        target.write_text(header + section, encoding="utf-8")
        return target

    existing = target.read_text(encoding="utf-8")
    # If appending would push the file over budget, roll over to the next
    # suffix instead — but only if the file already has at least one section
    # (otherwise we'd refuse to write anything for an enormous single section).
    projected_size = len(existing.encode("utf-8")) + len(section.encode("utf-8"))
    if projected_size > MAX_FILE_BYTES and existing.count("\n## ") >= 1:
        m = re.match(rf"{re.escape(yyyymm)}-{re.escape(topic_slug)}(?:-(\d+))?\.md$",
                     target.name)
        cur = int(m.group(1)) if (m and m.group(1)) else 1
        next_path = page_path(chapter, yyyymm, topic_slug, cur + 1)
        next_path.parent.mkdir(parents=True, exist_ok=True)
        header = render_frontmatter(
            topic=topic_long, tags=tags, sources=sources, updated=today,
        )
        next_path.write_text(header + section, encoding="utf-8")
        return next_path

    refreshed = update_frontmatter(
        existing, tags=tags, sources=sources, updated=today,
    )
    target.write_text(refreshed.rstrip() + "\n\n" + section, encoding="utf-8")
    return target


# ---------------------------------------------------------------------------
# Catalog: chat-index.md, regenerated from disk after every run
# ---------------------------------------------------------------------------


def rebuild_index() -> None:
    """Walk wiki/chats/<chapter>/*.md and (re)write a chapter-grouped index."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    by_chapter: dict[str, list[tuple[str, dict]]] = {}

    if CHATS_OUT.exists():
        for chapter_dir in sorted(p for p in CHATS_OUT.iterdir() if p.is_dir()):
            chapter = chapter_dir.name
            for md in sorted(chapter_dir.glob("*.md")):
                try:
                    text = md.read_text(encoding="utf-8")
                except OSError:
                    continue
                fields, _ = parse_frontmatter(text)
                rel = md.relative_to(WIKI_ROOT).as_posix()
                by_chapter.setdefault(chapter, []).append((rel, fields))

    lines: list[str] = []
    lines.append("---")
    lines.append("title: Chat Index")
    lines.append("type: overview")
    lines.append("tags: [chat, google-chat]")
    lines.append("sources: []")
    lines.append(f"updated: {today}")
    lines.append("status: active")
    lines.append("---")
    lines.append("")
    lines.append("# Chat Index")
    lines.append("Catalog of included Google Chat Groups. Excluded chats not listed.")
    lines.append(
        'Excluded: spaces named "We Are The Robots", "Status", "Shit Happened", '
        '"Tower", "NOTES", "Claude", "Кабаны"; DMs with excluded members.'
    )
    lines.append("")

    if not by_chapter:
        lines.append("_No chat pages ingested yet._")
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    for chapter in sorted(by_chapter):
        pretty = chapter.replace("-", " ").title()
        lines.append(f"## {pretty}")
        lines.append("")
        for rel, fields in by_chapter[chapter]:
            # The filename stem already encodes the topic (YYYYMM-topic-slug),
            # so the index is just a link plus tags — no separate topic field.
            stem = Path(rel).stem
            tags = fields.get("tags", "").strip("[]")
            tag_str = f" — tags: {tags}" if tags else ""
            lines.append(f"- [{stem}]({rel}){tag_str}")
        lines.append("")

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Checkpoint state — resumable runs
# ---------------------------------------------------------------------------


@dataclass
class State:
    completed_sessions: set[str] = field(default_factory=set)  # "chat_id::idx"
    completed_groups: set[str] = field(default_factory=set)
    total_written: int = 0
    last_saved_at: str = ""

    @staticmethod
    def session_key(chat_id: str, session_index: int) -> str:
        return f"{chat_id}::{session_index}"

    def has(self, chat_id: str, session_index: int) -> bool:
        return self.session_key(chat_id, session_index) in self.completed_sessions

    def mark(self, chat_id: str, session_index: int) -> None:
        self.completed_sessions.add(self.session_key(chat_id, session_index))


def load_state() -> State:
    if not STATE_PATH.exists():
        return State()
    try:
        raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return State()
    return State(
        completed_sessions=set(raw.get("completed_sessions") or []),
        completed_groups=set(raw.get("completed_groups") or []),
        total_written=int(raw.get("total_written") or 0),
        last_saved_at=raw.get("last_saved_at") or "",
    )


def save_state(state: State, *, reason: str) -> None:
    state.last_saved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "completed_sessions": sorted(state.completed_sessions),
        "completed_groups": sorted(state.completed_groups),
        "total_written": state.total_written,
        "last_saved_at": state.last_saved_at,
    }
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    tmp.replace(STATE_PATH)
    print(
        f"[checkpoint] {reason}: {state.total_written} sessions written, "
        f"{len(state.completed_sessions)} session keys, "
        f"{len(state.completed_groups)} groups complete "
        f"→ {STATE_PATH.relative_to(WIKI_ROOT.parent).as_posix()}"
    )


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def discover_groups(limit: int | None, only: str | None) -> Iterable[Group]:
    if not RAW_ROOT.exists():
        print(f"raw root not found: {RAW_ROOT}", file=sys.stderr)
        return []
    folders = sorted([p for p in RAW_ROOT.iterdir() if p.is_dir()])
    yielded = 0
    for folder in folders:
        group = load_group(folder)
        if group is None:
            continue
        if only and group.chat_id != only:
            continue
        yield group
        yielded += 1
        if limit and yielded >= limit:
            return


def run(args: argparse.Namespace) -> None:
    CHATS_OUT.mkdir(parents=True, exist_ok=True)

    if args.reset and STATE_PATH.exists():
        STATE_PATH.unlink()
        print(f"[reset] removed {STATE_PATH}")
    state = load_state()
    if state.completed_sessions:
        print(
            f"[resume] loaded checkpoint from {state.last_saved_at or '(unknown)'}: "
            f"{state.total_written} sessions previously written, "
            f"{len(state.completed_sessions)} session keys, "
            f"{len(state.completed_groups)} groups complete"
        )

    ingested = 0
    created = 0
    excluded = 0
    skipped = 0
    errors = 0
    pages_touched: set[Path] = set()
    sessions_since_checkpoint = 0

    # Ctrl-C → save state and exit cleanly. We let SIGTERM flow through too.
    interrupted = {"flag": False}

    def _on_signal(signum, frame):
        interrupted["flag"] = True
        print(f"\n[signal] caught {signum}, will checkpoint and stop "
              "after the current session …")

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _on_signal)
        except (ValueError, OSError):
            pass  # not in main thread / unsupported on platform

    try:
        for group in discover_groups(args.limit, args.only):
            ingested += 1
            if group.chat_id in state.completed_groups:
                print(f"[done] {group.folder.name}: already completed in a "
                      "prior run, skipping")
                continue
            exclude, reason = should_exclude(group)
            if exclude:
                excluded += 1
                print(f"[skip] {group.folder.name}: {reason}")
                continue

            messages = load_messages(group)
            if not messages:
                skipped += 1
                state.completed_groups.add(group.chat_id)
                print(f"[empty] {group.folder.name}: no usable messages")
                continue

            sessions = split_into_sessions(messages)
            if not sessions:
                skipped += 1
                state.completed_groups.add(group.chat_id)
                print(f"[thin] {group.folder.name}: no sessions of "
                      f">= {MIN_SESSION_MESSAGES} messages")
                continue

            print(f"[work] {group.folder.name}: "
                  f"{len(messages)} msg → {len(sessions)} session(s)")

            all_done_for_group = True
            for session in sessions:
                if interrupted["flag"]:
                    break
                if state.has(group.chat_id, session.index):
                    continue

                user_prompt = build_user_prompt(group, session)
                if args.dry_run:
                    print(f"  -> session {session.index} "
                          f"({session.date_str}, {len(session.messages)} msg) "
                          "[dry-run: not calling LLM]")
                    continue

                try:
                    extracted = call_lm_studio(
                        args.endpoint, args.model, SYSTEM_PROMPT, user_prompt
                    )
                except (urllib.error.URLError, urllib.error.HTTPError,
                        json.JSONDecodeError, KeyError, TimeoutError,
                        RuntimeError) as e:
                    errors += 1
                    all_done_for_group = False
                    print(f"  !! session {session.index}: LLM error: {e}")
                    continue

                if extracted.get("skip"):
                    skipped += 1
                    state.mark(group.chat_id, session.index)
                    print(f"  -- session {session.index} skipped by LLM: "
                          f"{extracted.get('skip_reason', '')}")
                    continue

                topic_long = (extracted.get("topic") or "").strip() \
                    or f"session {session.index}"
                # Cap at 25 chars to discourage over-specific slugs and let
                # broader topics naturally collapse into the same page.
                topic_slug = kebab(extracted.get("topic_slug") or topic_long)[:25]
                chapter = normalize_chapter(extracted.get("chapter") or "misc")

                try:
                    page = append_session(
                        chapter=chapter,
                        yyyymm=session.yyyymm,
                        topic_slug=topic_slug,
                        topic_long=topic_long,
                        group=group,
                        session=session,
                        extracted=extracted,
                    )
                except OSError as e:
                    errors += 1
                    all_done_for_group = False
                    print(f"  !! session {session.index}: write error: {e}")
                    continue

                pages_touched.add(page)
                created += 1
                state.mark(group.chat_id, session.index)
                state.total_written += 1
                sessions_since_checkpoint += 1
                print(f"  ++ session {session.index} -> "
                      f"{page.relative_to(WIKI_ROOT).as_posix()}")

                if sessions_since_checkpoint >= CHECKPOINT_EVERY:
                    save_state(state,
                               reason=f"every {CHECKPOINT_EVERY} sessions")
                    sessions_since_checkpoint = 0

                if args.sleep_ms:
                    time.sleep(args.sleep_ms / 1000.0)

            if not args.dry_run and all_done_for_group and not interrupted["flag"]:
                state.completed_groups.add(group.chat_id)

            if interrupted["flag"]:
                break
    finally:
        # Always save what we have, whether the run finished cleanly or was
        # interrupted by a signal / unhandled exception.
        if not args.dry_run:
            save_state(state, reason="end of run" if not interrupted["flag"]
                       else "interrupted, saving before exit")
            rebuild_index()

    print(
        "\nIngested: {n} raw files\n"
        "Created: {m} chat sessions\n"
        "Pages touched: {p}\n"
        "Excluded: {e} items (chats/drafts)\n"
        "Skipped (thin/empty/LLM-skip): {s}\n"
        "Errors: {err}\n"
        "Checkpoint: {cp}".format(
            n=ingested, m=created, p=len(pages_touched),
            e=excluded, s=skipped, err=errors,
            cp=STATE_PATH.relative_to(WIKI_ROOT.parent).as_posix(),
        )
    )
    if interrupted["flag"]:
        # Convey "stopped early" to a shell caller. State on disk is fine.
        sys.exit(130)


# ---------------------------------------------------------------------------
# Consolidation: collapse narrow per-incident topics into broad canonical pages
# ---------------------------------------------------------------------------

# Target ceiling: at most this many distinct topic slugs per (chapter, yyyymm).
# When the directory has more, the LLM is asked to canonicalize them down.
MAX_TOPICS_PER_MONTH = 4
# Don't bother running the LLM if a chapter+month has fewer files than this.
MIN_FILES_TO_CONSOLIDATE = 4

CONSOLIDATE_SCHEMA = {
    "name": "topic_canonicalization",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["mapping"],
        "properties": {
            "mapping": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["from", "canonical"],
                    "properties": {
                        "from":      {"type": "string"},
                        "canonical": {"type": "string"},
                    },
                },
            },
        },
    },
}

CONSOLIDATE_SYSTEM = """You are consolidating an Obsidian wiki of Google Chat sessions at AllUnite (a Digital Out-of-Home advertising analytics company).

Your job: relabel narrow per-incident kebab-case topic slugs into BROAD canonical slugs, so dozens of files in a chapter+month collapse into a small handful.

Input: a JSON object with the chapter, the YYYYMM, a max canonical count, and a list of current slugs.

Output: a SINGLE JSON object with a "mapping" array. Each entry maps one input slug to a canonical broad slug.

Hard constraints:
- The set of distinct canonical values in your output MUST contain at most max_canonical entries.
- Canonical slugs are 1-3 generic kebab-case words, max 20 characters, drawn from the AllUnite domain (e.g. recalc, inventory, dashboards, campaigns, releases, joe-and-the-juice, data-pipelines, mops, infra). A slug may map to itself if it is already canonical.
- NO dates, version numbers, person names, or incident-specifics in canonical slugs.
- EVERY input slug must appear exactly once in the mapping.
- Output MUST be a single valid JSON object and nothing else."""


_SECTION_SPLIT_RE = re.compile(r"(?m)^(?=## \*\*)")


def parse_sections(body: str) -> list[str]:
    """Split a page body into individual chat-session sections."""
    parts = _SECTION_SPLIT_RE.split(body)
    return [p.strip() for p in parts if p.strip().startswith("## **")]


def _list_field(value: str) -> set[str]:
    return {t.strip() for t in (value or "").strip("[]").split(",") if t.strip()}


def call_lm_studio_canonicalize(endpoint: str, model: str, slugs: list[str],
                                 chapter: str, yyyymm: str,
                                 max_canonical: int,
                                 timeout: int = 180) -> dict[str, str]:
    """Ask LM Studio for slug→canonical mapping. Returns {} on failure."""
    payload_user = {
        "chapter": chapter,
        "yyyymm": yyyymm,
        "max_canonical": max_canonical,
        "current_slugs": sorted(slugs),
    }
    url = endpoint.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": CONSOLIDATE_SYSTEM},
            {"role": "user", "content": json.dumps(payload_user,
                                                    ensure_ascii=False,
                                                    indent=2)},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_schema",
                             "json_schema": CONSOLIDATE_SCHEMA},
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise RuntimeError(
            f"LM Studio HTTP {e.code} at {url}: {body[:800] or e.reason}"
        ) from None
    data = json.loads(raw)
    content = data["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.S)
    parsed = json.loads(content)
    return {
        item["from"]: kebab(item["canonical"])[:25]
        for item in parsed.get("mapping", [])
        if item.get("from") and item.get("canonical")
    }


def _write_canonical_files(chapter: str, yyyymm: str, canonical: str,
                            sections: list[str], tags: list[str],
                            sources: list[str], title: str,
                            today: str) -> int:
    """Write all sections under one canonical slug, splitting on overflow.

    Returns the number of files written.
    """
    suffix = 1
    target = page_path(chapter, yyyymm, canonical, suffix)
    target.parent.mkdir(parents=True, exist_ok=True)
    buf = render_frontmatter(title, tags, sources, today)
    written = 0
    for sec in sections:
        chunk = sec.rstrip() + "\n\n"
        projected = len(buf.encode("utf-8")) + len(chunk.encode("utf-8"))
        if projected > MAX_FILE_BYTES and "## **" in buf:
            target.write_text(buf, encoding="utf-8")
            written += 1
            suffix += 1
            target = page_path(chapter, yyyymm, canonical, suffix)
            buf = render_frontmatter(title, tags, sources, today)
        buf += chunk
    target.write_text(buf, encoding="utf-8")
    return written + 1


def consolidate(args: argparse.Namespace) -> None:
    """Walk wiki/chats/ and collapse narrow topic files into canonical ones."""
    if not CHATS_OUT.exists():
        print("[consolidate] no chats dir; nothing to do")
        return

    chapters_scanned = 0
    groups_rewritten = 0
    files_before = 0
    files_after = 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for chapter_dir in sorted(p for p in CHATS_OUT.iterdir() if p.is_dir()):
        chapter = chapter_dir.name
        chapters_scanned += 1

        # Group files by yyyymm; within yyyymm, group by base slug (suffix-stripped).
        by_month: dict[str, dict[str, list[Path]]] = {}
        for md in sorted(chapter_dir.glob("*.md")):
            m = re.match(r"^(\d{6})-(.+?)(?:-(\d+))?\.md$", md.name)
            if not m:
                continue
            yyyymm, slug = m.group(1), m.group(2)
            by_month.setdefault(yyyymm, {}).setdefault(slug, []).append(md)
            files_before += 1

        for yyyymm, slugs_to_paths in by_month.items():
            distinct_slugs = len(slugs_to_paths)
            file_count = sum(len(v) for v in slugs_to_paths.values())

            if (distinct_slugs <= MAX_TOPICS_PER_MONTH
                    or file_count < MIN_FILES_TO_CONSOLIDATE):
                files_after += file_count
                continue

            print(f"[consolidate] {chapter}/{yyyymm}: "
                  f"{distinct_slugs} slugs across {file_count} files "
                  f"-> target ≤{MAX_TOPICS_PER_MONTH}")

            slugs = list(slugs_to_paths.keys())
            try:
                mapping = call_lm_studio_canonicalize(
                    args.endpoint, args.model, slugs, chapter, yyyymm,
                    MAX_TOPICS_PER_MONTH,
                )
            except (urllib.error.URLError, urllib.error.HTTPError,
                    json.JSONDecodeError, KeyError, TimeoutError,
                    RuntimeError) as e:
                print(f"  !! canonicalize error: {e}")
                files_after += file_count
                continue

            # LLM may have missed slugs — keep them as-is.
            for s in slugs:
                mapping.setdefault(s, s)

            # If LLM violated max_canonical, force-collapse the long tail
            # into the largest bucket.
            distinct_canonical = sorted(set(mapping.values()))
            if len(distinct_canonical) > MAX_TOPICS_PER_MONTH:
                load = Counter()
                for s, c in mapping.items():
                    load[c] += len(slugs_to_paths.get(s, []))
                top = {c for c, _ in load.most_common(MAX_TOPICS_PER_MONTH)}
                fallback = load.most_common(1)[0][0]
                mapping = {s: (c if c in top else fallback)
                           for s, c in mapping.items()}

            # If the mapping is a no-op, leave the directory alone.
            if all(mapping[s] == s for s in slugs):
                print("  -- already canonical, no rewrite needed")
                files_after += file_count
                continue

            canon_sections: dict[str, list[str]] = {}
            canon_tags: dict[str, set[str]] = {}
            canon_sources: dict[str, set[str]] = {}
            files_to_remove: list[Path] = []

            for slug, paths in slugs_to_paths.items():
                canonical = mapping[slug]
                for p in paths:
                    try:
                        text = p.read_text(encoding="utf-8")
                    except OSError as e:
                        print(f"  !! cannot read {p.name}: {e}")
                        continue
                    fm, body = parse_frontmatter(text)
                    sections = parse_sections(body)
                    if not sections:
                        # Nothing parseable; preserve the file.
                        continue
                    canon_sections.setdefault(canonical, []).extend(sections)
                    canon_tags.setdefault(canonical, set()).update(
                        _list_field(fm.get("tags", ""))
                    )
                    canon_sources.setdefault(canonical, set()).update(
                        _list_field(fm.get("sources", ""))
                    )
                    files_to_remove.append(p)

            if not canon_sections:
                print("  -- nothing parseable, skipping")
                files_after += file_count
                continue

            if args.dry_run:
                summary = ", ".join(
                    f"{c}<-{sum(1 for s in slugs if mapping[s]==c)}"
                    for c in sorted(set(mapping.values()))
                )
                print(f"  [dry-run] would collapse: {summary}")
                files_after += file_count
                continue

            for p in files_to_remove:
                try:
                    p.unlink()
                except OSError as e:
                    print(f"  !! cannot remove {p.name}: {e}")

            for canonical, sections in canon_sections.items():
                # Sort sections by their leading date so the page reads
                # chronologically after the merge.
                def _sec_key(s: str) -> str:
                    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
                    return m.group(1) if m else "9999-99-99"
                sections.sort(key=_sec_key)

                tags = sorted(canon_tags.get(canonical, set()) - {"chat"})
                sources = sorted(canon_sources.get(canonical, set()))
                title = canonical.replace("-", " ")
                written = _write_canonical_files(
                    chapter, yyyymm, canonical, sections,
                    tags, sources, title, today,
                )
                files_after += written
                print(f"  ++ {canonical}: {len(sections)} section(s) -> "
                      f"{written} file(s)")

            groups_rewritten += 1

    if not args.dry_run:
        rebuild_index()

    print(
        f"\n[consolidate] done.\n"
        f"  Chapters scanned:           {chapters_scanned}\n"
        f"  Chapter+month groups touched: {groups_rewritten}\n"
        f"  Files before:               {files_before}\n"
        f"  Files after:                {files_after}\n"
        f"  Net change:                 {files_after - files_before:+d}"
    )


def main() -> None:
    # Windows consoles default to cp1252/cp1251 which can't encode the arrows
    # and other Unicode we both log and write into markdown. Force UTF-8 so
    # stdout and stderr survive long ingest runs without crashing on a print.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--endpoint", default="http://localhost:1234/v1",
                    help="LM Studio OpenAI-compatible base URL")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"LM Studio model identifier (default: {DEFAULT_MODEL})")
    ap.add_argument("--limit", type=int, default=None,
                    help="Process at most N groups (for testing)")
    ap.add_argument("--only", default=None,
                    help="Process only one group by chat-id "
                         "(folder name minus 'DM '/'Space ')")
    ap.add_argument("--dry-run", action="store_true",
                    help="Walk and segment, but don't call the LLM and don't "
                         "write any files (state is also untouched)")
    ap.add_argument("--reset", action="store_true",
                    help="Wipe wiki/.ingest-state.json and start from scratch")
    ap.add_argument("--sleep-ms", type=int, default=0,
                    help="Sleep between LLM calls, ms")
    ap.add_argument("--consolidate", action="store_true",
                    help="Skip ingest. Walk wiki/chats/ and collapse narrow "
                         "per-incident topic files into <=4 canonical broad "
                         "topics per chapter+month, calling LM Studio to pick "
                         "the canonical labels. Old files are removed; new "
                         "ones are written, splitting on overflow. Combine "
                         "with --dry-run to preview.")
    args = ap.parse_args()
    if args.consolidate:
        consolidate(args)
        return
    run(args)


if __name__ == "__main__":
    main()
