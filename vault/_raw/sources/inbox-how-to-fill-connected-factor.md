---
title: "Source: Inbox / How to Fill Connected Factor for Facility in _v_facility_asset"
type: source
tags: [inbox, postgresql, facility, virtual-facility, data-ops]
sources:
  - raw/docs.allunite.com/Inbox/How to fill connected factor for facility in _v_facility_asset.md
updated: 2026-04-21
status: draft
---

# Source: How to Fill Connected Factor in _v_facility_asset

**Raw path:** `raw/docs.allunite.com/Inbox/How to fill connected factor for facility in _v_facility_asset.md`

## Summary

Note: `_v_facility_asset` is a PostgreSQL view that joins `company`, `facility`, `asset`, and `facility_virtual`. To fill `connected_facilities_factor` (traffic_factor), update the `facility_virtual` table directly — no other table needs changing. Note: recommends stopping use of `_v_facility_asset` view entirely.

Sources: `raw/docs.allunite.com/Inbox/How to fill connected factor for facility in _v_facility_asset.md` 2026-04-21
