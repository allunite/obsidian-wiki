---
title: "Source: Analytics Documentation / Clients' Questions Regarding Metrics"
type: source
tags: [analytics, metrics, client-faq]
sources:
  - raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md
updated: 2026-04-21
status: stable
---

# Source: Clients' Questions Regarding Metrics

**Raw path:** `raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md`

## Summary

Collection of client FAQ answers on metrics behavior. Key clarifications:

- Total Traffic (screens) vs. Total Traffic (Cluster): screens counts every sensor crossing; cluster deduplicates per-session window (2h transport, 8h mall/airport).
- Walking Speed is static/average and does not feed into Dwell Time calculation.
- Impressions decrease as slot duration increases.
- Viewable vs. Viewed Impressions: Viewed = Viewable × visibility factor × DAM.
- Unique Traffic is not additive; should not be evaluated at hourly granularity.
- Footfall cannot be used to evaluate audiences of a Network spanning multiple locations.
- SOT (Share of Time) has linear relationship to impressions.

See concept pages: [impression.md](../concepts/impression.md), [dwell-time.md](../concepts/dwell-time.md), [total-traffic.md](../concepts/total-traffic.md), [footfall.md](../concepts/footfall.md).

Sources: `raw/docs.allunite.com/Analytics Documentation/Clients' questions regarding metrics.md` 2026-04-21
