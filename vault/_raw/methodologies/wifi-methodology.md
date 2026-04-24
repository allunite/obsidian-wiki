---
title: WiFi Methodology
type: methodology
tags: [wifi, sensors, data-collection, traffic]
sources:
  - raw/docs.allunite.com/Data methodologies/WiFi methodology.md
related:
  - methodologies/sensors-calibration.md
  - concepts/total-traffic.md
  - concepts/dwell-time.md
updated: 2026-04-21
status: stable
---

# WiFi Methodology

AllUnite Wi-Fi sensors detect all devices sending Wi-Fi probe requests (90–95% of all mobile phones depending on country). [^1]

## MAC Address Types

- **Universally administered (UAA):** Uniquely assigned by manufacturer (OUI prefix). Second-least-significant bit of first octet = 0. Example: `00:40:FD:xx:xx:xx`.
- **Locally administered (LAA):** Overridden by network admin (second-least-significant bit = 1). Ranges: x2-xx, x6-xx, xA-xx, xE-xx.
- **Trusted MAC addresses:** Broadcasted when connected to public Wi-Fi. [^1]

LAA ("randomized") MACs correlate strongly with total devices and dwell time. A calibration model transforms random MAC counts to people counts. [^1]

## Filtration Rules

- Exclude sessions with signal level below -74 dBm (far away or moving too fast).
- Exclude "permanent devices" (≥5 consecutive hours of probe requests — e.g. printers, smart bulbs, staff phones). [^1]

## Session Counting

Signals (MAC address, timestamp, signal level in dBm) are grouped into sessions. Session completes when no signal is detected for 15 minutes. [^1]

## Calibration / Validation

Manual counting every 6–12 months per environment category. Training/validation split. OLS regression using R² and MAPE metrics. Current accuracy: 94% ± 5%. [^1]

[^1]: raw/docs.allunite.com/Data methodologies/WiFi methodology.md, 2026-04-21
