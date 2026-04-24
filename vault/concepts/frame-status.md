---
title: Frame Status
type: concept
tags: [inventory, workflow]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Statuses.md
related:
  - concepts/frame.md
  - concepts/campaign.md
updated: 2026-04-21
status: stable
---

# Frame Status

Frames follow a lifecycle through several statuses governing their visibility in campaigns and metrics calculation.

| Status | Description |
|--------|-------------|
| `New` | Created but not yet edited. |
| `Changed` | Auto-set when any metric-affecting parameter changes (position, angle, size, lighting, height). |
| `Ready` | Fully approved; final working status. |
| `Suspended` | Temporarily out of order; excluded from campaigns. |
| `Demolished` | Permanently removed from location; never used again. |
| `Unverified` | Team could not verify settings; needs attention. |
| `Approved by AU` | AllUnite team approved settings. |
| `Declined by AU` | AllUnite team rejected settings; correction needed. |
| `Approved by 3P` | Third-party team approved. |
| `Declined by 3P` | Third-party team rejected. |
| `Approved by Exhibitor` | Exhibitor team approved. |
| `Declined by Exhibitor` | Exhibitor team rejected. |

Campaign manager shows only `Ready`, `Approved by AU`, `Approved by 3P`, and `Approved by Exhibitor` frames for new campaigns. Traffic page does not filter by status. [^1]

Sources: `raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Statuses.md` 2026-04-21

[^1]: raw/docs.allunite.com/Analytics Documentation/Inventory/Frame Statuses.md, 2026-04-21
