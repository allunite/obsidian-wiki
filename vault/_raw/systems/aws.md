---
title: AWS Infrastructure
type: system
tags: [infrastructure, aws, cloud, storage, backup]
sources:
  - raw/docs.allunite.com/Infrastructure/AWS Access.md
related:
  - systems/monitoring.md
updated: 2026-04-21
status: stable
---

# AWS Infrastructure

AllUnite uses AWS for cloud storage (S3 for ML models) and PostgreSQL backup via EBS snapshots.

## Access

Sign-in URL: `allunite.signin.aws.amazon.com/console`. MFA is required (Google Authenticator). IAM account ID: `475333150727`.

CLI setup:
1. Install `awscliv2` and `aws-mfa`
2. Add credentials to `~/.aws/credentials` under `[default-long-term]` with `aws_access_key_id`, `aws_secret_access_key`, `aws_mfa_device`
3. Run `aws-mfa` with OTP to activate a session

## Services Used

- **S3** — ML model storage (`models_storage` bucket; see methodology pages)
- **EBS Snapshots** — PostgreSQL backup via Data Lifecycle Manager (7 daily + 30 weekly)

[^1]: raw/docs.allunite.com/Infrastructure/AWS Access.md, 2026-04-21
