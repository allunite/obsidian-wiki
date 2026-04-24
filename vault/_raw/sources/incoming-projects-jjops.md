---
title: "Source: Incoming Projects / JJOps"
type: source
tags: [incoming-projects, joe-and-the-juice, client, monitoring, operations]
sources:
  - raw/docs.allunite.com/Incoming Projects/JJOps.md
updated: 2026-04-21
status: draft
---

# Source: JJOps

**Raw path:** `raw/docs.allunite.com/Incoming Projects/JJOps.md`

## Summary

Project: helper application for Joe&TheJuice operations (monitoring, alerting, location management). Context: AllUnite provides network support (monitoring, ISP management, hardware installation/config) for 350+ J&J locations worldwide. Three hardware generations: (1) TP-Link 3600 + Unifi AP (~250 locations, Icinga2 monitoring), (2) Teltonika M08 + Unifi U7 Pro (~100 locations, Teltonika RMS + Unifi Controller), (3) Unifi Cloud Gateway + Switch + U7 Pro (new standard). Location list API: `joepay-api.joejuice.com/me/stores` (sync every 5 minutes). Required tracking: hardware setup + MAC addresses, ISP line info (contracts, credentials, speed, config), landlord contacts, location contacts, installation photos/documents, billing info. Future: Jira ticket integration, uptime display, LTE failover detection, Google Chat alerts with pause capability.

See [clients/joe-and-the-juice.md](../clients/joe-and-the-juice.md).

Sources: `raw/docs.allunite.com/Incoming Projects/JJOps.md` 2026-04-21
