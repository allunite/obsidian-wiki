---
title: Frame
type: concept
tags: [inventory, core-concept, analytics]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Parameters.md
  - raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Statuses.md
related:
  - concepts/facility.md
  - concepts/insertion.md
  - concepts/loop.md
  - concepts/impression.md
  - concepts/frame-status.md
updated: 2026-04-21
status: stable
---

# Frame

A **frame** is each visible ad side of a [facility](facility.md). It is the basic unit of inventory in AllUnite's platform — everything starts from the frame, and each frame can carry many properties. [^1]

## Key Parameters

- **Frame ID** — unique name/code; some clients also use an Alternative Frame ID.
- **Period of Operation** — active working hours, optionally per weekday.
- **Height and Width** — physical dimensions; critical for Visibility Adjustment (VA) and exposure calculations.
- **Movement Type** — Static, Dynamic Mechanical (rotating), or Digital (electronic loop-based).
- **Loop Duration / Insert Duration / Total Insertions** — apply to digital or rotated frames; define ad timing.
- **Contents** — types of content shown (e.g., 9 commercial + 1 social out of 10 insertions).
- **Lighting Type** — Backlight, Front light, No lighting, or Digital (self-lit).
- **Lighting Period** — Night or 24h.
- **Service Always Displayed** — small info area (time, weather, news) that draws attention but is not counted as an insertion. [^2]

## Status Lifecycle

Frames follow a lifecycle: `New` → `Changed` → approval/decline states → `Ready`. Only frames in `Ready`, `Approved by AU`, `Approved by 3P`, or `Approved by Exhibitor` status are shown in the campaign manager for new campaigns. `Suspended` frames are excluded from campaigns. `Demolished` frames are permanently deactivated. [^3]

See [frame-status.md](frame-status.md) for full status definitions.

[^1]: raw/docs.allunite.com/Analytics Documentation/Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Parameters.md, 2026-04-21
[^3]: raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Statuses.md, 2026-04-21
