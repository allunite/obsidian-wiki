---
title: "Source: Generic / Onboarding / Data Team Onboarding"
type: source
tags: [generic, onboarding, data-team, access, tools]
sources:
  - raw/docs.allunite.com/Generic/Onboarding/Data team onboarding.md
updated: 2026-04-21
status: stable
---

# Source: Data Team Onboarding

**Raw path:** `raw/docs.allunite.com/Generic/Onboarding/Data team onboarding.md`

## Summary

Data team onboarding checklist. Required accesses: VPN (`files.allunite.local/web/client/files`), Analytics (prod/staging/beta), ClickHouse (test: `select * from company_dict where country = 'Finland'`), PostgreSQL (test: `select * from ml_model order by id asc`), Rollbar, GitHub (`allunite/jobs`, `allunite/ml-api`, `allunite/data-science`), Clockify (create "onboarding" entry). Tools: PyCharm + Jupyter for Python, DataGrip for DB. Key GitHub branches: `template_scripts` (common scripts), `jobs/stage/ml_traffic_prediction` (traffic/impressions), data agg script, ds_copy script. Key ClickHouse tables: `raw_devices_seen_2`, `device_session`, `device_session_agg_ml_2`, `device_session_agg_5`, `company_dict`, `facility_dict`, `frame_dict`, `_v_facility_asset`. Key PostgreSQL tables: `ml_model`, `manual_counting`, `v_ch_manual_counting_extended`, `device_session_agg_version`.

Sources: `raw/docs.allunite.com/Generic/Onboarding/Data team onboarding.md` 2026-04-21
