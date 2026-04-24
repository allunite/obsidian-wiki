---
title: Sensors Calibration
type: methodology
tags: [data-science, sensors, calibration, traffic, wifi]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Sensors calibration.md
  - raw/docs.allunite.com/Data methodologies/Traffic validation and calibration.md
  - raw/docs.allunite.com/Data methodologies/WiFi methodology.md
related:
  - methodologies/total-traffic-modelling.md
  - methodologies/ds-workflow.md
  - methodologies/wifi-methodology.md
  - concepts/total-traffic.md
updated: 2026-04-21
status: stable
---

# Sensors Calibration

The goal of calibration is to find coefficients that convert raw sensor session counts into accurate traffic estimates, validated against manual counts (MC). [^1]

## Manual Counting (MC)

Select sample locations per environment category (Roadside, Mall, Metro, etc.). Representatives count all people, cars, buses crossing defined lines during 1-hour sessions (2 per location). MC data is verified with Operations for correct UTC conversion and multi-counter summation. [^2]

Standard MC coefficients: cars=1.4, buses=25, trains=50, pedestrians/bicycles/motorcycles=1.0. [^1]

## Modelling Steps

1. **Data collection:** `get_sessions()` / `get_sessions2()` from ClickHouse `device_session` table.
2. **Dataset preparation:** `collect_dataset()` / `collect_dataset2()` — merge sensor data with MC values; fill NaN/inf with 0.
3. **Model training:** OLS regression. Target: MAPE < 25%. Grid search on feature/hyper-parameter space.
4. **Model naming convention:** `{Country}_{Company}_{Category}_{target_column}_{coef}_sl{}.joblib`
5. **Upload:** AWS S3 bucket (prod/stage), update `postgres/ml_model` table.
6. **Signal level calibration:** Default `sl=89` for outdoor, `sl=78` for indoor (Mall, Attraction).
7. **Apply to history** (stage/alternative dataset only — never production directly).
8. **Validation:** Run validation script; review MAPE and signal level/category handling.
9. **Move to production** after approval; enable model in `ml_model` table (`disabled=False`). [^1]

## Current Accuracy

94% ± 5% on validation dataset with AllUnite sensors. [^3]

[^1]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Sensors calibration.md, 2026-04-21
[^2]: raw/docs.allunite.com/Data methodologies/Traffic validation and calibration.md, 2026-04-21
[^3]: raw/docs.allunite.com/Data methodologies/WiFi methodology.md, 2026-04-21
