---
title: Joe & The Juice
type: client
tags: [client, network, installation, unifi]
sources:
  - raw/docs.allunite.com/Joe&TheJuice/Installation Guide.md
  - raw/docs.allunite.com/Joe&TheJuice/Network policies.md
  - raw/docs.allunite.com/Operations/Joe&TheJuice.md
  - raw/docs.allunite.com/Operations/Joe&TheJuice/Add a device to Unifi Controller.md
related:
  - entities/analytics-platform.md
updated: 2026-04-21
status: stable
---

# Joe & The Juice

Joe & The Juice is a client of AllUnite with WiFi sensor installations across restaurant locations, managed via Ubiquiti UniFi network infrastructure.

## Hardware Standard

- Ubiquiti Cloud Gateway Max
- USW Pro Max 24 PoE
- U7 Pro Access Points [^2]

## Network Architecture (VLAN Summary)

| VLAN | Tag | Subnet | Purpose |
|------|-----|--------|---------|
| VLAN10-Backoffice | 10 | 192.168.10.0/29 | Admin/staff devices |
| VLAN20-PCI | 20 | 192.168.20.0/28 | Payment devices — isolated, all traffic logged |
| VLAN30-Services | 30 | 192.168.30.0/27 | TV, Audio, CCTV, auxiliary |
| VLAN40-Guests | 40 | 192.168.40.0/24 | Guest WiFi — client isolation, ports 80/443/53 only |

[^2]

## Installation Procedure (Summary)

1. Connect ISP modem to Gateway port 5.
2. Connect Gateway port 1 → Switch port 1 → AP on port 24.
3. Configure via `192.168.1.1` browser interface.
4. Name Gateway: `[MarketCountryCode]-[StoreID]-[StoreName]`.
5. Restore configuration from backup file (v1.4 config).
6. Adopt Switch and Access Points in UniFi Devices.
7. Configure PCI whitelist ACL rules (In/Out rules per device).
8. Create admin users via CSV upload; transfer ownership to client. [^1]

## Adding a Device to UniFi Controller

For Ubiquiti U7 Pro: SSH into device (`ubnt`/`ubnt`), run `set-inform http://unifi.allunite.com:8080/inform`, adopt in UniFi Devices at `unifi.allunite.com`. [^3]

## Network Policy Key Points

- Guest WiFi: "JJ-Guests" (VLAN40), open, 5/2 Mbps limit, 1-hour session timeout, content filtering (no streaming/torrents).
- PCI WiFi: "JJ-PCI" (VLAN20), hidden, WPA2/WPA3, MAC allowlist, highest QoS priority.
- Maintenance windows: outside business hours; AP reboot monthly (not all at once); 48h advance coordination.
- Equipment lifecycle: 5 years or end-of-support. 4-hour recovery RTO.
- Support tiers: L1 = Joe & The Juice IT; L1.5/L2 = AllUnite; L3 = Ubiquiti specialist. [^2]

[^1]: raw/docs.allunite.com/Joe&TheJuice/Installation Guide.md, 2026-04-21
[^2]: raw/docs.allunite.com/Joe&TheJuice/Network policies.md, 2026-04-21
[^3]: raw/docs.allunite.com/Operations/Joe&TheJuice/Add a device to Unifi Controller.md, 2026-04-21
