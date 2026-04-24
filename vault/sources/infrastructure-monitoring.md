---
title: "Source: Infrastructure / Monitoring"
type: source
tags: [infrastructure, monitoring, victoriametrics, alertmanager, grafana]
sources:
  - raw/docs.allunite.com/Infrastructure/Monitoring.md
updated: 2026-04-21
status: stable
---

# Source: Infrastructure Monitoring

**Raw path:** `raw/docs.allunite.com/Infrastructure/Monitoring.md`

## Summary

Two monitoring systems, both using VictoriaMetrics + Alertmanager:

**Infrastructure Monitoring:** Covers servers, databases, network devices. Alerts via internal messaging; critical incidents escalated via SMS and phone calls.

**Router and Data Monitoring:** Tracks router health and data integrity. Data sources: database polling (checks routers are sending data), Teltonika RMS (router accessibility), internal metrics platform. Notifications: ops team via messaging; Grafana dashboard for real-time router status across all companies. Daily automated job sends email to customers about offline routers. Daily anomaly detection job via Alertmanager.

**Cross-monitoring:** The two systems monitor each other via heartbeat checks.

See [systems/monitoring.md](../systems/monitoring.md).

Sources: `raw/docs.allunite.com/Infrastructure/Monitoring.md` 2026-04-21
