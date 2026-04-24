---
title: Facility
type: concept
tags: [inventory, core-concept, analytics]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
related:
  - concepts/frame.md
  - concepts/cluster.md
  - concepts/total-traffic.md
updated: 2026-04-21
status: stable
---

# Facility

A **facility** is a physical advertising screen or structure — the top-level unit of AllUnite's inventory model.

Examples include standalone screens (double-sided MUPIs), single-sided billboards, bus shelters with multiple ad sides, and rows of billboards treated as a single unit by a client. Each visible ad side of a facility is a [frame](frame.md). [^1]

A single physical screen may be modelled as two separate facilities if the client sells each side independently; otherwise it is one facility with two frames. [^1]

**Also known as:** Panel, Site, Structure, Unit (in media planning).

## Metrics

Total Traffic is a facility-level metric: the number of times people enter the area around the facility within a defined time period. The area is a circle with radius equal to `max_visibility_distance` (derived from the largest frame's dimensions), excluding areas behind enclosed walls or different floors. [^2]

[^1]: raw/docs.allunite.com/Analytics Documentation/Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
