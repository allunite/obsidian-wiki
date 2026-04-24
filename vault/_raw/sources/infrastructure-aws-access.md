---
title: "Source: Infrastructure / AWS Access"
type: source
tags: [infrastructure, aws, access, mfa, cli]
sources:
  - raw/docs.allunite.com/Infrastructure/AWS Access.md
updated: 2026-04-21
status: stable
---

# Source: AWS Access

**Raw path:** `raw/docs.allunite.com/Infrastructure/AWS Access.md`

## Summary

AWS access setup for AllUnite. Sign-in URL: `allunite.signin.aws.amazon.com/console`. MFA required; uses Google Authenticator. Setup: first login → Security Credentials → Assign MFA device → Authenticator app. Access key creation: Security Credentials → Access keys → Create → Other. CLI prerequisites: `awscliv2` + `aws-mfa` tool. Credentials stored in `~/.aws/credentials` under `[default-long-term]` with `aws_access_key_id`, `aws_secret_access_key`, `aws_mfa_device` (ARN format: `arn:aws:iam::475333150727:mfa/<name>`). Activate session: run `aws-mfa` and enter OTP.

See [systems/aws.md](../systems/aws.md).

Sources: `raw/docs.allunite.com/Infrastructure/AWS Access.md` 2026-04-21
