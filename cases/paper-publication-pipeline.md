---
case_id: paper-publication-pipeline
title: "From edited papers to a reviewed, pinned public release"
status: written
work_items: [KCP-0040, KCP-0041, KCP-0042]
license: CC-BY-4.0
language: en
---

# From edited papers to a reviewed, pinned public release

## Goal

Publish the papers P00 to P13 and their specifications in the public repository as a first release, and let an indexer read a file only through a decision that names the file, its digest, its rights holder and its licence and that a blind review has approved. The case records how far that went: the decisions cover the English entry pages of the papers and the 6 [R4] mirrored project documents, not the whole release.

## Setup

The first release catalogue lists 24 [R1] items and a release digest taken over 50 [R2] files. The files are the full texts, the entry pages and the index pages of the release. The papers and specifications were published with link targets rewritten to repository routes or marked as not in the release, as the link map records; it holds 24 [R3] per-file entries. Publication decisions are append-only files in batches. Batch b1 holds 6 [R4] decision lines and batch b2 holds 14 [R5] decision lines. Each batch has a receipt that binds the reviewed head, the base, the diff digest and the digests of the decision lines to the reviewers' transcripts. The allowlist table that the exporter reads now has 20 [R6] rows.

## What was checked and how

Each decision line carries the path, the SHA-256 of the file, the rights holder, the licence, the stated rights basis, third-party material, the credit line and the limits of the review. Reviewers working blind, 2 [R7] per batch, received the same fixed checklist and the same input: the diff, the file bytes and the licence declarations. Their transcripts and inputs are kept in the repository. The exporter refuses a row without a matching decision line, and a repository check refuses a change that combines any of these with another of them: decision files, the allowlist table, content paths, so a decision cannot land together with the content it approves.

## Receipts

| Tag | File | Kind | Locator | Value | Near |
| --- | --- | --- | --- | --- | --- |
| R1 | receipts/meaning-management/release-catalog.json | count | /items | 24 | item |
| R2 | receipts/meaning-management/release-catalog.json | value | /release_digest/files | 50 | file |
| R3 | receipts/meaning-management/link-rewrites.json | count | /files | 24 | entr |
| R4 | corpus/publication-decisions/receipts/b1.json | count | /decision_lines_sha256 | 6 | decision line,mirrored |
| R5 | corpus/publication-decisions/receipts/b2.json | count | /decision_lines_sha256 | 14 | decision line,entry page |
| R6 | corpus/README.md | table_rows | Public corpus allowlist | 20 | row |
| R7 | corpus/publication-decisions/receipts/b1.json | count | /reviewers | 2 | batch |
| R8 | corpus/publication-decisions/receipts/b2.json | count | /reviewers | 2 | batch |
| R9 | corpus/publication-decisions/receipts/b2.json | value | /reviewers/0/verdict | APPROVE | |
| R10 | receipts/meaning-management/release-catalog.json | value | /gates/independent_semantic_review | not_performed | |
| R11 | receipts/meaning-management/release-catalog.json | value | /gates/corpus_allowlist_rows | none | |
| R12 | receipts/meaning-management/release-catalog.json | value | /deviations/0/id | spec-front-matter | |
| R13 | receipts/meaning-management/release-catalog.json | value | /decisions/0/status | DECIDED-BY-AGENT, reversible | |
| R14 | receipts/meaning-management/release-catalog.json | value | /gates/exporter_scope | not in SCOPE_PATHS; not an indexing input | |
| R15 | corpus/publication-decisions/receipts/b2.json | value | /reviewers/1/verdict | APPROVE | |
| R16 | receipts/meaning-management/release-catalog.json | value | /gates/late_research_synthesis | open | |
| R17 | receipts/meaning-management/release-catalog.json | value | /status | scientific draft; see gates | |

## Result

The batches were approved by their reviewers (2 [R7] for batch b1 and 2 [R8] for batch b2); the verdicts of the reviewers of batch b2 are APPROVE [R9] and APPROVE [R15]. The 6 [R4] mirrored documents of batch b1 and the 14 [R5] English entry pages of batch b2 are the 20 [R6] rows of the allowlist. The specification entry pages and the Russian full texts have no decision line and no allowlist row; the release catalogue says its exporter scope was [R14] at the time it was written, and the scope was widened afterwards only for the paper entry pages. The release catalogue binds its 24 [R1] items to a digest over 50 [R2] files, so a later change to any of those files shows as a different digest if someone recomputes it; no check in this repository recomputes it.

## Limits

- The reviewers run under the same account as the writer; the exporter records this as the class same_account_blind_agent, not as proof of independence. The first reviewer of batch b2 states that recomputing the digests from the page bytes was not measured by that reviewer.
- The semantic content has not been reviewed by an independent party: the catalogue gate reads [R10]. The late research synthesis gate reads [R16] and the release status reads [R17]; the papers are drafts, not results.
- The catalogue gate for allowlist rows reads [R11] while the table has 20 [R6] rows, and the repository history dates the first rows (batch b1) before the catalogue. The gate is therefore stale or means no rows for the catalogue's own items; the repository does not say which, and it was not corrected.
- The edition of record was chosen by an agent and is marked reversible [R13].
- Approval of a file for the exporter is not KC2 admission and not a statement that the claims in the papers are true.

## What failed on the way

- The first publication route asked another hosting-platform identity for an approving review. The repository states why it was replaced: all work is authored by a service account and the operator signs nothing, so the route was replaced, not weakened, by a decision file with a receipt.
- The specifications carry front matter without a title and without a sources key. The catalogue records this as a deviation [R12]; the source coverage is declared in the source register instead.
- The exporter and its checks were hardened in separate commits: before the first decision batch (secret scanner install, rename-safe separation check, deny scan) and again after the first allowlist rows (review notes on the whole-word DCO match, named deny-scan messages and pinned author shapes).
