---
title: PostgreSQL
type: system
tags: [infrastructure, database, postgresql, backup, terraform]
sources:
  - raw/docs.allunite.com/Infrastructure/Postgresql Backups and Recovery.md
  - raw/docs.allunite.com/Generic/Onboarding/Data team onboarding.md
related:
  - systems/aws.md
updated: 2026-04-21
status: stable
---

# PostgreSQL

AllUnite's primary relational database. Hosts application data including inventory, ML model metadata, manual counting data, and dataset version tracking.

## Key Tables

- `ml_model` — ML model registry
- `manual_counting` / `v_ch_manual_counting_extended` — manual traffic count records
- `device_session_agg_version` — dataset version tracking
- `box_versions` — sensor hardware history by MAC address or facility_id [^2]

## Backup and Recovery

Backups via AWS Data Lifecycle Manager using EBS Volume snapshots. Retention: 7 daily + 30 weekly. [^1]

Restore procedure:
1. Checkout `server-configs` repo → `terraform/master/layers/data`
2. Create `terraform.tfvars` with `restored_db_active = true` and the snapshot ID
3. Run `terraform apply` → restored DB at `restored-db.allunite.local`
4. Cleanup: set `restored_db_active = false`, re-run `terraform apply`

[^1]: raw/docs.allunite.com/Infrastructure/Postgresql Backups and Recovery.md, 2026-04-21
[^2]: raw/docs.allunite.com/Operations/DataBase query.md, 2026-04-21
