---
title: "Source: Inbox / Copy Sessions for Virtual Facilities in the Past"
type: source
tags: [inbox, clickhouse, virtual-facility, sql, data-ops]
sources:
  - raw/docs.allunite.com/Inbox/Copy sessions for virtual facilities in the past.md
updated: 2026-04-21
status: draft
---

# Source: Copy Sessions for Virtual Facilities in the Past

**Raw path:** `raw/docs.allunite.com/Inbox/Copy sessions for virtual facilities in the past.md`

## Summary

Operational task/script: when a virtual facility mapping is set up after data collection has started, backfill historical sessions from source facilities into the virtual facility's records. Two SQL steps: (1) INSERT into `allunite.device_session` selecting from existing `device_session` joined with `facility_virtual_dict`, setting `is_virtual=1`; (2) INSERT into `device_session_trusted` for the trusted subset. Example target: company_num 7885, facility_master_num 43975, date range 2025-01-23 to 2025-04-04.

Sources: `raw/docs.allunite.com/Inbox/Copy sessions for virtual facilities in the past.md` 2026-04-21
