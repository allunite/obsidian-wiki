---
title: Operations
type: overview
tags: [operations, team, workflow, clockify]
sources:
  - raw/docs.allunite.com/Operations/Data%2FOps Team Operating Model.md
  - raw/docs.allunite.com/Operations/Clockify manual.md
  - raw/docs.allunite.com/Operations/Terminology.md
related:
  - clients/joe-and-the-juice.md
  - systems/routers.md
updated: 2026-04-21
status: stable
---

# Operations

The Data/Ops team operates under a structured model emphasizing clear task ownership, scope control, budget discipline, and efficient project activation. [^1]

## Operating Model Summary

1. **Task Ownership:** Every task must have defined scope, man-hours, owner, deadline, and priority. PM handles cross-functional coordination; Data/Ops executes within approved scope.
2. **Scope Control:** Out-of-scope tasks require PM-created ClickUp task tagged "out of scope" with estimation before work starts.
3. **Budget Escalation:** When estimated hours are reached, comment in ClickUp tagging PM, reassign to PM, set status "Waiting for approval." No additional work without explicit approval.
4. **Blockers:** Blocked tasks are reassigned to PM with clear description. 2-hour escalation rule to team leads/COO/CDO.
5. **Clockify Structure:** All hours logged under: Project – Delivery, Project – OOS, Project – Client Communication, Project – Maintenance, Project – Pre-sale.
6. **Client Communication:** Data team max 5h per client per project. Scope questions → PM.
7. **R&D/Optimization/Automation:** Requires dedicated ClickUp task and prioritization review before starting. [^1]

## Communication Responsibility Model

- **PM:** Owns all email and meeting communication; owns scope discussions; creates ClickUp tasks for Ops/Data involvement.
- **Ops:** Handles technical installation communication only upon PM request.
- **Data:** Technical and methodology questions only upon PM request, time-boxed to 5h/project/client. [^1]

## Clockify Usage

Time tracking guidelines: ±5–10 min accuracy acceptable; connect Google Calendar for ease; always specify project; description optional. [^2]

---

## Active Ops Work (ClickUp)

Source: OT Work list `901511360787`, Operational Team space `90154748965`. 38 open tasks at sync 2026-04-21. [clickup:list/901511360787]

### Sensor Installation & Maintenance

Largest work cluster (~20 tasks). Recurring task types per site: "Installation Guideline + Firmware Update", "Sensor installation (rule – 3 sensors per day)", "Sensor re-positioning (If needed)". Active deployment sites include Brazilian airports and venue rollouts.

### Inventory Finalisation

Tasks for finalising inventory records at newly onboarded sites — multiple Brazilian clients (JCDecaux SP/BSB/GRU, Helloo Malls, Helloo Neooh Airports, MUDE, Bike Station). Includes "Update inventory" and "Finalisation of Inventory" task types.

### Client Sensor Checks

"Ask the client about offline sensors", "Check with client some sensors" — reactive maintenance coordination.

### Manual Countings

Airport sites requiring manual pedestrian counting to supplement sensor data (validation / calibration support).

### New Zealand — Phantom Billstickers (`901512571750`)

15 tasks including:
- Site Coverage Analysis: 10 vs. 17 Sensors (high priority)
- 3rd-party demographics to be applied (in review)
- Validate demographics after application (low)
- Relocation of Sensor suggestion (in review)
- Maintenance OT / IT / CSM tasks
- Final Report and Client Feedback (not started)

[clickup:list/901512571750]

### Mexico — OLA Media (`901517509005`)

2 open tasks: captive portal data analysis, export/graph discrepancy investigation. [clickup:list/901517509005]

### Costa Rica — Publiex (`901512121885`)

2 open tasks: finalising sensor count, analysis and location recommendation for sensors. [clickup:list/901512121885]

[^1]: raw/docs.allunite.com/Operations/Data%2FOps Team Operating Model.md, 2026-04-21
[^2]: raw/docs.allunite.com/Operations/Clockify manual.md, 2026-04-21
