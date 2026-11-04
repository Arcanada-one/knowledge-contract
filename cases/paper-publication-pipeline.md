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

Publish the papers P00 to P13 and their specifications in the public repository as a first release, so that the text reaches an indexer only through a decision that names the file, its digest, its rights holder and its licence, and that a blind review has approved.

## Setup

The first release catalogue lists 24 [R1] items and a release digest taken over 50 [R2] files. The papers and specifications were published with link targets rewritten to repository routes or marked as not in the release, as the link map records; it holds 24 [R3] per-file entries. Publication decisions are append-only files in batches. Batch b1 holds 6 [R4] decision lines and batch b2 holds 14 [R5]. Each batch has a receipt that binds the reviewed head, the base, the diff digest and the digests of the decision lines to the reviewers' transcripts. The allowlist table that the exporter reads now has 20 [R6] rows.

## What was checked and how

Each decision line carries the path, the SHA-256 of the file, the rights holder, the licence, the stated rights basis, third-party material, the credit line and the limits of the review. A pair of blind reviewers received the same fixed checklist and the same input: the diff, the file bytes and the licence declarations. Their transcripts and inputs are kept in the repository. The exporter refuses a row without a matching decision line, and a repository check refuses a change that mixes decision files, the allowlist table and content paths, so a decision cannot land together with the content it approves.

## Receipts

| Tag | File | Kind | Locator | Value |
| --- | --- | --- | --- | --- |
| R1 | receipts/meaning-management/release-catalog.json | count | /items | 24 |
| R2 | receipts/meaning-management/release-catalog.json | value | /release_digest/files | 50 |
| R3 | receipts/meaning-management/link-rewrites.json | count | /files | 24 |
| R4 | corpus/publication-decisions/receipts/b1.json | count | /decision_lines_sha256 | 6 |
| R5 | corpus/publication-decisions/receipts/b2.json | count | /decision_lines_sha256 | 14 |
| R6 | corpus/README.md | table_rows | Public corpus allowlist | 20 |
| R7 | corpus/publication-decisions/receipts/b1.json | count | /reviewers | 2 |
| R8 | corpus/publication-decisions/receipts/b2.json | count | /reviewers | 2 |
| R9 | corpus/publication-decisions/receipts/b2.json | value | /reviewers/0/verdict | APPROVE |
| R10 | receipts/meaning-management/release-catalog.json | value | /gates/independent_semantic_review | not_performed |
| R11 | receipts/meaning-management/release-catalog.json | value | /gates/corpus_allowlist_rows | none |
| R12 | receipts/meaning-management/release-catalog.json | value | /deviations/0/id | spec-front-matter |
| R13 | receipts/meaning-management/release-catalog.json | value | /decisions/0/status | DECIDED-BY-AGENT, reversible |

## Result

Both batches were approved by their reviewers (2 [R7] for batch b1 and 2 [R8] for batch b2); the verdict of the first reviewer of batch b2 is APPROVE [R9]. The 6 [R4] documents of batch b1 and the 14 [R5] entry pages of batch b2 are the 20 [R6] rows of the allowlist. The release catalogue binds the 24 [R1] papers and specifications to one digest over 50 [R2] files, so a later change to any of those files is visible as a different digest.

## Limits

- The reviewers run under the same account and model family as the writer; the exporter records this as a class, not as proof of independence. The reviewer of batch b2 states that recomputing the digests from the page bytes was not measured by that reviewer.
- The semantic content has not been reviewed by an independent party: the catalogue gate reads [R10].
- The release catalogue was written before batch b2 and its gate for allowlist rows reads [R11] while the table now has 20 [R6] rows. The gate describes that moment, not the present; the catalogue was not updated.
- The edition of record was chosen by an agent and is marked reversible [R13].
- Approval of a file for the exporter is not KC2 admission and not a statement that the claims in the papers are true.

## What failed on the way

- The first publication route relied on review approvals on the hosting platform. The repository history records its replacement by merged decision files with receipts; the repository does not record a reason beyond that change.
- The specifications carry front matter without a title and without a sources key. The catalogue records this as a deviation [R12]; the source coverage is declared in the source register instead.
- The exporter and its checks were hardened in separate commits: before the first decision batch (secret scanner install, rename-safe separation check, deny scan) and again after the first allowlist rows (review notes on the whole-word DCO match, named deny-scan messages and pinned author shapes).
