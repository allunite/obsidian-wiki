---
title: "Source: Analytics Documentation / Metrics Terminology / Metrics Calculation"
type: source
tags: [analytics, metrics, formulas]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md
updated: 2026-04-21
status: stable
---

# Source: Metrics Calculation

**Raw path:** `raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md`

## Summary

Formal calculation formulas for ROTS, VAC, Viewable/Viewed Impressions, Reach, Dynamic Slot Duration coefficients, and Visibility Adjustment. Contains LaTeX formulas. Key formulas:

- `ROTS = Total Traffic × Facility Traffic Share`
- `VAC = ROTS × clip(VA × Dynamic Coefficient, 0, 1)` (Dynamic Coefficient = 1.2 for digital, 1.0 for static)
- `Viewable Impressions = ROTS × Impressions Coefficient`
- `Viewed Impressions = VAC × Impressions Coefficient`
- VA calculation: three-step process (Momentary VA → Segment VA → Trip VA) using Route's k value and angular screen dimensions.
- Reach: estimated via slots_coeff, avg_va, avg_freq_facility, avg_screen_seen, reach_fraction.

TODO from source: re-introduce Illumination coefficient.

See [impression.md](../concepts/impression.md), [vac.md](../concepts/vac.md), [visibility-adjustment.md](../concepts/visibility-adjustment.md).

Sources: `raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md` 2026-04-21
