---
title: "Source: Data Methodologies / 3rd-Party Data / Finland LAM"
type: source
tags: [data-science, finland, lam, traffic-measurement, 3rd-party]
sources:
  - raw/docs.allunite.com/Data methodologies/3rd-party data/Finland, LAM.md
updated: 2026-04-21
status: stable
---

# Source: Finland LAM

**Raw path:** `raw/docs.allunite.com/Data methodologies/3rd-party data/Finland, LAM.md`

## Summary

LAM (Liikenteen Automaattisten Mittausasemien) = TMS (Traffic Measurement System) — Finnish automatic traffic measurement stations using induction loops in roads. Data from digitraffic.fi. AllUnite collects hourly statistics aggregated by vehicle class and direction. Results stored in `clickhouse/raw_lam`, station list in `postgresql/lam_stations`. Manual loading SQL via ClickHouse INSERT from digitraffic API.

Sources: `raw/docs.allunite.com/Data methodologies/3rd-party data/Finland, LAM.md` 2026-04-21
