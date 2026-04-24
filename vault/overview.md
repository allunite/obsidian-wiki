---
title: AllUnite Platform Overview
type: overview
tags: [allunite, dooh, analytics, platform]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md
updated: 2026-04-21
status: stable
---

# AllUnite Platform Overview

AllUnite (Allunite A/S, Hellerup, Denmark) is a Digital Out-of-Home (DOOH) analytics company. Its core product — the **Analytics Platform** — provides traffic measurement, impression modelling, campaign planning, and inventory management for advertising screen operators worldwide.

## Inventory Model

The fundamental unit is a **Facility** — a physical structure that hosts advertising screens at a specific location. Each facility has one or more **Frames** (visible ad sides). Frames show **Insertions** (individual ad plays) within a **Loop** (full ad rotation cycle).

Facilities are grouped into **Clusters** (mall, park, transit, airport) for aggregate analytics. A facility can be configured as a virtual facility that mirrors traffic from a sensor-equipped source facility.

## Metrics Hierarchy

Traffic flows through a chain of decreasing audience size:

1. **Total Traffic** — all people passing near the facility (15-min session window; WiFi sensor)
2. **ROTS** (Realistic OTS) — `Total Traffic × Facility Traffic Share`; people who could see the frame
3. **VAC** (Visually Adjusted Contact) — `ROTS × clip(VA × Dynamic Coefficient, 0, 1)`; people likely to have seen the ad
4. **Viewable Impressions** — `ROTS × Impressions Coefficient`
5. **Viewed Impressions** — `VAC × Impressions Coefficient`
6. **Reach** — unique people in VAC across all slots; **Frequency** = Viewed Impressions / Reach

Key modifiers: **Visibility Adjustment (VA)** is a 0–1 score derived from angular screen geometry and route direction. **Dynamic Slot Duration** adjusts the impressions coefficient per frame per hour when enabled.

## Data Infrastructure

- **WiFi sensors** (Teltonika RUT200 + antenna) detect probe requests; sessions are built from MAC addresses with 15-min window; accuracy ~94%±5%
- **ClickHouse** stores all raw and processed data (`device_session`, `device_session_agg_ml_2`, etc.)
- **PostgreSQL** stores application state (inventory, ML model registry, manual counting)
- **AWS S3** (`allunite-models` bucket) stores ML model files; accessed via sftpgo at `files.allunite.local`
- **Rundeck** + **Windmill** orchestrate scheduled jobs (traffic prediction, aggregation, impressions)
- **VictoriaMetrics + Alertmanager + Grafana** monitor infrastructure and router health

## Modelling Pipeline

Traffic for facilities without sensors uses: **multi-source mirroring** (OSM feature similarity) or **Global Model** (static seasonality). Manual counting validates sensor calibration. The **Total Traffic modelling** page covers the full flow.

## Platform Modules

- **Traffic Dashboard** — facility/cluster traffic metrics with filters and export
- **Campaign Planner** — configure frames, timing, demographics, slot duration
- **Inventory Manager** — manage frames, facilities, clusters, parameters, statuses
- **Mall / Park / Transit / Airport Analytics** — cluster-specific views

## Role-Based Access

Key roles: `trafficAnalytics`, `campaignPlanner`, `campaignPublisher`, `campaignAdmin`, `inventoryEditor`, `inventoryAuditor`, `userManager`, `localAdmin`, `admins`. Per-company feature flags control which metrics and modules are visible.

## Operations and Team

The Data/Ops team tracks work in **Clockify** (5 task categories: PreSales, New Project, Maintains, R&D, Internal). Tasks tracked in ClickUp. Client communications routed through designated channels. Pre-project checklist and scope control practices defined in the Operating Model.

## Recent Development (as of 2026-04-14)

Latest release (v2026.04.14) introduced: Campaign Sharing System, AI validation for inventory import, cross-company inventory editing, VA column in traffic report, and `company.enableDynamicVA` toggle. See [release-timeline.md](release-timeline.md) for full history since v2025.05.
