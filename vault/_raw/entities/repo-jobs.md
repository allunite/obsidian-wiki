---
title: "Repo: allunite/jobs"
type: entity
tags: [github, repository, jobs, ml, data-pipeline]
sources:
  - raw/github.md
related:
  - systems/ml-traffic-prediction.md
  - methodologies/total-traffic-modelling.md
  - methodologies/sensors-calibration.md
updated: 2026-04-21
status: stable
---

# Repo: allunite/jobs

GitHub repository `allunite/jobs`. Contains scheduled data pipeline jobs.

## Known Paths

| Path | Description |
|------|-------------|
| `jobs/master/recalc_ch` | Recalculation (sessionization) job — processes raw WiFi probe data into device sessions |
| `jobs/master/ml_traffic_prediction` | Traffic Prediction Job — runs Total Traffic and Impressions modelling |
| `jobs/master/recalc_ch_agg` | Aggregation Job — aggregates session data into `device_session_agg_5` |
| `jobs/master/data_health_check` | Data health check job |
| `jobs/master/data_monitoring` | Data monitoring job |
| `jobs/master/data_upload` | Data upload job |

See [systems/ml-traffic-prediction.md](../systems/ml-traffic-prediction.md) for job documentation.

[^1]: raw/github.md, 2026-04-21
