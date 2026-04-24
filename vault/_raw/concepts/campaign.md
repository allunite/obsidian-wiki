---
title: Campaign
type: concept
tags: [analytics, campaign, platform]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Statuses.md
  - raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Frames.md
  - raw/docs.allunite.com/Analytics Documentation/Campaign/Combined Campaigns.md
  - raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Frames/Filtering frames on a map.md
  - raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Frames/POI filter.md
related:
  - concepts/frame.md
  - concepts/frame-status.md
  - concepts/impression.md
  - concepts/dynamic-slot-duration.md
updated: 2026-04-21
status: stable
---

# Campaign

A campaign in AllUnite is a booking/planning unit that links a set of frames to an advertising period, enabling impression and reach calculations.

## Status Lifecycle

Campaigns move through statuses from Draft to Closed/Refused. Key statuses:

- **Draft** → **Proposal** → **Proposal Changed** → **Reserve** → **Awaiting PI** → **Request** → **Ready** → **Active** (auto) → **Delivered** (auto) → **Closed**
- **Refused** is reachable from most statuses. [^1]

## Frame Configuration

Frames are added to a campaign via:
- Filtering (campaign filters, frame attribute filters, tag filters, POI filters, manual map selection)
- Loading (from packages, CSV/Excel import)

For new campaigns, all client frames with status `Ready` or `Approved` are available. Once frames are loaded, further filtering is limited to that loaded set. [^2]

### Map Filtering

Frames can be filtered by drawing a polygon on the map using the "Select Frames on the map" toggle. [^3]

### POI Filter

Frames can be filtered by distance to Points of Interest (include within N meters, exclude within M meters). POIs sourced from Google or client-provided files. [^4]

## Combined Campaign Types

| Type | Description |
|------|-------------|
| **Merge** | Creates independent new campaign from frame lists of base campaigns. |
| **Combined** | Linked to base campaigns; updates automatically when base frame lists change. |
| **Grouped** | Aggregated reporting view only; no campaign parameters, base campaigns can be added/removed. | [^5]

[^1]: raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Statuses.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Frames.md, 2026-04-21
[^3]: raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Frames/Filtering frames on a map.md, 2026-04-21
[^4]: raw/docs.allunite.com/Analytics Documentation/Campaign/Campaign Frames/POI filter.md, 2026-04-21
[^5]: raw/docs.allunite.com/Analytics Documentation/Campaign/Combined Campaigns.md, 2026-04-21
