---
title: "Source: Operations / Operation Tools / Geocooding"
type: source
tags: [operations, tools, geocoding, google-sheets]
sources:
  - raw/docs.allunite.com/Operations/Operation tools/Geocooding.md
updated: 2026-04-21
status: stable
---

# Source: Geocooding

**Raw path:** `raw/docs.allunite.com/Operations/Operation tools/Geocooding.md`

## Summary

Google Apps Script for reverse geocoding in Google Sheets. Provides 5 custom functions: `GEO_FULL_ADDRESS`, `GEO_STREET`, `GEO_ZIP`, `GEO_CITY`, `GEO_REGION` — all take latitude and longitude parameters. Limitations: ~1,000–2,000 free calls/day (Google quota); process in batches of 50 rows to avoid OVER_QUERY_LIMIT; 100ms sleep between calls. Uses `Maps.newGeocoder().reverseGeocode()` API.

Sources: `raw/docs.allunite.com/Operations/Operation tools/Geocooding.md` 2026-04-21
