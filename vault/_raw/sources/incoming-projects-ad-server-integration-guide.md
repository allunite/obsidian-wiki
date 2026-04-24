---
title: "Source: Incoming Projects / Ad Server Integration Guide"
type: source
tags: [incoming-projects, captive-portal, ad-server, api, wifi]
sources:
  - raw/docs.allunite.com/Incoming Projects/Ad Server Integration Guide.md
updated: 2026-04-21
status: draft
---

# Source: Ad Server Integration Guide

**Raw path:** `raw/docs.allunite.com/Incoming Projects/Ad Server Integration Guide.md`

## Summary

Integration spec for connecting external ad servers to the AllUnite captive portal (WiFi hotspot flow). Flow: User connects WiFi → accepts terms → portal redirects to ad server with params (`router`, `client_id`, `return`) → ad server shows ad → ad server HTTP 302 redirects back to `return` URL → user gets internet access. Optional `redirect_url` appended to control post-auth destination. Requirements: must redirect back; must preserve `return` URL; should complete promptly; handle mobile browsers. Custom parameters configurable per-portal or per-router. Each new session triggers a new ad flow.

Sources: `raw/docs.allunite.com/Incoming Projects/Ad Server Integration Guide.md` 2026-04-21
