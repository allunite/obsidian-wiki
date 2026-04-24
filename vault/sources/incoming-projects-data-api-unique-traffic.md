---
title: "Source: Incoming Projects / Data-API Unique Traffic Endpoint"
type: source
tags: [incoming-projects, api, unique-traffic, data-api]
sources:
  - raw/docs.allunite.com/Incoming Projects/The new data-api endpoint with aggregated unique traffic.md
updated: 2026-04-21
status: draft
---

# Source: Data-API Unique Traffic Endpoint

**Raw path:** `raw/docs.allunite.com/Incoming Projects/The new data-api endpoint with aggregated unique traffic.md`

## Summary

Spec v1.0 (January 2026, Draft) for `POST /v1/reports/traffic/unique`. Accepts: `facilities[]`, `networks[]`, `fromDate`, `toDate`, `granularity` (hour/day/week/month/year or total), `includeInactive`. Returns array of records with: `date`, `trafficTotal`, `trafficTotalBulk`, `viewableImpressions`, `viewedImpressions`, `frequency`. Cannot combine facilities and networks in one request. Without granularity returns single total record.

Sources: `raw/docs.allunite.com/Incoming Projects/The new data-api endpoint with aggregated unique traffic.md` 2026-04-21
