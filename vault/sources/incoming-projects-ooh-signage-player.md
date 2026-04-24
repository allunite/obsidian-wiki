---
title: "Source: Incoming Projects / OOH Signage Player"
type: source
tags: [incoming-projects, signage-player, dooh, raspberry-pi, proof-of-play]
sources:
  - raw/docs.allunite.com/Incoming Projects/OOH Signage Player.md
updated: 2026-04-21
status: draft
---

# Source: OOH Signage Player

**Raw path:** `raw/docs.allunite.com/Incoming Projects/OOH Signage Player.md`

## Summary

PoC for an AllUnite-managed DOOH signage player. Campaign lifecycle: Campaign Manager → Active status → content on screen. Parameters: 10s slot duration, 90s loop duration (40 loops/hour). Fixed slots (no Dynamic Slot Allocation for PoC). Proof of Play: real-time, fields: timestamp (end of display), Campaign ID, Creative ID, Frame ID, duration. Player polls server every 5 minutes for next-hour schedule; pre-downloads creatives. Hardware: Teltonika RUT200 router + Raspberry Pi (HDMI to screen, Ethernet to router). Media: video and images (no HTML for MVP). Ideas: MQTT for real-time PoP; screenshot monitoring; Dynamic Slot Allocation by demographics. Reference implementations: Screenly/Anthias, obscreen/obscreen.

Sources: `raw/docs.allunite.com/Incoming Projects/OOH Signage Player.md` 2026-04-21
