---
title: Wiki Index
type: overview
updated: 2026-04-21
status: stable
---

# AllUnite LLM Wiki — Index

Flat catalog, grouped by page type. Alphabetical within each section.

## Overview

- [overview](overview.md) — Top-level synthesis of AllUnite's platform and operations.
- [operations](operations.md) — Data/Ops operating model, team processes, active ops work.
- [release-timeline](release-timeline.md) — Monthly release changelog (v2025.05 – v2026.04).
- [inbox](inbox.md) — Unfiled drafts, candidate pages, follow-ups, Knowledge Hub items.
- [roadmap](roadmap.md) — In-flight IT work from ClickUp (DEV backlog + Release 11).
- [sales-pipeline](sales-pipeline.md) — Sales space synthesis: RFPs, opportunities, leads, LATAM.
- [marketing](marketing.md) — Marketing space: briefs, strategy, conferences, social, case studies.
- [governance](governance.md) — Board Meeting and High Level Review synthesis.
- [finance](finance.md) — Finance list structural categories (no figures).
- [customer-issues](customer-issues.md) — Customer issues (last 90 days).
- [clickup-index](clickup-index.md) — Full ClickUp workspace catalog (spaces, folders, lists).
- [chat-index](chat-index.md) — Google Chat spaces and DMs history.

## Concepts

- [campaign](concepts/campaign.md) — Campaign lifecycle, frame configuration, combined campaign types.
- [cluster](concepts/cluster.md) — Venue-based facility grouping; mall/park/transit/airport analytics.
- [dwell-time](concepts/dwell-time.md) — Screen and cluster dwell time; V2 calculation method.
- [dynamic-slot-duration](concepts/dynamic-slot-duration.md) — Per-campaign slot/loop override; slot_coeff.
- [facility](concepts/facility.md) — Physical advertising structure; Total Traffic area.
- [footfall](concepts/footfall.md) — Cluster-level metric; session windows by venue type.
- [frame](concepts/frame.md) — Each visible ad side; parameters and status lifecycle.
- [frame-status](concepts/frame-status.md) — 12 frame statuses and state machine.
- [frame-types](concepts/frame-types.md) — 13 frame type codes.
- [impression](concepts/impression.md) — Viewable and Viewed Impressions; Dynamic Slot Duration impact.
- [insertion](concepts/insertion.md) — Single advertisement shown on a screen.
- [linking-rules](concepts/linking-rules.md) — Outdoor and cluster linking for sensor-less facilities.
- [loop](concepts/loop.md) — Full ad rotation sequence; loop duration.
- [reach](concepts/reach.md) — Unique people in VAC; Frequency formula.
- [rots](concepts/rots.md) — ROTS = Total Traffic × Facility Traffic Share.
- [total-traffic](concepts/total-traffic.md) — Facility-level metric; 15-min session window.
- [unique-traffic](concepts/unique-traffic.md) — Non-additive unique people count; Visit Frequency.
- [vac](concepts/vac.md) — VAC = ROTS × clip(VA × Dynamic Coefficient, 0, 1).
- [visibility-adjustment](concepts/visibility-adjustment.md) — VA 0–1; 3-step calculation; Route methodology.

## Methodologies

- [ds-workflow](methodologies/ds-workflow.md) — Pre-project prep, traffic modelling overview, dwell time, impressions.
- [multi-source-mirroring](methodologies/multi-source-mirroring.md) — OSM feature similarity weights; Multisource Finland.
- [sensors-calibration](methodologies/sensors-calibration.md) — MC-to-prod pipeline; OLS regression; accuracy 94%±5%.
- [total-traffic-modelling](methodologies/total-traffic-modelling.md) — Sessions method, Global Model, validation.
- [wifi-methodology](methodologies/wifi-methodology.md) — MAC filtration rules; session counting.

## Systems

- [aws](systems/aws.md) — AWS access, S3 storage, EBS backup.
- [clickhouse](systems/clickhouse.md) — Core analytics data store; key tables.
- [ml-traffic-prediction](systems/ml-traffic-prediction.md) — Traffic + Impressions job; env vars; Rundeck orchestration.
- [monitoring](systems/monitoring.md) — VictoriaMetrics + Alertmanager; Grafana dashboard; router monitoring.
- [postgresql](systems/postgresql.md) — Relational DB; key tables; backup and restore.

## Entities

- [analytics-platform](entities/analytics-platform.md) — AllUnite's core DOOH analytics product; modules; roles.
- [repo-db](entities/repo-db.md) — allunite/db GitHub repository (ClickHouse queries).
- [repo-jobs](entities/repo-jobs.md) — allunite/jobs GitHub repository (data pipeline jobs).
- [repo-mops](entities/repo-mops.md) — allunite/mops GitHub repository (platform + Data API).
- [repo-server-configs](entities/repo-server-configs.md) — allunite/server-configs GitHub repository (Terraform).
- [team-data](entities/team-data.md) — Data team resource management (Resource Management list was empty at sync).

## Clients

- [joe-and-the-juice](clients/joe-and-the-juice.md) — Hardware standard, 4-VLAN network, installation, network policy.
- [finland](clients/finland.md) — Finland AM Project; contract addendum renegotiation.
- [estonia](clients/estonia.md) — Estonia Country rollout; 5 operators; sensor installation blocked.
- [japan](clients/japan.md) — Japan RFP; advanced negotiation; local team hiring.
- [latvia](clients/latvia.md) — Visual Media + JCDecaux projects; delivery phase.
- [india](clients/india.md) — Times OOH Goa Airport POC.
- [malaysia](clients/malaysia.md) — Malaysia RFP; preparation phase.
- [denmark](clients/denmark.md) — Denmark RFP; contract signing in progress.
- [belgium](clients/belgium.md) — Belgium PoC; 100 PMO tasks active.
- [nigeria](clients/nigeria.md) — Nigeria RFP (POC); sensor delivery in progress.
- [new-zealand](clients/new-zealand.md) — Phantom Billstickers; demographics + coverage analysis.
- [pakistan](clients/pakistan.md) — Move Pakistan; demographics integration in review.
- [cyprus-and-hungary](clients/cyprus-and-hungary.md) — Cyprus Malls; early deployment stage.
- [uae](clients/uae.md) — Backlite POC; data issue under investigation.
- [singapore](clients/singapore.md) — JCD Singapore; calibration + maintenance active.
- [brazil](clients/brazil.md) — 9 active client lists; sensor installation + inventory.
- [mexico](clients/mexico.md) — OLA Media; 2 open analytical issues.
- [costa-rica](clients/costa-rica.md) — Publiex; pre-deployment planning.

## Tasks

- [dev-225](tasks/dev-225.md) — DEV-225: Hourly traffic footfall bug (Singapore JCD; closed 2026-03-09).

## Sources

117 source pages in `sources/`. Key groups:
- `analytics-documentation-*` — 25 pages (Phase 1)
- `data-methodologies-*` — 27 pages (Phase 2)
- `operations-*` — 18 pages (Phase 3)
- `joe-and-the-juice-*` / `operations-joe-and-the-juice-*` — 5 pages (Phase 3)
- `infrastructure-*` / `development-*` / `services-*` / `generic-*` — 11 pages (Phase 4)
- `release-notes-*` — 12 pages (Phase 5)
- `ideas-*` / `inbox-*` / `incoming-projects-*` — 19 pages (Phase 6)
