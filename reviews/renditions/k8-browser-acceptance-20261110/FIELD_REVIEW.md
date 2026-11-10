---
title: "K8 browser-acceptance public report.json field review"
sources: none
status: "Deterministic residual-field scan of redacted report.json"
updated: 2026-11-10
---

# K8 browser-acceptance public report.json field review

Deterministic scan of the committed redacted `report.json`.
This is a bounded residual-field review, not an independent browser
replay and not a claim that every unknown field is safe.

- report bytes: `733560`
- report sha256: `78dd20f3a3e9192865bfab07f4d8f1f56c550cfa8fcfc04506c3507dedbb4242`

## Header keys kept (`response_headers_sample`)

- `content-type`
- `last-modified`

Expected only: `content-type`, `last-modified`.

## Residual marker counts

| Marker | Count |
| --- | ---: |
| IPv4 | 0 |
| Absolute host paths | 0 |
| Cookies | 0 |
| cf-ray | 0 |
| Tokens/keys | 0 |
| Emails | 0 |
| User agents | 0 |

Expected count for each marker above: `0`.

## Non-github host strings

- `contract.place`
- `static.cloudflareinsights.com`
