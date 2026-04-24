---
title: Monitoring Systems
type: system
tags: [infrastructure, monitoring, victoriametrics, alertmanager, grafana, routers]
sources:
  - raw/docs.allunite.com/Infrastructure/Monitoring.md
  - raw/docs.allunite.com/Operations/Operation tools/Monitoring.md
related:
  - systems/aws.md
updated: 2026-04-21
status: stable
---

# Monitoring Systems

AllUnite runs two monitoring systems, both using **VictoriaMetrics** (Prometheus-like) for metrics and **Alertmanager** for notifications. They cross-monitor each other via heartbeat checks.

## Infrastructure Monitoring

Covers servers, databases, and network devices. Alerts routed via internal messaging; critical incidents escalated via SMS and phone calls to on-call team. [^1]

## Router and Data Monitoring

Monitors WiFi sensor routers across all deployments. Three data sources: database polling (checks data delivery), Teltonika RMS (checks router connectivity), internal metrics gathering platform. [^1]

Notification chain:
- Ops team notified via internal messaging on issues
- Grafana dashboard at `boxmon.allunite.local/grafana/d/ed884e90-c4c1-40e0-98ce-f040858fcfd1/devices-status` for real-time status (VPN required) [^2]
- Daily job sends email to customers listing offline routers
- Daily anomaly detection job triggers Alertmanager alerts on unexpected data patterns

[^1]: raw/docs.allunite.com/Infrastructure/Monitoring.md, 2026-04-21
[^2]: raw/docs.allunite.com/Operations/Operation tools/Monitoring.md, 2026-04-21
