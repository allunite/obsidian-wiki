# AllUnite Domain Primer

A short primer on the shape of AllUnite's business and platform, so the model knows enough to route questions correctly without having to read every concept page first. This is background — authoritative definitions live in the wiki.

## What AllUnite is

AllUnite (Allunite A/S, Hellerup, Denmark) sells **Digital Out-of-Home (DOOH) analytics**: measurement of how many people pass a physical advertising screen, how many could have seen it, and how many likely did. Customers are screen-network operators (e.g. JCDecaux, Visual Media, Joe&TheJuice's internal network). The product is called **Analytics**; the underlying platform is called **MOPS**.

## Inventory model

```
Facility (physical structure, e.g. a billboard or a mall screen stack)
  └── Frame (one visible ad side; basic unit of inventory)
        └── Insertion (one ad play) within a Loop (full rotation cycle)
```

Facilities are grouped into **Clusters** by venue type: mall, park, transit, airport. Some facilities are **virtual**: they mirror traffic from a sensor-equipped source facility when they do not have their own sensor.

A frame has attributes like Frame ID, height/width, movement type (Static / Dynamic Mechanical / Digital), loop/insert duration, contents mix, lighting type, and a status lifecycle: `New → Changed → Approved (AU / 3P / Exhibitor) → Ready`, plus `Suspended` and `Demolished`.

## Metrics hierarchy (top → bottom, audience size shrinks)

```
Total Traffic           all people passing near the facility; 15-min WiFi session window
  └── ROTS              = Total Traffic × Facility Traffic Share; "people who could see the frame"
        └── VAC         = ROTS × clip(VA × Dynamic Coefficient, 0, 1); "people likely to have seen the ad"
              └── Viewed Impressions  = VAC × Impressions Coefficient
  Viewable Impressions  = ROTS × Impressions Coefficient  (parallel branch off ROTS)
  Reach                 unique people in VAC across slots
  Frequency             = Viewed Impressions / Reach
  Unique Traffic        non-additive; Visit Frequency
```

Key modifiers:
- **VA (Visibility Adjustment)** — 0–1 score from screen geometry and route direction.
- **Dynamic Slot Duration** — per-campaign slot/loop override; scales the Impressions Coefficient per hour when enabled via `company.enableDynamicVA`.

## Measurement stack

- **WiFi sensors**: Teltonika RUT200 + external antenna. Detect probe requests; sessions built from MAC addresses with a 15-min window; claimed accuracy ~94% ± 5%.
- **Sessions** are counted with MAC filtration rules defined in the WiFi methodology.
- **Without sensors**: traffic is modelled — either **multi-source mirroring** (OSM feature similarity, weighted) or **Global Model** (static seasonality). Manual counting validates calibration.

## Data infrastructure

- **ClickHouse** — raw and aggregated analytics (`device_session`, `device_session_agg_ml_2`, etc.). Repo: `allunite/db`.
- **PostgreSQL** — application state (inventory, ML model registry, manual counting).
- **AWS S3** — `allunite-models` bucket (ML model files); accessed via `sftpgo` at `files.allunite.local`.
- **Rundeck + Windmill** — scheduled job orchestration.
- **VictoriaMetrics + Alertmanager + Grafana** — infrastructure and router monitoring.

## Jobs / systems of note

- `recalc_ch` — sessionization in ClickHouse.
- `recalc_ch_agg` — aggregation on top of sessionization.
- `ml_traffic_prediction` — modelled traffic for sensor-less facilities; env vars configure model selection.
- Platform modules: Traffic Dashboard, Campaign Planner, Inventory Manager, Cluster Analytics (mall/park/transit/airport).
- Roles include: `trafficAnalytics`, `campaignPlanner`, `campaignPublisher`, `campaignAdmin`, `inventoryEditor`, `inventoryAuditor`, `userManager`, `localAdmin`, `admins`. Per-company feature flags gate visibility.

## Repos (GitHub)

- `allunite/mops` — the platform.
- `allunite/jobs` — data pipeline jobs (`recalc_ch`, `recalc_ch_agg`, `ml_traffic_prediction`, etc.).
- `allunite/db` — ClickHouse queries/schema.
- `allunite/server-configs` — Terraform / infra.

## Release cadence

Monthly-ish. Release naming is `v<YYYY>.<MM>.<DD>`. Wiki carries release notes back to **v2025.05.13**; most recent at time of wiki as of 2026-04-21 is **v2026.04.14** (Campaign Sharing System, AI inventory import validation, cross-company inventory editing, VA column in traffic report, `company.enableDynamicVA` toggle).

Releases are tracked in two places at once — the `raw/docs.allunite.com/Release Notes/` files and the ClickUp "Release N" lists under IT → Analytics Releases. Discrepancies are flagged in `wiki/release-timeline.md` rather than silently resolved.

## Clients and rollouts

Clients range from active deployments (Joe&TheJuice, Singapore JCD, Finland, Latvia) through rollouts in progress (Estonia, Belgium, Brazil) to early-stage RFPs/PoCs (Japan, Malaysia, Denmark, Nigeria, UAE, Cyprus+Hungary). Per-country pages live under `wiki/clients/<kebab-name>.md`.

Client-stage transitions (POC → Roll-Out → Active → Renewal → Churned) are preserved under `## History` on the client page — the wiki keeps the trajectory, not just the current state.

## Operational layout

Work tracking is in **ClickUp** (workspace `9015438153`). Ten spaces: IT, PMO & Delivery, Operational team, Customer Issues, Sales, Marketing, Board Meeting, High Level Review Projects, Finance, Resource Management. Task IDs are `DEV-###`; these are first-class cross-references (also used in commits/PRs). Time tracking is in **Clockify** across five categories: PreSales, New Project, Maintains, R&D, Internal.

## Chat shape

Internal chat is on Google Chat. The wiki has a **chat-index** (`wiki/chat-index.md`) listing spaces and DMs by topic tags and date range only — no personal names, no message content. Some chats are excluded from ingestion entirely (see `agent-prompt.md` §2). Deep per-thread ingestion happens on-demand, not by default.
