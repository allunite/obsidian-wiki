---
title: Multi-Source Mirroring
type: methodology
tags: [data-science, traffic, mirroring, modelling]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Mirroring.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multi-Source Mirroring - Tetiana's model.md
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multisource Finland.md
related:
  - methodologies/total-traffic-modelling.md
  - methodologies/ds-workflow.md
  - concepts/total-traffic.md
  - concepts/linking-rules.md
updated: 2026-04-21
status: stable
---

# Multi-Source Mirroring

**Mirroring** estimates traffic for facilities without installed sensors by copying or weighting traffic from similar sensor-equipped facilities. [^1]

Basic connections between source and target facilities are stored in:
- `postgresql/facility_virtual`, `postgresql/v_ch_facility_virtual`
- `clickhouse/facility_virtual_dict`, `clickhouse/_v_facility_asset`

## Multi-Source Mirroring Algorithm

For each non-sensor facility, the system selects the *n* most similar sensor-equipped facilities within the same company and category. Similarity is measured using OSM-derived environmental features. [^2]

**Implementation:** `ml_traffic_prediction/traffic_multisource_weights/` (weights calculation) + `traffic_multisource_mirroring.py` (weights application).

### Weight Calculation

Configuration in `constants.py` (COMPANY_DICT) per company/category:
- `radius` — bounding box in degrees of lat/lon (~0.005–0.0075° = several hundred metres)
- `features` — subset of OSM attributes to compare (road network counts, speed attributes, amenities)
- `top_n` — number of source sensor facilities
- `del_outliers` — IQR-based outlier filtering

Features extracted from OSM: road counts per type, speed attributes, node geometry, amenity counts (parking, fuel, bus_station, school, hospital, mall). [^2]

### Weights Application

Load weights → load source traffic → join on `session_start_hour` and `facility_num_source` → normalize weights per target/hour → compute weighted traffic → merge with old predictions (new replaces old) → save to ClickHouse. Only current non-sensor facilities receive mirrored traffic. [^2]

### Multisource Finland

Finland-specific variant using OSM + Ramboll traffic data. Two components: (1) sensor pool selection by road type and city classification; (2) Ramboll-based correction via sigmoid function (midpoint ratio = 0.3 — below this threshold sensor estimates are trusted more). Exception: no Ramboll correction if a physical sensor is within 200m. [^3]

[^1]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Mirroring.md, 2026-04-21
[^2]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multi-Source Mirroring - Tetiana's model.md, 2026-04-21
[^3]: raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multisource Finland.md, 2026-04-21
