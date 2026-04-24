# Dasha — endpoint reference

Dasha has **one surface** (Dashboard) and **one tool palette** (read-only inventory + demographics + ClickHouse traffic). All paths are relative to the MOPS API base. Extracted from `C:\Solutions\mops\src\server\controllers\` on 2026-04-22.

## 1. Inbound: the Dashboard chat contract

This is the only endpoint Dasha *receives* traffic on. MOPS proxies the user's message to Dasha's AI API; Dasha returns markdown + StructuredOutput.

| MOPS route | AI API route (Dasha) | File |
|---|---|---|
| `POST /dashboard/traffic/agent/chat` | `POST {aiApiUrl}/chat/dashboard` | `dashboard-traffic.controller.ts` |

Request body (MOPS → Dasha) — grounded with the user's scope:
```json
{
  "email": "...",
  "session": "<chat_session_id>",
  "message": "...",
  "index_restrictions": "<SQL snippet>",
  "cities":    ["Copenhagen", "Aarhus", ...],
  "regions":   ["Hovedstaden", ...],
  "networks":  ["JCDecaux-DK", ...],
  "timezones": ["Europe/Copenhagen"],
  "labels":    ["flagship", "transit", ...]
}
```

Response body (Dasha → MOPS → UI):
```json
{
  "message":    "markdown string",
  "query":      { /* partial QueryTrafficParamsScheme — keys the user changed */ },
  "is_noquery": false,
  "is_error":   false
}
```

See `query-traffic-params.schema.json` in this folder for the exact shape of `query`.

**Auth forwarding.** MOPS forwards the user's `Cookie: SESSION=<value>` header to Dasha on every dashboard chat call. Dasha uses this cookie on every outbound call she makes back into MOPS (inventory, demographics, impersonation). This is a **required** piece of the wiring — without SESSION forwarding, Dasha's impersonation and scope-gated reads fail. Today the forwarding is implemented for `/chat/campaign` in `ai-agent.service.ts`; the equivalent needs to live on the `/chat/dashboard` path for Dasha to function with the tool palette below.

**NB:** as of 2026-04-22 the controller at `dashboard-traffic.controller.ts:36` currently wires `/dashboard/traffic/agent/chat` to `chatHelp` (not `chatTrafficDashboard`) — the `chatTrafficDashboard` call is commented out. When MOPS flips that line back, Dasha's full StructuredOutput payload will start flowing to the widget.

Dasha does **not** call any chat endpoint. She serves this one.

## 2. Outbound tool palette — read-only MOPS REST

Dasha calls these *from* her own service back into MOPS, grounding dashboard answers in inventory structure and demographic context. Everything below is a GET (plus a few POSTs that are read-like filtered-lookups).

### 2a. Dashboard live metrics (the primary tool)
`dashboard-traffic.controller.ts` — `@Controller('dashboard/traffic')`
- `GET /dashboard/traffic/:metric` — the main live-metric endpoint. `:metric ∈ { all-visitors, totals, charts, bar, hf, demographics, conversion }`.
- `GET /dashboard/traffic/report-matrix`

Query-string params match `QueryTrafficParams` (the same schema Dasha emits) plus `report-grouping`, `report-header`, `ds`, `iwh`, `queryCache`.

*Do not* call `report-xlsx` or `monthly-xlsx` — those are UI-button exports.

### 2b. Inventory read
- `facility.controller.ts` — `@Controller('facility')`
  - `GET /facility/list`
  - `GET /facility/tree`
  - `GET /facility/:id`
- `frame.controller.ts` — `@Controller('frames')`
  - `GET /frames/:id`
  - `GET /frames/:id/segments`
  - `GET /frames/:id/versions`
  - `GET /frames/:id/versions/:versionId`
  - `GET /frames/versions/unapproved`
  - `GET /frames/versions/all-unapproved`
- `cluster.controller.ts` — `@Controller('clusters')`
  - `GET /clusters`
  - `GET /clusters/:id`
  - `GET /clusters/:id/facilities`
- `inventory.controller.ts` — `@Controller('inventory')`
  - `GET  /inventory`
  - `POST /inventory/list` — filtered read, body carries the filter spec
  - `GET  /inventory/inventory-frames`
  - `GET  /inventory/inventory-frames-tz`
  - `GET  /inventory/inventory-networks`
  - `GET  /inventory/facilities`
  - `GET  /inventory/master-facilities`
  - `GET  /inventory/virtual-facilities`
  - `GET  /inventory/framestatuses`
  - `GET  /inventory/:id`
  - `GET  /inventory/:id/changes`
- `inventory-classification.controller.ts` — `@Controller('inventory-classification')`
  - `GET /inventory-classification/traffic-segments`
  - `GET /inventory-classification/frames`
  - `GET /inventory-classification/facilities`
- `points-of-interest.controller.ts` — `@Controller('points-of-interest')`
  - `GET  /points-of-interest`
  - `GET  /points-of-interest/categories`
  - `POST /points-of-interest/filtered-poi` — filtered read
  - `POST /points-of-interest/filter-frames` — filtered read

### 2c. Demographics read
`demographics.controller.ts` — `@Controller('demographics')`
- `GET /demographics/variables`
- `GET /demographics/filters`
- `GET /demographics/targets`
- `GET /demographics/countries`

(`data-layers` and `country-areas/traffic` are admin-only and out of scope for Dasha.)

### 2d. Impersonation (admin-gated, one narrow write exception)
`impersonation.controller.ts` — `@Controller('impersonation')` — guarded by `Roles.admins | Roles.localAdmin`:
- `GET    /impersonation` — read the current impersonation state (returns `null` / the impersonated user)
- `PUT    /impersonation` — body `{ userId: "<uuid>" }`, switch the session to that user. On success, MOPS re-issues the JWT cookie under the impersonated identity. A non-admin caller is rejected with 403.
- `DELETE /impersonation` — clear impersonation, revert to the real user

Target discovery (read-only, used to resolve "view as <name/email>" into a `userId`):
`user.controller.ts` — `@Controller('user')`:
- `GET /user/list` — list users (supports `filter`, `sortBy`, `sortDir`, `pageSize`, `pageNum`). Requires one of `userManager | companies | campaignPublisher | campaignPlanner | campaignGuest | campaignAdmin`.
- `GET /user/:userId/details` — confirm a specific user (UUID) before switching. Requires `userManager | companies | self`.

All of these require the forwarded SESSION cookie. Dasha attempts the PUT blindly and lets MOPS' guard decide; 403 → surface via `is_error: true`. Full protocol in SKILL.md §6.

## 3. Endpoints Dasha must NOT call

- **Any chat endpoint** — `POST /help/chat`, `POST /dashboard/traffic/agent/chat`, `POST /campaigns/ai/chat`. Dasha *is* the chat agent; she never calls it back.
- **All campaign endpoints** — everything under `/campaigns/*` (including `/campaigns/ai/*`, `/campaigns/target/*`, `/campaigns/report/*`, `/campaigns/frames/*`, `/campaigns/:id/*`) and all of `/campaign-packages`.
- **All writes, deletes, and admin paths** — any `POST`/`PUT`/`DELETE` on `inventory`, `frame`, `facility`, `cluster`, `boxes`, `vehicles`, `user`, `companies`, `manual-countings`, `footfall`, and anything under `auth`, `access-token`, `admin-tools`, `seed`. **Single narrow exception:** `/impersonation` GET/PUT/DELETE (see §2d). (The two `POST` entries in §2b — `/inventory/list` and the `points-of-interest/filter*` pair — are filtered reads, not writes.)
- **Exports** — `dashboard-traffic/report-xlsx`, `dashboard-traffic/monthly-xlsx`, `dashboard-traffic/report-matrix` (this last one *is* readable but initiated by a UI button, not chat).
- **Other dashboard surfaces** — `dashboard-realtime`, `dashboard-mall`, `dashboard-captive`, `dashboard-conversion`, `dashboard-ds`. Dasha only serves the Traffic dashboard.

If the user asks for one of these, decline politely and name the MOPS screen that performs the action.

## 4. Ground-truth files (read-only)

- Chat request/response DTOs: `mops/src/server/models/chat/dashboard-chat-request.ts`, `dashboard-chat-response.ts`
- StructuredOutput schema: `mops/src/common/models/params/query-traffic.params.schema.json` (copied into `references/query-traffic-params.schema.json` in this skill)
- Query traffic params class: `mops/src/common/models/params/query-traffic.params.ts`
- Scope restriction queries (source of `index_restrictions`, `cities`, `regions`, `networks`, `timezones`, `labels`): `mops/src/server/core/queries/dashboard-chat.queries.ts`
- Live metrics controller: `mops/src/server/controllers/dashboard-traffic.controller.ts`
- Impersonation controller: `mops/src/server/controllers/impersonation.controller.ts`
- User listing controller: `mops/src/server/controllers/user.controller.ts`
- SESSION cookie forwarding pattern (applied today to `/chat/campaign`, must be extended to `/chat/dashboard`): `mops/src/server/services/ai-agent.service.ts` lines 123–134
