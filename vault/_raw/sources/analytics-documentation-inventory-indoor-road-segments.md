---
title: "Source: Analytics Documentation / Inventory / Indoor Road Segments"
type: source
tags: [analytics, inventory, road-segments]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Inventory/Indoor Road Segments.md
updated: 2026-04-21
status: stable
---

# Source: Indoor Road Segments

**Raw path:** `raw/docs.allunite.com/Analytics Documentation/Inventory/Indoor Road Segments.md`

## Summary

Design document for road segment management in indoor venues. Problem: two storage types (system-wide roads vs. frame-specific roads) cause friction when new road segments are added — Ready frames must not have metrics changed automatically. Proposes three solutions: (1) Status-Based Auto-Add (recommended) — auto-add only for non-Ready frames; (2) Inventory-Level Flag — company-wide In Progress/Ready mode; (3) Hybrid. Includes implementation considerations and next steps.

Sources: `raw/docs.allunite.com/Analytics Documentation/Inventory/Indoor Road Segments.md` 2026-04-21
