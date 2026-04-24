---
title: "Source: Inbox / Models Storage"
type: source
tags: [inbox, aws, s3, models, ml, sftpgo]
sources:
  - raw/docs.allunite.com/Inbox/Models storage.md
updated: 2026-04-21
status: draft
---

# Source: Models Storage

**Raw path:** `raw/docs.allunite.com/Inbox/Models storage.md`

## Summary

ML model file storage: web interface at `files.allunite.local/web/client/login` (sign in with OpenID using allunite.com credentials). Backend: sftpgo service using S3 bucket `allunite-models`. Script/programmatic access via WebDAV at `https://files.allunite.local/dav`, credentials: login `models`, password `models` (no aws-mfa needed for this path).

Sources: `raw/docs.allunite.com/Inbox/Models storage.md` 2026-04-21
