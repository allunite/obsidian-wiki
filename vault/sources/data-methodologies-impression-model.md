---
title: "Source: Data Methodologies / Impression Model"
type: source
tags: [data-science, impressions, model]
sources:
  - raw/docs.allunite.com/Data methodologies/Impression model.md
updated: 2026-04-21
status: stable
---

# Source: Impression Model

**Raw path:** `raw/docs.allunite.com/Data methodologies/Impression model.md`

## Summary

Comprehensive overview of the AllUnite impression model. Two components:

1. **Moving audience (ImpressionsFlow):** Visibility distance = f(screen surface); Engagement Coefficient EC = max(DE-2X, 0) + DS (dynamic) or 1 (static); ImpressionsFlow = EligibleContactsMovingAudience × EC.
2. **Stationary audience (ImpressionsDwell):** Three exposure zones (primary 0-15m, secondary 15-30m, tertiary 30-50m/70m). ImpressionsDwell = sum over brackets of (dwell_bracket_mid × PrimaryVisibilityDistance × EligibleTraffic).

Total ViewableImpressions = ImpressionsFlow + ImpressionsDwell. ViewedImpressions = ViewableImpressions × min(VA × DAM, 1). Linear SOT model: ViewedImpressions_SOT = ViewedImpressions × SOT.

See [impression.md](../concepts/impression.md).

Sources: `raw/docs.allunite.com/Data methodologies/Impression model.md` 2026-04-21
