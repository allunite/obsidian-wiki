---
title: Reach
type: concept
tags: [analytics, metrics, campaign]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md
related:
  - concepts/vac.md
  - concepts/unique-traffic.md
  - concepts/impression.md
  - concepts/dynamic-slot-duration.md
updated: 2026-04-21
status: stable
---

# Reach

**Reach** is the number of unique people who are part of [VAC](vac.md) within any defined period of time around any defined number of frames. Reach is **not additive** (same constraints as [Unique Traffic](unique-traffic.md)). [^1]

`Frequency (campaign) = Viewed Impressions / Reach` [^1]

## Calculation

For a given campaign, reach is estimated using:
- `slots_coeff` — average fraction of combined slot durations over combined loop durations
- `avg_va` — total VAC / total ROTS for the whole campaign
- `avg_freq_facility` — weighted average frequency per facility, weighted by Unique Traffic
- `avg_screen_seen` — campaign frequency / weighted average facility frequency
- `reach_fraction` — formula using avg_va, slots_coeff, avg_screen_seen
- `reach = Unique Traffic × reach_fraction` [^2]

[Dynamic Slot Duration](dynamic-slot-duration.md) overrides affect Reach calculations via the same `slot_coeff`. [^2]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md, 2026-04-21
