---
title: Impression
type: concept
tags: [analytics, metrics, core-concept]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md
  - raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md
related:
  - concepts/total-traffic.md
  - concepts/rots.md
  - concepts/vac.md
  - concepts/dwell-time.md
  - concepts/dynamic-slot-duration.md
  - systems/recalc-ch.md
  - systems/recalc-ch-agg.md
updated: 2026-04-21
status: stable
---

# Impression

AllUnite distinguishes two types of impressions, both frame-level metrics:

## Viewable Impressions

**Viewable impressions** — the total number of times different ad slots can be seen by people who are part of [ROTS](rots.md). One slot is one period of playing the specific ad; slots from different loops are considered different. [^1]

Formula: `Viewable Impressions = ROTS × Impressions Coefficient`

Where `Impressions Coefficient = (Dwell Time / Slot Duration) + 1` for dynamic frames, and `1` for static frames. [^2]

## Viewed Impressions

**Viewed impressions** — the total number of times different slots are actually seen by people who are part of [VAC](vac.md). [^1]

Formula: `Viewed Impressions = VAC × Impressions Coefficient` [^2]

A shorter slot duration yields more impressions per unit of dwell time. Example: dwell time = 60s, slot = 20s → 3 impressions; slot = 30s → 2 impressions. [^3]

## Impact of Dynamic Slot Duration

When [Dynamic Slot Duration](dynamic-slot-duration.md) overrides are applied at the campaign level, a `slot_coeff` adjusts both viewable and viewed impressions per frame per hour. Total Traffic is not affected. [^4]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md, 2026-04-21
[^3]: raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md, 2026-04-21
[^4]: raw/docs.allunite.com/Analytics Documentation/Dynamic Slot Duration.md, 2026-04-21
