---
title: Total Traffic
type: concept
tags: [analytics, metrics, core-concept]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md
related:
  - concepts/facility.md
  - concepts/rots.md
  - concepts/unique-traffic.md
  - concepts/dwell-time.md
  - systems/ml-traffic-prediction.md
updated: 2026-04-21
status: stable
---

# Total Traffic

**Total Traffic** is a facility-level metric: the number of times people enter the area around a facility within a defined time period. Once a person enters the area, they do not contribute additional Total Traffic unless they exit for more than 15 minutes. [^1]

- **Time period:** 1 hour, from XX:00 to XX+1:00 UTC (always round hours by UTC).
- **Area:** Circle with radius = `max_visibility_distance` (derived from the largest frame's dimensions), excluding areas behind enclosed walls or different floors.
- **Additive:** Total Traffic for combined facilities or combined periods is the sum of individual values. [^1]

**Known issue:** At midnight UTC, all people within the area are counted again as +1 Total Traffic. [^1]

## Calculation

Total Traffic is calculated by the Traffic job: `ml_traffic_prediction/main.py` on GitHub. See [ml-traffic-prediction](../systems/ml-traffic-prediction.md). [^1]

## Relationship to Other Metrics

- `ROTS = Total Traffic × Facility Traffic Share`
- `Unique Traffic` — non-additive count of unique people within Total Traffic population. [^1]
- `Visit Frequency = Total Traffic / Unique Traffic` [^1]

## Client FAQ

Total Traffic grows with the number of screens and reflects session counts. Unique Traffic is independent of screen count and does not grow as evenly. Total Traffic depends on sensor data (devices seen, distance, duration in visibility zone). [^2]

Changing a facility's Network does not affect Total Traffic, Unique Traffic, or other metrics. Only changes to frame characteristics (loop/slot duration, frame size, etc.) can affect impression calculations. [^2]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md, 2026-04-21
