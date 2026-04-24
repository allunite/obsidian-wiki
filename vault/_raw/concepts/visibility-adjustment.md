---
title: Visibility Adjustment (VA)
type: concept
tags: [analytics, metrics, methodology]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md
related:
  - concepts/vac.md
  - concepts/rots.md
  - concepts/frame.md
updated: 2026-04-21
status: stable
---

# Visibility Adjustment (VA)

**Visibility Adjustment (VA)** is a number between 0 and 1 representing the chance that a person from ROTS actually focuses attention on a frame of specific dimensions and placement, without accounting for illumination or whether the frame is static/dynamic. [^1]

## Calculation Steps

1. **Momentary VA** — For each road segment and direction/mode combination, the segment is split into points spaced 0.1 second of travel time apart. For each point:
   `va_momentary = 1 - exp(k_route × theta_deg)` where `theta_deg` is the angular size of the screen and `k_route` is provided by Route. [^2]

2. **Segment VA** — Momentary values combined as probabilities:
   `va_segment = 1 - (1 - va_0)(1 - va_1)...(1 - va_n)` [^2]

3. **Trip VA** — For each transport mode, trips are sequences of road segments. The final VA is one number per frame. [^2]

**TODO (from source):** A planned illumination coefficient would adjust VAC so illuminated screens have higher visibility at night and non-illuminated screens have zero. [^1]

[^1]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Metrics Terminology/Metrics Calculation.md, 2026-04-21
