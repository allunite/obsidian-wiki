---
title: Unique Traffic
type: concept
tags: [analytics, metrics]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
related:
  - concepts/total-traffic.md
  - concepts/reach.md
updated: 2026-04-21
status: stable
---

# Unique Traffic

**Unique Traffic** is the number of unique people who are part of [Total Traffic](total-traffic.md) within any defined period of time around any defined number of facilities. [^1]

Unique Traffic is **not additive**:
- For 2 time periods: `max(UT1, UT2) ≤ UT_combined ≤ UT1 + UT2`
- For 2 facility groups: same constraints apply. [^1]

`Visit Frequency = Total Traffic / Unique Traffic` (average number of times a unique person passes a facility). [^1]

Unlike Total Traffic, Unique Traffic is independent of the number of screens and does not grow as evenly. [^1]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
