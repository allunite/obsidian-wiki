---
title: "Source: Infrastructure / PostgreSQL Backups and Recovery"
type: source
tags: [infrastructure, postgresql, backup, recovery, aws, terraform]
sources:
  - raw/docs.allunite.com/Infrastructure/Postgresql Backups and Recovery.md
updated: 2026-04-21
status: stable
---

# Source: PostgreSQL Backups and Recovery

**Raw path:** `raw/docs.allunite.com/Infrastructure/Postgresql Backups and Recovery.md`

## Summary

PostgreSQL backup via AWS Data Lifecycle Manager using EBS Volume snapshots. Retention: last 7 daily + 30 weekly snapshots. Restore procedure: checkout `server-configs` repo → `terraform/master/layers/data` → create `terraform.tfvars` with `restored_db_active = true` and `restored_db_snapshot_id` → run `terraform apply` → restored DB available at `restored-db.allunite.local`. Cleanup: set `restored_db_active = false` and re-run `terraform apply`.

Sources: `raw/docs.allunite.com/Infrastructure/Postgresql Backups and Recovery.md` 2026-04-21
