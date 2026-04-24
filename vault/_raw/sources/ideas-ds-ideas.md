---
title: "Source: Ideas / DS Ideas"
type: source
tags: [ideas, data-science, traffic, frequency, impressions]
sources:
  - raw/docs.allunite.com/Ideas/DS ideas.md
updated: 2026-04-21
status: draft
---

# Source: Ideas / DS Ideas

**Raw path:** `raw/docs.allunite.com/Ideas/DS ideas.md`

## Summary

Data Science backlog ideas:

1. Jupyter Notebook for data validation (ClickUp: 86c6geqm4) — Total Traffic validation with filters (country/company/category/facility whitelist+blacklist, date range, dataset); MC vs. predicted comparison; validation on TT>0, TT==0, missing, session type combinations.
2. Platform UI to enable Impressions per company and set parameters (ClickUp: 86c6qd0ay).
3. Apply automatic multi-source mirroring for Finland (ClickUp: 86c6qdu9h) — use Tetiana's model + Ramboll 3rd-party coefficients; preserve existing coefficients; easily extensible to other markets.
4. Dwell-time for virtual locations without virtual sessions (using mirroring?).
5. Fix clean-up in Traffic job when facility changes category (ClickUp: 86c95070w).

**Visit Frequency ideas (ClickUp: 86c91phut):**
1. Frequency modelling by device_ids: assign synthetic device_ids for unique traffic union counting.
2. Log-log surface model (2-parameter) for frequency — more natural economic interpretation; can be vibe-coded in Cursor-IDE; build dictionary {project: parameters} for lookup.
3. Account for changes in number of facilities per region (parameters not bound to facility count).
4. Account for actual distances between facilities (not just within/across cluster membership).

Sources: `raw/docs.allunite.com/Ideas/DS ideas.md` 2026-04-21
