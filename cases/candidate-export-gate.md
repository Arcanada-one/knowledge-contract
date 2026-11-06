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

The current exporter reads the allowlist table of the repository, checks each row against the decision files and the merged history, and writes a candidate bundle with a manifest. It does not write to the search index, does not advance a serving generation and does not claim admission by the Knowledge Contract runtime. A change to this tool was described by a provisional change-admission receipt, captured against an earlier version of the exporter (base commit [R10], source commit [R11]), listing 5 [R1] changed files and 3 [R2] impact entries. After the review-based route was replaced by decision files, a later provisional receipt [R14] remeasured the same work item against the decision-file exporter on current main and retired the expired not-measured entries of the historical receipt.

## What was checked and how

The historical receipt records a verifier for each impacted entity. For the allowlist parser and the rights decision gate the verifier is a local unit-test run; the receipt states that all 14 [R3] local unit cases passed on the current source at that time. For the other entities the receipt names a verifier that was still pending (a run on the resulting main branch) or could not yet run (no approved rows existed), and says so.

The later receipt [R14] remeasures those entities for the decision-file exporter. Local tests on the pinned main tip report 83 [R15] unit cases passed. An exact-main candidate export on that tip, and the matching continuous-integration step on the same head, report a candidate-only bundle with 35 [R16] allowlist rows exported, decision-file readback, and no index write.

## Receipts

| Tag | File | Kind | Locator | Value | Near |
| --- | --- | --- | --- | --- | --- |
| R1 | receipts/graph/change-admission-kcp-0018-export.json | count | /change_set | 5 | file |
| R2 | receipts/graph/change-admission-kcp-0018-export.json | count | /impact_set | 3 | impact |
| R3 | receipts/graph/change-admission-kcp-0018-export.json | text_contains | /impact_set/0/evidence | 14/14 local unittest PASS | unit |
| R4 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/0/verdict | verified | |
| R5 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/1/verdict | not_measured | |
| R6 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/2/verdict | not_measured | |
| R7 | receipts/graph/change-admission-kcp-0018-export.json | value | /canonical_admission | not_measured | |
| R8 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/1/expires_at_utc | 2026-11-02T00:00:00Z | |
| R10 | receipts/graph/change-admission-kcp-0018-export.json | value | /base_sha | 21f4331b7944feee5562d1193e6843cf442e04b9 | |
| R11 | receipts/graph/change-admission-kcp-0018-export.json | value | /source_head_sha | 37e3415541280199f42cbc316324b9f13586cb8e | |
| R12 | receipts/graph/change-admission-kcp-0018-export.json | value | /admission | paused_safe_until_ci_and_independent_review | |
| R13 | receipts/graph/change-admission-kcp-0018-export.json | value | /impact_set/2/expires_at_utc | 2026-11-02T00:00:00Z | |
| R9 | receipts/graph/change-admission-kcp-0018-export.json | value | /graph | manual fallback: no installed graph verifier in this public repository | |
| R14 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | value | /supersedes/path | receipts/graph/change-admission-kcp-0018-export.json | |
| R15 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | text_contains | /impact_set/0/evidence | 83/83 local unittest PASS | unit |
| R16 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | text_contains | /impact_set/1/evidence | row_count=35 | row |
| R17 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | value | /impact_set/1/verdict | verified | |
| R18 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | value | /impact_set/2/verdict | verified | |
| R19 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | value | /canonical_admission | not_measured | |
| R20 | receipts/graph/change-admission-kcp-0018-export-decision-file.json | value | /measured_main_sha | ea0c30575d56e793fb2875df47126ab3f6dc30ad | |

## Result

The historical parser and decision-gate entity was verified [R4]. The other historical entities were recorded as not measured [R5] [R6], each with an owner and an expiry. Canonical admission is likewise not measured [R7]. The result of that earlier capture is a gate that is closed by default and a receipt that says which parts of it were and were not verified.

The later receipt [R14] retires those expired not-measured entries and records verified [R17] [R18] for the decision-file exporter's exact-main candidate binding and for the nonempty corpus decision-file rights and secret-scan path into a candidate bundle that does not write an index. Canonical admission remains not measured [R19]. The measurement is pinned to main tip [R20].

## Limits

- The historical receipt describes an earlier exporter in which a publication decision was an approving review on the hosting platform; its unit cases covered an exact review body and an independent identity. That route was replaced by decision files with receipts, so the historical receipt does not verify the current exporter. The historical receipt's own admission reads [R12].
- The historical receipt was produced by a manual fallback, not by an installed graph verifier [R9]; it is not a native change-admission record. The later receipt [R14] is likewise a provisional manual fallback.
- The expiries [R8] [R13] of the historical not-measured entries are in the past. The later receipt [R14] remeasures those entities for the decision-file exporter and retires the expired entries; the historical JSON file is left unchanged.
- The statement in the historical receipt that the public allowlist was empty described the repository at that time; the allowlist has since received rows, and the later receipt records 35 [R16] exported rows on the pinned tip.
- The 14 [R3] unit cases tested the parser and the decision gate of that earlier version on boundary cases. They do not show that the current exporter, or that version, is free of other defects. The later local run reports 83 [R15] unit cases on the decision-file exporter; that count still does not prove absence of every other defect.
- Index ingestion and KC2 runtime admission remain outside the exporter's effect boundary; the later receipt measures `scrutator_projection=not_applied` and leaves canonical admission not measured [R19].

## What failed on the way

- The historical receipt was provisional. A later commit rebound it to the public continuous-integration source, and another commit changed the public workflow's runner configuration to keep it impersonal.
- After the first release the exporter's scope list had to be extended to admit the new entry pages. The scope is an explicit list by design, so each widening needs a decision.
- The historical not-measured entries were left past their expiry without a replacement receipt until the decision-file remeasurement recorded here.
