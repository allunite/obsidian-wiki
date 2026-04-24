---
title: Dwell Time
type: concept
tags: [analytics, metrics]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md
related:
  - concepts/rots.md
  - concepts/impression.md
  - concepts/total-traffic.md
  - concepts/cluster.md
updated: 2026-04-21
status: stable
---

# Dwell Time

**Dwell Time (Screen)** is a frame-level metric: the average period of time one unit of ROTS spends satisfying ROTS conditions (being able to see the display of the frame). Aggregated as an average across every visit that starts within the aggregation period. Minimum aggregation period is 1 hour. [^1]

**Dwell Time (Cluster)** — the average time a person spent in a cluster (mall, airport, etc.), calculated from the first to last session within the cluster session window (2 hours for transport hubs, 8 hours for malls/airports). [^2]

## Sensor Calibration

Sensors are calibrated per environment to capture devices within the required distance (e.g., ~25m for malls, ~60m for roadside). Walking Speed is a static average value and does not participate in Dwell Time calculation. [^2]

Dwell Time (Cluster) may be shorter than expected because sensors do not always cover the full area, and people may leave sensor range temporarily. [^2]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md, 2026-04-21
