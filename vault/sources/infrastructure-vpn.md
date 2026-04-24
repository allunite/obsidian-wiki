---
title: "Source: Infrastructure / VPN"
type: source
tags: [infrastructure, vpn, wireguard, networking]
sources:
  - raw/docs.allunite.com/Infrastructure/VPN.md
updated: 2026-04-21
status: stable
---

# Source: VPN

**Raw path:** `raw/docs.allunite.com/Infrastructure/VPN.md`

## Summary

WireGuard VPN at `wg-us`. Key generation: `wg genkey | tee privatekey | wg pubkey > publickey` and `wg genpsk > preshared`. New peer: edit `/etc/wireguard/wg0.conf` and add new public and preshared key.

Sources: `raw/docs.allunite.com/Infrastructure/VPN.md` 2026-04-21
