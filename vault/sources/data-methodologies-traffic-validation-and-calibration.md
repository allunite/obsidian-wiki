---
title: "Source: Data Methodologies / Traffic Validation and Calibration"
type: source
tags: [data-science, calibration, validation, manual-counting]
sources:
  - raw/docs.allunite.com/Data methodologies/Traffic validation and calibration.md
updated: 2026-04-21
status: stable
---

# Source: Traffic Validation and Calibration

**Raw path:** `raw/docs.allunite.com/Data methodologies/Traffic validation and calibration.md`

## Summary

Process overview for calibrating AllUnite sensors using manual counting. Steps: select sample locations per category, create counting instructions (map with red lines), representative counts with clicker app for 1h × 2 sessions. MC formula: Total = Pedestrians + 1.4×Cars + 15×Buses + 15×Trams + 50×Trains. Dataset split into training/validation. OLS regression with R² and MAPE metrics. Validation every 6–12 months.

See [sensors-calibration.md](../methodologies/sensors-calibration.md), [wifi-methodology.md](../methodologies/wifi-methodology.md).

Sources: `raw/docs.allunite.com/Data methodologies/Traffic validation and calibration.md` 2026-04-21
