---
case_id: candidate-export-gate
title: "A fail-closed exporter between a public repository and an indexer"
status: written
work_items: [KCP-0018]
license: CC-BY-4.0
language: en
---

# A fail-closed exporter between a public repository and an indexer

## Goal

Let an indexer read documents from the public repository only when each document has an explicit allowlist row, a merged source commit, a content digest, a rights holder, a licence and a reviewed publication decision, and refuse everything else without writing to any index.

## Setup

The exporter reads the allowlist table of the repository, checks each row against the decision files and the merged history, and writes a candidate bundle with a manifest. It does not write to the search index, does not advance a serving generation and does not claim admission by the Knowledge Contract runtime. A change to this tool was described by a provisional change-admission receipt listing 5 [R1] changed files and 3 [R2] impact entries.

## What was checked and how

The receipt records one verifier per impacted entity. For the allowlist parser and the rights decision gate the verifier is a local unit-test run; the receipt states that all 14 [R3] local unit cases passed on the current source at that time. For the other entities the receipt names a verifier that was still pending (a run on the resulting main branch) or could not yet run (no approved rows existed), and says so.

## Receipts

| Tag | File | Kind | Locator | Value |
| --- | --- | --- | --- | --- |
| R1 | receipts/graph/change-admission-kcp-0018-export.json | count | /change_set | 5 |
| R2 | receipts/graph/change-admission-kcp-0018-export.json | count | /impact_set | 3 |
| R3 | receipts/graph/change-admission-kcp-0018-export.json | text_contains | /impact_set/0/evidence | 14/14 local unittest PASS |
| R4 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/0/verdict | verified |
| R5 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/1/verdict | not_measured |
| R6 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/2/verdict | not_measured |
| R7 | receipts/graph/change-admission-kcp-0018-export.json | value | /canonical_admission | not_measured |
| R8 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/1/expires_at_utc | 2026-11-02T00:00:00Z |
| R9 | receipts/graph/change-admission-kcp-0018-export.json | value | /graph | manual fallback: no installed graph verifier in this public repository |

## Result

One entity was verified [R4]. The other entities were recorded as not measured [R5] [R6], each with an owner and an expiry. Canonical admission is likewise not measured [R7]. The result is a gate that is closed by default and a receipt that says which parts of it were and were not verified.

## Limits

- The receipt was produced by a manual fallback, not by an installed graph verifier [R9]; it is not a native change-admission record.
- The expiry of the not-measured entries [R8] is in the past at the time of writing, and this repository holds no later receipt that measured them. They remain not measured.
- The statement in the receipt that the public allowlist was empty described the repository at that time; the allowlist has since received rows (see the case on the publication pipeline).
- The 14 [R3] unit cases test the parser and the decision gate on constructed inputs. They do not show that the exporter is free of other defects.

## What failed on the way

- The receipt was provisional. A later commit rebound it to the public continuous-integration source, and another commit changed the public workflow's runner configuration to keep it impersonal.
- After the first release the exporter's scope list had to be extended to admit the new entry pages. The scope is an explicit list by design, so each widening needs a decision.
