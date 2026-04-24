---
title: DS Workflow
type: methodology
tags: [data-science, workflow, traffic, impressions]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Preparation before project.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Dwell time.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Impressions.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Facility Traffic Share & Visibility Adjustment.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling.md
related:
  - methodologies/total-traffic-modelling.md
  - methodologies/sensors-calibration.md
  - methodologies/multi-source-mirroring.md
  - concepts/total-traffic.md
  - concepts/impression.md
  - concepts/dwell-time.md
  - systems/ml-traffic-prediction.md
updated: 2026-04-21
status: stable
---

# DS Workflow

The DS Workflow describes the standard steps for a Data Science project at AllUnite, from pre-project preparation through traffic modelling, calibration, impression calculation, and delivery.

## 1. Preparation Before Project

Before starting, a DS must: verify system access and git repo access; identify the PM (primary client contact point); read the project transfer doc (ClickUp home page); check inventory (facilities, sensors, facility_dict); confirm deliverables (modelled facilities, mirrored facilities, campaign manager, demographics); create a project communication chat with PM, ops, Data Delivery Lead, CDO. [^1]

Discuss with PM: client-provided data, 3rd-party data plans, demographics requirements.
Discuss with Ops: inventory completeness, virtual facility linking, timezone, categories, clusters. [^1]

## 2. Total Traffic Modelling

Several approaches depending on facility sensor status:
- **Total Traffic by Sessions** — primary method; applies calibrated ML models to session data. See [total-traffic-modelling.md](total-traffic-modelling.md).
- **Mirroring** — copies sessions from sensor facilities to non-sensor facilities. See [multi-source-mirroring.md](multi-source-mirroring.md).
- **Global Model** — for new deployments without sensor data; uses static seasonality and avg daily traffic predictions from OSM/ESRI features.

## 3. Dwell Time

Three versions of dwell time calculation exist in `ml_traffic_prediction`:

- **Old version** (default unless `use_old_dwell_time: False`): `medianIf` from `device_session_trusted`.
- **V1** (deprecated): more advanced but should not be used for new companies.
- **V2** (current, recommended for new companies): `add_hourly_med_dwell_time_V2` — 9-step pipeline including session filtering (excludes devices with ≥4h daily sessions or ≥5 distinct hours), quality gates, category-hour median gap filling, outlier handling. Requires `use_old_dwell_time: False` and `dashboard.useModelledDwellTime = True` in company settings. [^2]

## 4. Impressions

Impressions (Viewable and Viewed) are calculated by the Impression job (`ml_traffic_prediction/impressions.py`). Inputs: Total Traffic and Dwell Time from `clickhouse/device_session_agg_ml_2`, Facility Traffic Share and VA defaults from `postgres/ml_job_param_overrides`, frame parameters from PostgreSQL. [^3]

## 5. Facility Traffic Share and Visibility Adjustment

Both can be sourced from: (1) hard-coded company values in Impressions job, (2) `postgres/ml_job_param_overrides` (company/frame level), or (3) calculated by ML-API. [^4]

[^1]: raw/docs.allunite.com/Data methodologies/DS Workflow/Preparation before project.md, 2026-04-21
[^2]: raw/docs.allunite.com/Data methodologies/DS Workflow/Dwell time.md, 2026-04-21
[^3]: raw/docs.allunite.com/Data methodologies/DS Workflow/Impressions.md, 2026-04-21
[^4]: raw/docs.allunite.com/Data methodologies/DS Workflow/Facility Traffic Share & Visibility Adjustment.md, 2026-04-21
