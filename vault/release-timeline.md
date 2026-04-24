---
title: Release Timeline
type: release
tags: [releases, changelog]
sources:
  - raw/docs.allunite.com/Release Notes/v2025.05.13.md
  - raw/docs.allunite.com/Release Notes/v2025.06.10.md
  - raw/docs.allunite.com/Release Notes/v2025.07.08.md
  - raw/docs.allunite.com/Release Notes/v2025.08.12.md
  - raw/docs.allunite.com/Release Notes/v2025.09.09.md
  - raw/docs.allunite.com/Release Notes/v2025.10.14.md
  - raw/docs.allunite.com/Release Notes/v2025.11.11.md
  - raw/docs.allunite.com/Release Notes/v2025.12.09.md
  - raw/docs.allunite.com/Release Notes/v2026.01.13.md
  - raw/docs.allunite.com/Release Notes/v2026.02.10.md
  - raw/docs.allunite.com/Release Notes/v2026.03.02.md
  - raw/docs.allunite.com/Release Notes/v2026.04.14.md
updated: 2026-04-21
status: stable
---

# Release Timeline

Chronological release log. Newest first. Compiled from `raw/docs.allunite.com/Release Notes/`.

---

## v2026.04.14

**Campaign Manager:** Campaign Sharing System (cross-company/user access control); Package suite (create from file); external ID field for campaign linking. **Inventory Manager:** Cross-company inventory editing (JIC "edit right" feature); Estimated Daily Traffic export; AI semantic validation for inventory data import (coordinates/geography checks); Sandbox inventory mode. **Traffic Analytics:** Admin interface for data team company params; VA column in traffic report by frames; Share of Time exact value input; Hidden Metrics — Unique Traffic and Total Traffic can be hidden per company settings. **General:** Environment label in UI; default values shown on company settings page; `company.enableDynamicVA` toggle added. [^12]

---

## v2026.03.02

**Campaign Manager:** Frames list search bar; full zone facility support in campaign manager; Dynamic VA company setting (enable/disable). **Inventory Manager:** Zone polygon view in Inventory Manager. **Traffic Analytics:** Network search in traffic panel; new data-API endpoint for aggregated unique traffic. **Improvements:** "Frame ID" renamed to "User Frame ID"; inactive facility exclusion setting; API standardization (camelCase); single-step import; data date restrictions. [^11]

---

## v2026.02.10

**Campaign Manager:** Customized monthly traffic report; improved frame importing with help buttons. **Inventory Manager:** Coverage Zone Management with impressions settings. **Traffic Analytics:** New data-API endpoints for unique traffic and aggregated data; Cyprus and Belgium demographics. **Company Management:** White labeling (custom logos via Company Details); user deletion and change tracking. **Improvements:** Cost calculation fixes; admins restricted from creating campaigns; Japan data privacy (hide 1-month prior data); Angular 21 upgrade; Media Owner filter in dashboard. [^10]

---

## v2026.01.13

**Campaign Manager:** Estimated Cost for campaigns (frame CPM × impressions / 1000 per frame); custom campaign report format (contact commercial team). **Inventory Manager:** Global Visibility Engine (automatic VA using OSM building/road data); cluster facility list view; cross-company tag access. **Traffic Dashboard:** Visibility of facilities actively contributing to metrics. **Improvements:** Singapore-specific frequency formula; UI updated to Material 3 "warming" color palette; API returns only active facilities by default. [^9]

---

## v2025.12.09

**Campaign Manager:** Background metrics calculation for better UX. **Inventory Manager:** Active/inactive/all facilities filter. **Traffic Dashboard:** "Save Filters" button (persists default filter state). **Company Management:** Extended company list/edit page; role and settings management for users. **Authentication:** Microsoft and Google authentication support added. **Data-API:** Comprehensive documentation updates; campaign create/update endpoints; deprecated legacy reports marked; webhook notification on campaign change. [^8]

---

## v2025.11.11

**Campaign Manager:** Package Management section (group packages for all-or-nothing sales); Campaign Sharing between users and linked companies; Dynamic Slot Duration improvements (flexible validation, user guidance). **Inventory Manager:** Virtual Facility auto-relining; technical image uploads via API. **Traffic Dashboard:** Frame-level traffic report. **Data:** UAE frequency formula + demographics; Costa Rica demographics update; `additional_consents` field in captive portal analytics. **Improvements:** Performance optimization (calculate on save); impersonation reset icon. [^7]

---

## v2025.10.14

**Campaign Manager:** Dynamic Slot Duration — custom slot settings per campaign. **Captive Portal:** Detailed user report for logged-in users. **Campaigns:** New reach-frequency logic in campaign reports. **Improvements:** Frame sector recalculation when height changes; building height editing for VA; campaign folder "All"; frame filtering improvements; environment/frame type config renamed. [^6]

---

## v2025.09.09

**New Reach calculation algorithm.** **Shared Mall metrics:** If a cluster (Mall) is shared between media owners, totals use all screens from all owners. **Improvements:** Demographics Engine refactored for easier data source integration; "Apply Filter" button introduced (metrics calculated on demand rather than on page open); hour filter for combined campaigns; package filters; campaign metrics recalculation enhanced; floor frame management for mobile facilities. **Bug fixes:** Viewable impressions in campaigns; Reach chart edge display. [^5]

---

## v2025.08.12

**Campaign Manager:** Campaign Simulation (scenario preview); "# Loops" metric in campaign reports; API for DSP integration; linked-company package access. **Inventory Manager (Transit v2):** Frames directly in inventory with Frames tab; admin/other tabs; mobile inventory role; vehicle zoom controls; zone categories. **Data:** New demographics provider and frequency formula; new Reach methodology in campaign total metrics. **Improvements:** Scheduling UX rework; filter reliability fixes; operation hours improvements; Ramboll segment corrections. [^4]

---

## v2025.07.08

**Buses Inventory System:** Major new module for bus, tram, and train inventory with dynamic facility creation. **Inventory Validation:** Separate validation page for inventory parameters. **New VA logic:** VA calculation now uses all nearby roads (not just those explicitly linked to a frame). **Improvements:** Demographic data visualization in campaign report; seed/share link loads all campaign data; filter autocomplete in traffic panel; pagination and Excel export improvements. [^3]

---

## v2025.06.10

**AI Assistant (beta):** Available to all customers for metrics/methodology questions. **Campaign Report PDF export.** **Traffic Dashboard:** City filter autocomplete. **Hourly Impression Multipliers report** (some clients). **API Keys management.** **Improvements:** Performance improvements across Traffic Dashboard, Campaign Planner, Inventory; "Use Inventory Working Hours" flag in Campaign Manager; footfall calculations for clusters/networks/multiple frames; inventory data validation on import; custom road/segment links for train stations, parks, etc. [^2]

---

## v2025.05.13

**AI Assistant (testing mode):** Answers questions about metrics/methodologies; helps set Traffic Dashboard filters via natural language. **Inventory Manager:** Network filter on Inventory Manager List. **Combined Campaigns — Grouped Campaigns:** New campaign type with UI for adding/removing base campaigns. **VA for indoor segments:** Percentage facility based on visibility zone; VA based on indoor movement routes. **Outdoor Cluster for indoor pedestrian ways.** **Campaign Planner Active Hours widget.** **Improvements:** Dynamic filter dependencies (country → city chaining) in Campaign Planner and Traffic Dashboard; historical data limitation for campaign analysis periods; frame selection via XLSX file upload. [^1]

---

[^1]: raw/docs.allunite.com/Release Notes/v2025.05.13.md, 2026-04-21
[^2]: raw/docs.allunite.com/Release Notes/v2025.06.10.md, 2026-04-21
[^3]: raw/docs.allunite.com/Release Notes/v2025.07.08.md, 2026-04-21
[^4]: raw/docs.allunite.com/Release Notes/v2025.08.12.md, 2026-04-21
[^5]: raw/docs.allunite.com/Release Notes/v2025.09.09.md, 2026-04-21
[^6]: raw/docs.allunite.com/Release Notes/v2025.10.14.md, 2026-04-21
[^7]: raw/docs.allunite.com/Release Notes/v2025.11.11.md, 2026-04-21
[^8]: raw/docs.allunite.com/Release Notes/v2025.12.09.md, 2026-04-21
[^9]: raw/docs.allunite.com/Release Notes/v2026.01.13.md, 2026-04-21
[^10]: raw/docs.allunite.com/Release Notes/v2026.02.10.md, 2026-04-21
[^11]: raw/docs.allunite.com/Release Notes/v2026.03.02.md, 2026-04-21
[^12]: raw/docs.allunite.com/Release Notes/v2026.04.14.md, 2026-04-21

---

## Contradictions Flagged (ClickUp vs Docs)

- **Release 9 date mismatch:** Documentation source names this release `v2026.03.02`; ClickUp list is named `Release 9 - v2026-03-10` (list `901522017207`). Use doc date `2026-03-02` as canonical until confirmed. [clickup:list/901522017207]
- **Release 2 (v2025.06.10) has 0 ClickUp tasks** in list `901512928320` — this release may predate ClickUp tracking or tasks were closed/deleted.
