---
title: Total Traffic Modelling
type: methodology
tags: [data-science, traffic, ml, modelling]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Global Model.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Validation Total Traffic.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Special case in Brazil.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Traffic trend adjustment.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Proximity traffic modelling.md
related:
  - methodologies/sensors-calibration.md
  - methodologies/multi-source-mirroring.md
  - methodologies/ds-workflow.md
  - concepts/total-traffic.md
  - systems/ml-traffic-prediction.md
updated: 2026-04-21
status: stable
---

# Total Traffic Modelling

## Total Traffic by Sessions (Primary Method)

The most basic method: applies calibrated ML models to sensor session data to predict Total Traffic per facility per hour. Implemented in `ml_traffic_prediction/main.py`. [^1]

**Script flow:** Iterate over saved models → for each model/company/category, load model, create features from `clickhouse/device_session`, apply model, write traffic to `clickhouse/device_session_agg_ml_2`. [^1]

**Parameters** (env vars): `CH_HOST`, `PG_HOST`, `S3_FOLDER` (prod/stage), `MODEL_ENVIRONMENT`, `DATASET_TARGET`, date range, `ML_MODEL_COMPANY_NUMS`, `ML_MODEL_CATEGORIES`. [^1]

**Known issue:** Reproducibility is affected by inventory changes (adding/removing/changing facilities/sensors impacts historical recalculations). [^1]

## Global Model

For new facilities/deployments without sensor data. Predicts Average Daily Total Traffic and Confidence score using features from OSM and ESRI. Weekly seasonality patterns and dwell time values are taken from existing clients with similar environments. [^2]

**Activation steps:** Fill inventory → enable `company.enableMlStaticMetrics` → fill static seasonality in `ml_job_param_overrides` → set `global_traffic_version` → set forced VA and facility_traffic_share → enable impressions → enable visit frequency → enable new Reach. [^2]

**Default inventory parameters:** category=Roadside, 1 frame/facility, width=1.2m, height=1.8m, movement=DD, loop_duration=60s, insertion_duration=10s, total_insertions=6. [^2]

## Validation

Traffic validation uses `validation_traffic_review.ipynb`. Key checks: NaN/negative/zero traffic flags, traffic vs. sessions consistency matrix (good/bad/ambiguous cases), hourly vs. daily aggregate consistency, comparison of `device_session_agg_5` vs. `device_session_agg_ml_2`. [^3]

[^1]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Total Traffic by sessions.md, 2026-04-21
[^2]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Global Model.md, 2026-04-21
[^3]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Validation Total Traffic.md, 2026-04-21
