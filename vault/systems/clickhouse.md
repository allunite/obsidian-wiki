---
title: ClickHouse
type: system
tags: [infrastructure, database, clickhouse, analytics, data]
sources:
  - raw/docs.allunite.com/Generic/Onboarding/Data team onboarding.md
  - raw/docs.allunite.com/Operations/DataBase query.md
related:
  - systems/ml-traffic-prediction.md
  - methodologies/wifi-methodology.md
updated: 2026-04-21
status: stable
---

# ClickHouse

AllUnite's primary analytics data store. Hosts raw sensor data, processed session data, and aggregated metrics.

## Key Tables

**Data tables:**
- `allunite.raw_devices_seen_buffer` / `raw_devices_seen_2` — raw WiFi probe data from sensors
- `device_session` — processed WiFi sessions
- `device_session_agg_ml_2` — metrics as predicted by ML models
- `device_session_agg_5` — aggregated metrics (5-minute buckets)

**Reference/info tables:**
- `company_dict` — company lookup
- `facility_dict` — facility lookup; check if facility has real data
- `frame_dict` — frame lookup
- `_v_facility_asset` — facility asset parameters view

**3rd-party data tables:**
- `clickhouse/raw_positioning_buffer` — Finland GTFS Realtime vehicle positions [^3]
- `clickhouse/raw_lam` — Finland LAM (TMS) hourly traffic counts [^3]
- `core.raw_data_3rd_party` — generic 3rd-party location data (Denmark, Belgium, Japan, Pakistan) [^3]

## Web GUI

ClickHouse play interface at `clicknorris.allunite.local:8123/play` (VPN required). [^2]

[^1]: raw/docs.allunite.com/Generic/Onboarding/Data team onboarding.md, 2026-04-21
[^2]: raw/docs.allunite.com/Operations/DataBase query.md, 2026-04-21
[^3]: raw/docs.allunite.com/Data methodologies/3rd-party data/, 2026-04-21
