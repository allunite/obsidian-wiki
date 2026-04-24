---
title: "Source: Data Methodologies / 3rd-Party Data / Raw Location Data"
type: source
tags: [data-science, location-data, 3rd-party, clickhouse]
sources:
  - raw/docs.allunite.com/Data methodologies/3rd-party data/Raw location data.md
updated: 2026-04-21
status: stable
---

# Source: Raw Location Data

**Raw path:** `raw/docs.allunite.com/Data methodologies/3rd-party data/Raw location data.md`

## Summary

Third-party raw location data: main columns `latitude, longitude, device_id, timestamp, horizontal_accuracy`. Stored in `clickhouse/core.raw_data_3rd_party` with fields: `country`, `case_name`, `timestamp` (UTC), `device_id`, `latitude`, `longitude`, `horizontal_accuracy`, `data` (JSON), `created`. Data received as archives (CSV on S3 or otherwise), uploaded under new `case_name`. Processing script: `update_traffic_coefficients.ipynb`. Known cases: Denmark (citydata-2025-denmark), Belgium (accurat-2025-poc), Japan (multiple lifesight datasets), Malaysia, Pakistan.

Sources: `raw/docs.allunite.com/Data methodologies/3rd-party data/Raw location data.md` 2026-04-21
