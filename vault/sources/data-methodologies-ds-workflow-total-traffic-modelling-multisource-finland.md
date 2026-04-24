---
title: "Source: Data Methodologies / DS Workflow / Total Traffic Modelling / Multisource Finland"
type: source
tags: [data-science, finland, mirroring, ramboll]
sources:
  - raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multisource Finland.md
updated: 2026-04-21
status: stable
---

# Source: Multisource Finland

**Raw path:** `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multisource Finland.md`

## Summary

Finland-specific total traffic model for outdoor facilities without sensors. Two components: (1) OSM-based sensor pool selection and weighting by road type + city classification (Helsinki / largest cities / other); (2) Ramboll data correction via sigmoid function (midpoint=0.3). No Ramboll correction if physical sensor within 200m. Note: not yet automated, applied for May only (as of source writing).

See [multi-source-mirroring.md](../methodologies/multi-source-mirroring.md).

Sources: `raw/docs.allunite.com/Data methodologies/DS Workflow/Total Traffic modelling/Multisource Finland.md` 2026-04-21
