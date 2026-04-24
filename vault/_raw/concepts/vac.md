---
title: VAC (Visibility Adjusted Contact)
type: concept
tags: [analytics, metrics]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md
related:
  - concepts/rots.md
  - concepts/impression.md
  - concepts/visibility-adjustment.md
updated: 2026-04-21
status: stable
---

# VAC (Visibility Adjusted Contact)

**VAC** is a frame-level metric: the part of [ROTS](rots.md) consisting of people who actually saw the screen. [^1]

Formula: `VAC = ROTS × clip(Visibility Adjustment × Dynamic Coefficient, 0, 1)` [^2]

Where:
- `Dynamic Coefficient = 1.2` for dynamic (digital) frames, `1.0` for static frames.
- [Visibility Adjustment](visibility-adjustment.md) (VA) is a number between 0 and 1 representing the probability that a person from ROTS actually focused attention on the frame.

VAC feeds directly into [Viewed Impressions](impression.md) and [Reach](reach.md).

**TODO (from source):** Re-introduce Illumination coefficient for VAC so that illuminated screens have higher visibility at night and non-illuminated screens have zero. [^2]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md, 2026-04-21
