---
title: "Source: Data Methodologies / DS Workflow / Dwell Time"
type: source
tags: [data-science, dwell-time, methodology]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Dwell time.md
updated: 2026-04-21
status: stable
---

# Source: Dwell Time Methodology

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Dwell time.md`

## Summary

Three dwell time calculation versions in `ml_traffic_prediction`: Old (default, medianIf from device_session_trusted), V1 (deprecated, not for new companies), V2 (current, recommended — `add_hourly_med_dwell_time_V2` with 9-step pipeline). V2 uses `use_old_dwell_time: False` + `dashboard.useModelledDwellTime = True`. Finland-specific: company_nums [7863, 7864, 7865, 7905, 7906] share category-hour dwell time across companies.

See [ds-workflow.md](../methodologies/ds-workflow.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Dwell time.md` 2026-04-21
