---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Mirroring"
type: source
tags: [data-science, mirroring, traffic]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Mirroring.md
updated: 2026-04-21
status: stable
---

# Source: Mirroring

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Mirroring.md`

## Summary

Basic mirroring: copies sessions from facilities with sensors to facilities without sensors. Connections stored in `postgresql/facility_virtual`, `postgresql/v_ch_facility_virtual`, `clickhouse/facility_virtual_dict`, `postgresql/v_facility_asset`, `clickhouse/_v_facility_asset`. Has `traffic_factor` column.

See [multi-source-mirroring.md](../methodologies/multi-source-mirroring.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Mirroring.md` 2026-04-21
