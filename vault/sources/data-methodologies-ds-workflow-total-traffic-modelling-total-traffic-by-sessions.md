---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Total Traffic by Sessions"
type: source
tags: [data-science, traffic, sessions, ml]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md
updated: 2026-04-21
status: stable
---

# Source: Total Traffic by Sessions

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md`

## Summary

Primary method for computing Total Traffic. Script (`ml_traffic_prediction/main.py`) iterates over saved models, loads session data from `clickhouse/device_session`, applies models, writes to `clickhouse/device_session_agg_ml_2`. Parameters via env vars. Orchestrated via Rundeck job "ML Traffic prediction with parameters".

See [total-traffic-modelling.md](../methodologies/total-traffic-modelling.md), [ml-traffic-prediction.md](../systems/ml-traffic-prediction.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md` 2026-04-21
