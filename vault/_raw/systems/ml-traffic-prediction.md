---
title: ML Traffic Prediction Job
type: system
tags: [system, ml, traffic, job, clickhouse]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Impressions.md
  - raw/docs.allunite.com/Analytics Documentation/Metrics Terminology.md
related:
  - entities/repo-jobs.md
  - methodologies/total-traffic-modelling.md
  - methodologies/ds-workflow.md
  - concepts/total-traffic.md
  - concepts/impression.md
  - systems/recalc-ch.md
updated: 2026-04-21
status: stable
---

# ML Traffic Prediction Job

The ML Traffic Prediction job (`ml_traffic_prediction/main.py`) is the core runnable job for computing Total Traffic per facility per hour and associated impression metrics.

**Repository:** `github.com/allunite/jobs/blob/master/ml_traffic_prediction/main.py`

## What It Does

1. **Total Traffic by Sessions:** Iterates over saved ML models, loads session data from `clickhouse/device_session`, applies models, writes results to `clickhouse/device_session_agg_ml_2`.
2. **Multi-source mirroring:** Estimates traffic for non-sensor facilities using `traffic_multisource_mirroring.py`.
3. **Dwell Time calculation** (V2 for new companies): `add_hourly_med_dwell_time_V2()`.
4. **Impressions job** (`impressions.py`): Reads Total Traffic and Dwell Time from `clickhouse/device_session_agg_ml_2`, Facility Traffic Share and VA from `postgres/ml_job_param_overrides`, frame params from PostgreSQL. Calculates Viewable and Viewed Impressions. [^1]

## Key Parameters (env vars)

- `CH_HOST`, `CH_USER`, `CH_PASSWORD` — ClickHouse connection
- `PG_HOST`, `PG_USER`, `PG_PASSWORD` — PostgreSQL connection
- `S3_FOLDER` — prod/stage model folder
- `MODEL_ENVIRONMENT` — prod/stage/beta
- `DATASET_TARGET` — output dataset (model1)
- `DATE_START`, `DATE_END` — processing window
- `ML_MODEL_COMPANY_NUMS` — comma-separated company list (empty = all)
- `ROLLBAR_ENVIRONMENT` — use `manual` for local runs [^1]

## Orchestration

Job is scheduled and run via Rundeck (`rundeck.allunite.local`). Manual recalculation job: "ML Traffic prediction with parameters". [^1]

[^1]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md, 2026-04-21
