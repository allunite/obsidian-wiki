---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Sensors Calibration"
type: source
tags: [data-science, sensors, calibration]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Sensors calibration.md
updated: 2026-04-21
status: stable
---

# Source: Sensors Calibration

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Sensors calibration.md`

## Summary

Full MC-to-prod calibration pipeline: MC preparation (UTC verification, multi-counter summation), `get_sessions`/`collect_dataset` utility functions, Modelling.ipynb notebook (grid search, MAPE target < 25%), model upload to S3 with naming convention `{Country}_{Company}_{Category}_{target}_{coef}_sl{}.joblib`, signal level defaults (sl=89 outdoor, sl=78 indoor), history application on stage dataset, validation, production deployment.

See [sensors-calibration.md](../methodologies/sensors-calibration.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Sensors calibration.md` 2026-04-21
