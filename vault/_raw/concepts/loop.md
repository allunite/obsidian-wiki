---
title: Loop
type: concept
tags: [analytics, core-concept, campaign]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Terminology.md
  - raw/docs.allunite.com/Analytics Documentation/Dynamic Slot Duration.md
related:
  - concepts/insertion.md
  - concepts/frame.md
  - concepts/impression.md
  - concepts/dynamic-slot-duration.md
updated: 2026-04-21
status: stable
---

# Loop

A **loop** is a full set of insertions (ads) that play one after another on a digital or rotated screen before they repeat. [^1]

**Also known as:** Ad rotation, Playlist, Ad cycle.

## Loop Duration

**Loop Duration** is the total time in seconds to complete one loop from start to end. For example: 6 ads × 10 seconds each = 60-second loop duration. Also known as cycle time, play loop time, or full rotation duration. [^1]

Analytics can support flexible setups where slot/loop parameters are not fixed or defined.

## Relationship to Impressions

The loop duration and insert duration (slot duration) are key inputs for impression calculation. The number of impressions a person generates depends on their dwell time relative to the slot duration and loop duration. Longer ads mean fewer impressions per person with the same dwell time. [^2]

See [dynamic-slot-duration.md](dynamic-slot-duration.md) for campaign-level overrides of slot/loop parameters.

[^1]: raw/docs.allunite.com/Analytics Documentation/Terminology.md, 2026-04-21
[^2]: raw/docs.allunite.com/Analytics Documentation/Dynamic Slot Duration.md, 2026-04-21
