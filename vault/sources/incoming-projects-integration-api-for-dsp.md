---
title: "Source: Incoming Projects / Integration API for DSP"
type: source
tags: [incoming-projects, dsp, api, doohclick, proof-of-play, programmatic]
sources:
  - raw/docs.allunite.com/Incoming Projects/Integration API for DSP.md
updated: 2026-04-21
status: draft
---

# Source: Integration API for DSP

**Raw path:** `raw/docs.allunite.com/Incoming Projects/Integration API for DSP.md`

## Summary

Spec for AllUnite DSP integration API (initial partner: DOOHClick; future: Broadsign and others). Asynchronous design (job IDs with polling). Flow: frame ID linking → DSP sends preliminary campaign data (frames, period, demographics) → AllUnite responds with forecasted metrics (Impressions, Reach, VAC) → DSP sends booked campaign → DSP sends Proof of Play on completion → AllUnite sends follow-up report.

Planned endpoints:
- `GET /frames` — frame list with external_id
- `PUT /frames/[frame_id]` — update frame attributes (TBD)
- `POST /campaigns` — create campaign, returns job_id
- `POST /campaigns/[id]/book` — confirm/lock campaign
- `POST /campaigns/[id]/finish` — mark campaign finished
- `POST /campaigns/[external_id]/pop` — upload Proof of Play (fields: frame_id, timestamp, duration)
- `GET /jobs/[id]/status` — check job status (queued/processing/done/failed)
- `GET /jobs/[id]/results` — retrieve job results (JSON)

Sources: `raw/docs.allunite.com/Incoming Projects/Integration API for DSP.md` 2026-04-21
