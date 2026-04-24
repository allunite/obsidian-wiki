---
title: Analytics Platform
type: entity
tags: [platform, analytics, product]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Roles.md
  - raw/docs.allunite.com/Analytics Documentation/Terminology.md
related:
  - concepts/facility.md
  - concepts/frame.md
  - concepts/campaign.md
  - concepts/cluster.md
updated: 2026-04-21
status: stable
---

# Analytics Platform

AllUnite's Analytics Platform is the core product for DOOH (Digital Out-of-Home) analytics. It provides traffic measurement, impression modelling, campaign planning, and inventory management for advertising screen operators.

## Key Modules

- **Traffic Dashboard** — facility/cluster traffic metrics with filters and export.
- **Campaign Planner** — create and manage advertising campaigns; configure frames, timing, targets.
- **Inventory Manager** — manage frames and facilities; configure parameters, statuses, clusters.
- **Mall/Park/Transit/Airport Analytics** — cluster-specific analytics views.

## Role Structure

The platform uses granular role-based access control. See source page for full role list. Key roles:

- `trafficAnalytics` — main analytics dashboard, start page for most users
- `campaignPlanner` / `campaignPublisher` / `campaignAdmin` — campaign management
- `inventoryEditor` / `inventoryAuditor` — inventory management
- `admins` — full administrative access [^1]

[^1]: raw/docs.allunite.com/Analytics Documentation/Roles.md, 2026-04-21
