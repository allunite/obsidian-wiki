---
title: Inbox
type: overview
tags: [inbox, drafts, ideas, incoming-projects]
updated: 2026-04-21
status: draft
---

# Inbox

Unfiled items: draft raw docs, concepts mentioned without dedicated pages, contradictions, candidate pages, follow-ups.

## Unfiled Drafts

### Ideas

- **Chatbot framework** — Python multi-backend chatbot with LLM + MCP integration. Source: [ideas-chatbot.md](sources/ideas-chatbot.md)
- **Creatives update** — video/image preview in platform, S3 storage, CMS integration. Source: [ideas-creatives-update.md](sources/ideas-creatives-update.md)
- **DS ideas** — data validation Jupyter notebook, impressions UI, Finland multi-source mirroring, dwell-time for virtual locations, frequency modelling improvements. Source: [ideas-ds-ideas.md](sources/ideas-ds-ideas.md)

### Inbox

- **Copy sessions for virtual facilities** — SQL scripts to backfill historical sessions into virtual facility records. Source: [inbox-copy-sessions-for-virtual-facilities.md](sources/inbox-copy-sessions-for-virtual-facilities.md)
- **Enable forecast** — task note: enable forecast on facility 44296, company 7957. Source: [inbox-enable-forecast.md](sources/inbox-enable-forecast.md)
- **Fill connected factor in _v_facility_asset** — update `facility_virtual` table directly; recommendation to retire `_v_facility_asset`. Source: [inbox-how-to-fill-connected-factor.md](sources/inbox-how-to-fill-connected-factor.md)
- **Models storage** — sftpgo + S3 `allunite-models` bucket; WebDAV access at `files.allunite.local/dav`. Source: [inbox-models-storage.md](sources/inbox-models-storage.md)

### Incoming Projects

- **Ad Server Integration Guide** — captive portal ad server redirect flow spec. Source: [incoming-projects-ad-server-integration-guide.md](sources/incoming-projects-ad-server-integration-guide.md)
- **Bundles and Offers Proposal** — replace Package concept with Bundle + Offer; deprecate Combined Campaigns. Source: [incoming-projects-bundles-and-offers.md](sources/incoming-projects-bundles-and-offers.md)
- **DSP** — OpenRTB 2.x DSP integration stub. Source: [incoming-projects-dsp.md](sources/incoming-projects-dsp.md)
- **Financials KPI** — revenue/cost calculations for campaigns. Source: [incoming-projects-financials-kpi.md](sources/incoming-projects-financials-kpi.md)
- **Integration API for DSP** — async job-based API spec for DOOHClick integration (campaigns, Proof of Play, forecasts). Source: [incoming-projects-integration-api-for-dsp.md](sources/incoming-projects-integration-api-for-dsp.md)
- **JJOps** — Joe&TheJuice operations helper app (monitoring, ISP management, location tracking). Source: [incoming-projects-jjops.md](sources/incoming-projects-jjops.md)
- **MotionWorks Questions** — due diligence questionnaire for prospective data partner. Source: [incoming-projects-motionworks-questions.md](sources/incoming-projects-motionworks-questions.md)
- **New VPN** — netbird.io-based VPN to replace WireGuard. Source: [incoming-projects-new-vpn.md](sources/incoming-projects-new-vpn.md)
- **OOH Signage Player** — AllUnite-managed DOOH player on Raspberry Pi + RUT200; Proof of Play; PoC spec. Source: [incoming-projects-ooh-signage-player.md](sources/incoming-projects-ooh-signage-player.md)
- **OOH Terminology** — minimal DSP/SSP/CPM glossary stub. Source: [incoming-projects-ooh-terminology.md](sources/incoming-projects-ooh-terminology.md)
- **RMS Alternative** — vendor-agnostic MQTT-based router management. Source: [incoming-projects-rms-alternative.md](sources/incoming-projects-rms-alternative.md)
- **Data-API Unique Traffic Endpoint** — spec for `POST /v1/reports/traffic/unique`. Source: [incoming-projects-data-api-unique-traffic.md](sources/incoming-projects-data-api-unique-traffic.md)
- **Traffic Analytics Solution - Video** — exploratory CCTV-based traffic analytics (3 options). Source: [incoming-projects-traffic-analytics-video.md](sources/incoming-projects-traffic-analytics-video.md)

## Candidate Concept Pages

- **Virtual Facility** — a facility that mirrors sessions from a physical sensor facility via `facility_virtual_dict`. Referenced in multiple sources but no dedicated page yet.
- **Proof of Play** — timestamp + campaign/creative/frame/duration record sent by signage player after ad is shown. Referenced in OOH Signage Player and DSP integration specs.
- **Bundle / Offer** — proposed replacements for Package concept (see Bundles and Offers Proposal).
- **Captive Portal** — WiFi hotspot captive portal; ad server integration; session analytics. Referenced in release notes and Incoming Projects.

## ClickUp Knowledge Hub Items (Sales Space)

Sourced from `Improvements & Ideas Pipeline` list (`901511321430`). 10 items; selected:

1. Create screen-recording instruction videos for new pipeline
2. Develop Combined Campaign Results (urgent)
3. Create slides on AllUnite Methodology
4. AllUnite Clientele Knowledge Base
5. Methodology and Glossary Hub — multi-language versions
6. Global/standard pricing
7. Travel Policy Implementation
8. Company-wide newsletter
9. Knowledge hub
10. Various sales process/pipeline improvements

[clickup:list/901511321430]

---

## Contradictions Flagged

- **Release 9 date mismatch:** Docs say `v2026.03.02`; ClickUp list name is `Release 9 - v2026-03-10`. See [release-timeline.md](release-timeline.md).
- **Release 2 (v2025.06.10):** ClickUp list `901512928320` has 0 tasks — may predate ClickUp tracking.

## Follow-ups

- `_v_facility_asset` view: source recommends retiring it; confirm with Data team.
- Combined Campaigns deprecation: Bundles and Offers Proposal planned to supersede this; update concepts/campaign.md when decision is final.
- MotionWorks: unclear if prospective partner or acquisition; clarify context.
