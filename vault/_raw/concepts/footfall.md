---
title: Footfall
type: concept
tags: [analytics, metrics, cluster]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md
related:
  - concepts/cluster.md
  - concepts/total-traffic.md
  - concepts/dwell-time.md
updated: 2026-04-21
status: stable
---

# Footfall

**Footfall** (also called "Total Traffic (Cluster)" on the platform) is a cluster-level metric: the number of times people enter the area of a cluster within a defined time period. A person does not contribute additional Footfall unless they exit the cluster area for more than X hours (varies by category: typically 2h for transport hubs, 8h for malls and airports). [^1]

Time period: 1 hour, XX:00 to XX+1:00 UTC.

Area: union of all floor plan areas in the cluster and all facility areas in the cluster.

**Known issue:** At midnight UTC, all people within the cluster area are counted again as +1 Footfall. Footfall also depends on the number of facilities in the cluster — adding a new facility (even one fully covered by existing ones) will likely change Footfall significantly. [^1]

Footfall = Total Traffic (Cluster) = Total Footfall from Campaign Planner. [^2]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md, 2026-04-21
