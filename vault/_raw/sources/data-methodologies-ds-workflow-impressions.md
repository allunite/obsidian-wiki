---
title: "Source: Data Methodologies / DS Workflow / Impressions"
type: source
tags: [data-science, impressions, methodology]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Impressions.md
updated: 2026-04-21
status: stable
---

# Source: Impressions Methodology

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Impressions.md`

## Summary

Impressions job (`impressions.py`) calculates Viewable and Viewed Impressions. Inputs: Total Traffic + Dwell Time from `clickhouse/device_session_agg_ml_2`; Facility Traffic Share + VA from `postgres/ml_job_param_overrides`; frame params from PostgreSQL. Parameters via env vars (include CH_HOST, PG_HOST, ML_MODEL_COMPANY_NUMS, date range). Old impressions for a few legacy companies calculated differently in Traffic job — not enabled for new companies.

See [ds-workflow.md](../methodologies/ds-workflow.md), [ml-traffic-prediction.md](../systems/ml-traffic-prediction.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Impressions.md` 2026-04-21
