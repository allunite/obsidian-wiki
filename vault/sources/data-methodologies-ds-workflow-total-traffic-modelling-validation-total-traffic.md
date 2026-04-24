---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Validation Total Traffic"
type: source
tags: [data-science, traffic, validation]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Validation Total Traffic.md
updated: 2026-04-21
status: stable
---

# Source: Validation Total Traffic

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Validation Total Traffic.md`

## Summary

Validation script `validation_traffic_review.ipynb` parameters: country_names, company_names, company_blacklist, categories, dataset, date range. Outputs: report + DataFrames (df_facilities, df_metrics_daily, df_metrics). Report sections: general info, inventory info, basic traffic stats, hourly NaN/zero/negative flags, traffic vs. sessions consistency matrix (good/bad), hourly vs. daily aggregate check, agg_5 vs. ml_2 comparison.

See [total-traffic-modelling.md](../methodologies/total-traffic-modelling.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Validation Total Traffic.md` 2026-04-21
