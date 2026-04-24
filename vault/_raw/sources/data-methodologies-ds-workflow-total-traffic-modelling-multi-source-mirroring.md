---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Multi-Source Mirroring"
type: source
tags: [data-science, mirroring, traffic, osm]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multi-Source Mirroring - Tetiana's model.md
updated: 2026-04-21
status: stable
---

# Source: Multi-Source Mirroring

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multi-Source Mirroring - Tetiana's model.md`

## Summary

Detailed technical spec for multi-source mirroring. Selects n most similar sensor facilities using OSM feature vectors (road network, speed, amenities). Weights computed by `traffic_multisource_weights/`, applied by `traffic_multisource_mirroring.py`. Includes: daily run, historical recalculation, full rewrite (rewrite=True), and leave-one-out evaluation procedure for new companies/categories. IQR outlier handling with `del_outliers` flag.

See [multi-source-mirroring.md](../methodologies/multi-source-mirroring.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multi-Source Mirroring - Tetiana's model.md` 2026-04-21
