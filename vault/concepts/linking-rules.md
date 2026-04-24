---
title: Linking Rules
type: concept
tags: [inventory, methodology, traffic-modelling]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Inventory/Linking rules.md
related:
  - concepts/facility.md
  - concepts/cluster.md
  - concepts/total-traffic.md
updated: 2026-04-21
status: stable
---

# Linking Rules

Linking rules determine how facilities without sensors are associated with sensor-equipped facilities for traffic data attribution.

## Outdoor Linking

- Facility without a sensor is linked to the nearest facility with a sensor of the **same category**.
- "Nearest" = shortest direct distance between virtual and sensor locations.
- Other categories are considered only if no facility of the required category exists in the same city or region. [^1]

## Cluster Linking

- Facility without a sensor links to the nearest sensor-equipped facility in the **same cluster and same category**.
- If no same-category sensor exists in the cluster, category is ignored.
- If only one sensor exists in the cluster, all non-sensor facilities link to it regardless of category.
- If no sensor exists in the cluster, search the same city for another cluster of the same category with similar size and operating hours; then expand to nearest city. [^1]

When linking across clusters, distribute links evenly across all sensors, accounting for location (facilities near entrances link to sensor facilities near entrances). [^1]

[^1]: raw/docs.allunite.com/Analytics Documentation/Inventory/Linking rules.md, 2026-04-21
