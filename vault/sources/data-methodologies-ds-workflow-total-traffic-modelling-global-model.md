---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Global Model"
type: source
tags: [data-science, traffic, global-model]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Global Model.md
updated: 2026-04-21
status: stable
---

# Source: Global Model

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Global Model.md`

## Summary

Static seasonality global model for new facilities without sensors. Predicts Average Daily Total Traffic and Confidence using OSM/ESRI features. Weekly seasonality applied on top. Default inventory: Roadside, 1 frame, width=1.2m, height=1.8m, DD movement, 60s loop, 10s insertion, 6 insertions. 8-step manual activation checklist. Calculation flow: Global Model batch job → Traffic job → Impressions job.

See [total-traffic-modelling.md](../methodologies/total-traffic-modelling.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Global Model.md` 2026-04-21
