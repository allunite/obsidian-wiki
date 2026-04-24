---
title: Dynamic Slot Duration
type: concept
tags: [analytics, campaign, impressions]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Dynamic Slot Duration.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md
related:
  - concepts/loop.md
  - concepts/impression.md
  - concepts/reach.md
  - concepts/frame.md
updated: 2026-04-21
status: stable
---

# Dynamic Slot Duration

**Dynamic Slot Duration** is a Campaign Planner feature that allows campaign-level overrides of the default slot and loop durations defined in Inventory Manager. It models scenarios where a campaign occupies a different share of screen rotation than the inventory defaults. [^1]

**Affected metrics:** Viewable Impressions, Viewed Impressions, Reach.
**Unaffected:** Total Traffic.

## Campaign Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Slots (n_slots_campaign) | 1 | Ad slots per loop |
| Loops (n_loops_campaign) | 1 | Consecutive loops the campaign runs |
| Slot Duration (sec) | From inventory | Duration of one ad slot |
| Loop Duration (sec) | From inventory | Total loop cycle time |

## Algorithm

The system computes a `slot_coeff` per frame per hour:

`slot_coeff = impressions_per_traffic_campaign / impressions_per_traffic_inventory`

Where each `impressions_per_traffic = (dwell_time + slot_duration) / effective_loop_duration`.

A coefficient > 1 means more impressions; < 1 means fewer. Static frames always use coefficient = 1. [^1]

## Edge Cases

- Empty/zero campaign values fall back to inventory defaults.
- Invalid configurations (slot time exceeds loop time) set coefficient to 1.
- Validation may be relaxed for customers with non-standard inventory parameters. [^1]

[^1]: raw/docs.allunite.com/Analytics Documentation/Dynamic Slot Duration.md, 2026-04-21
