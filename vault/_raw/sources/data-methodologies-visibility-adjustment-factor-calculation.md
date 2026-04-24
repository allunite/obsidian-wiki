---
title: "Source: Data Methodologies / Visibility Adjustment Factor Calculation"
type: source
tags: [data-science, visibility-adjustment, route]
sources:
  - raw/docs.allunite.com/Data methodologies/Visibility Adjustment Factor Calculation.md
updated: 2026-04-21
status: stable
---

# Source: Visibility Adjustment Factor Calculation

**Raw path:** `raw/docs.allunite.com/Data methodologies/Visibility Adjustment Factor Calculation.md`

## Summary

VA factor is calculated using the Route methodology: accounts for distance to frame, dwell time, deflection angle, azimuth, visible angle, offset. Model uses Wi-Fi dwell time data from sensor locations; models dwell time for locations without sensors based on transport mode from mobility analytics (Nommon or Ramboll). Calculates momentary opportunities every 0.1 seconds to determine probability of screen visibility.

See [visibility-adjustment.md](../concepts/visibility-adjustment.md).

Sources: `raw/docs.allunite.com/Data methodologies/Visibility Adjustment Factor Calculation.md` 2026-04-21
