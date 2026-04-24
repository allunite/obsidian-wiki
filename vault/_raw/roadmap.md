---
title: Roadmap
type: overview
tags: [roadmap, clickup, it]
sources: []
updated: 2026-04-21
status: stable
---

# Roadmap

In-flight IT work grouped by theme. Sourced from ClickUp: Platform Development (`901511730069`), Project Tasks (`901511907168`), Infrastructure Tasks (`901512018681`), and Release 11 (`901522927904`). Open tasks only. As-of 2026-04-21.

---

## Release 11 — v2026-05-12 (in-flight)

These tasks are actively scoped for the next release. [clickup:list/901522927904]

- **DEV-196** — Campaign: set limit so old Reach cannot be higher than Unique Traffic (`in progress`) [clickup:task/86c74c7x9]
- **DEV-166** — Inconsistency in footfall calculation (`in progress`) [clickup:task/86c6gr8bt]
- **DEV-86** — Group campaign metrics (`in progress`, high priority) [clickup:task/86c5adrdz]

---

## Data Pipeline & ClickHouse

Core analytics data store and aggregation pipeline work. [clickup:list/901511730069]

- **DEV-254** — Recalculate `device_session_trusted` with `device_id` (`in progress`, high) [clickup:task/86c8y6hvb]
- **DEV-203** — Initial schema and seed for ClickHouse (`in progress`, high) [clickup:task/86c7cqr3b]
- **DEV-160** — Dry agg_6 (`backlog`) [clickup:task/86c6fgmx7]
- **DEV-161** — Avoid sessions in dashboards and data-api (`backlog`) [clickup:task/86c6fgp9a]
- **DEV-162** — Add projections for views (`backlog`) [clickup:task/86c6fgpv3]
- **DEV-163** — Try PASTE JOIN (`backlog`) [clickup:task/86c6fgq89]
- **DEV-158** — Fill `device_theta_sample` from trusted sessions (`backlog`) [clickup:task/86c6fgkpg]
- **DEV-159** — Adjust DB DDL for prod/stage (`backlog`) [clickup:task/86c6fgmfq]
- **DEV-213** — Fix aggregation script (`backlog`) [clickup:task/86c7rkn50]
- **DEV-249** — Issue with mirroring (`backlog`) [clickup:task/86c8xftyw]

---

## Platform Features

New capabilities and improvements to the analytics platform. [clickup:list/901511730069]

- **DEV-277** — Allow only "Ready" status frames in campaigns (`backlog`) [clickup:task/86c9eqpaq]
- **DEV-275** — Update inventory import rules: HARD/SOFT split + bypass checkbox (`backlog`) [clickup:task/86c9e2e83]
- **DEV-274** — Inventory Sandbox: approve/decline workflow to push to live inventory (`backlog`) [clickup:task/86c9e1wr8]
- **DEV-189** — Using Proof-of-Play data in calculations (`backlog`) [clickup:task/86c6yypku]
- **DEV-168** — Campaign problem (`backlog`) [clickup:task/86c6gv0zq]
- **DEV-190** — Terminology (`backlog`) [clickup:task/86c6zz4x7]
- **DEV-210** — Monitoring bot assistant (`backlog`) [clickup:task/86c7m7t9e]

---

## Infrastructure

Server, access, and pipeline infrastructure. [clickup:list/901512018681]

- **DEV-202** — Set up Overpass API to fill geodata for locations (`in progress`) [clickup:task/86c7bwpfx]
- **DEV-276** — Provide access to `vault.allunite.com` to Data Team (`backlog`, normal) [clickup:task/86c9ehefh]
- **DEV-199** — Remove writing to `stat_ping` table (`backlog`) [clickup:task/86c76xh1q]
- **DEV-165** — Move and structurize raw seen (`backlog`) [clickup:task/86c6gqhzf]
- **DEV-164** — Adjust queries in templates to use views (`backlog`) [clickup:task/86c6gqh9n]
- **DEV-177** — Environment for Freelancers (Data Team) (`backlog`) [clickup:task/86c6q73kk]

---

## Project / DS Work

Data science and analytics project tasks. [clickup:list/901511907168]

- **DEV-171** — Optimize geometry for Ramboll segments (`backlog`) [clickup:task/86c6je8tt]
