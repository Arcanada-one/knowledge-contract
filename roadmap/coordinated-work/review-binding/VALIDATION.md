---
name: "coordinated-work-review-binding-validation"
title: "Binding Controls: Bounded Local Validation"
short_title: "Binding Controls"
subtitle: "Bounded Local Validation"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "author-side-validation"
sources:
  - "Knowledge Contract project corpus and publication edition"
---

# Binding Controls: Bounded Local Validation

## Scope and source

These are new author-side engineering observations from 18 November 2026. The
candidate is based on Knowledge Contract PR #125 at
`9cbcd22fc215e8089363912dc531e42ef6845e29`. Independently accepted science,
reviewer authenticity, publication, native admission and operational benefit are
not established by these checks. The reviewing sub-agents share the authoring
controller; this is not an independent acceptance record.

The method implements preparation and binding checks described in
[Review Bindings](README.md). The source graph retains Git blob
`0471a791e329f2f0f38ad8645a6c99f7246558a1` and SHA256
`8c7b7e6fb1f95df9f9c1c85ce083fa7ba3250ed6637ae7ce1a41d6cc1c49e3a6`.
The implementation checked here, `tools/prepare_cw_review.py`, has SHA256
`d59bf51de9c60f833a23495153ebe61affd201297c989da29de5adf1a40faaba`.
Its new regression suite has SHA256
`097172f84daff6b5d16f59823d81d7c88c5b1032d39a31e485f60031d577f6fd`.

## Executed controls

Local runtime: Python 3.12.14, the existing exchange dependency pinned to
`jsonschema==4.23.0`, and Pandoc 3.1.3 for publication checks.

| Executed check | Observed result | Claim boundary |
| --- | --- | --- |
| `tools.test_prepare_cw_review` | 39 tests pass in normal Python; 39 pass with `-O` | Positive packet preparation and adverse identity/obligation controls |
| `tools.test_reproduce_cw_scope_gap` | 8 tests pass in normal Python; 8 pass with `-O` | Exact old/corrected validator replay and failure controls |
| Existing CW programme, registration, flow-probe input and localization suites | 112 tests pass in normal Python; 112 pass with `-O` | Retained proposal, registration and source boundaries |
| Existing publication, sources, separation, DCO and CI-workflow suites | 93 tests pass | Repository gates, not scientific review |
| Publication, source and requirement-register checks | Pass; 387 registered requirements | No new competing normative schema or publication-catalogue entry |
| CW programme rendering check | Pass | Existing complete EN/RU/zh-Hans programme pages remain in sync |

An initial invocation used the system Pandoc 3.1.11.1 and was refused by the
version gate; 15 publication tests consequently failed for that same prerequisite.
The required Pandoc 3.1.3 was then selected and the full 93-test gate passed.
The gate and its required version were not weakened.

The 39-test suite includes complete synthetic P01, P02 and P13 packets, all three
document languages, and a programme announcement that does not depend on future
scientific outputs. All evidence, people and supplied review contexts in these
positive fixtures are explicitly synthetic. A mechanical pass preserves
`claim_support`, `qualified_review`, `reviewer_authenticity`, result and eligibility
as `unknown`, with `REVIEW_REQUIRED` and `effects_authorized: false`.

Adverse controls change full document tails, scope or class together with their
pin maps, source reference, domain, criterion bytes, evidence bytes and locators,
origin and review policy. They also cover missing outputs, weakened criteria,
duplicate observations, conflicting identities, wrong review scope/property,
missing review materials and hand-edited subject objects. Negative, unknown and
inapplicability observations remain retained in either input order; their
presence is not overwritten by a positive observation.

## Findings corrected during author-side review

1. A supplied observation could carry a different free-text scope. The adapter
   now compares the exact `observation_scope(subject, property)` representation,
   and the protocol context also binds that scope and property.
2. Announcement accuracy and review-protocol records lacked required material
   references. They now reference the graph and complete announcement texts, or
   the bound review policy, respectively. Rights records reference the declared
   documents without treating those references as a rights grant.
3. The pure API could receive changed graph bytes under an unchanged claimed Git
   revision. It now requires an independently selected `expected_source_ref` and
   compares the full reference. The API explicitly reports caller-selected,
   unauthenticated provenance; the CLI separately reads and checks the local Git
   commit. A P01 gate reduction from ten outputs to one is refused against the
   original expected reference. This is not authentication of repository ownership.

The first two fixes have both a complete positive announcement control and
specific adverse controls. The third has the original ten-output positive
control and the gate-reduction adverse control. These are implementation checks,
not proof of complete security or semantic conformance.

## Retained new reports

[historical-scope-replay.json](historical-scope-replay.json) is a new deterministic
synthetic replay, not recovered c167 bytes. Its exact SHA256 is
`1dbbbe39c18af72f91d8e3b4ea2e47c7dd51f4f2d0548ff564d6b858d1b5b4b5`.
The original graph passes both pinned validators. Both synthetic same-class
overstatements pass full validation and are copied into proposed release
instances by `9ba73c99`; `9cbcd22f` refuses them at its exact scope guard. The report
records every input path, blob, SHA256 and observed stage result. It does not
claim that the real paper texts contained either synthetic statement.

[pending-paper-reviews.json](pending-paper-reviews.json) prepares the 16 actual
proposed paper contracts at the pinned source. It contains 138 required output
references, with no supplied result bytes for those references. Manuscripts,
applicability records, review policies and observations are also unprovided in
these packets. All 16 report `REVIEW_REQUIRED`; this is an inventory of these
inputs, not a claim that no materials exist elsewhere or a search of Muneral.

## Remaining acceptance and use boundaries

The repository-only method does not resolve authenticated reviewer records,
establish competence, assess the semantics of prose or evidence locators,
evaluate contrary evidence, verify translation fidelity, determine rights,
subscribe to withdrawals or recheck current authority at release time. Those
obligations remain explicit in the method and in the existing programme Work
Items. No native IDs or completion states were written into the programme.

Hosted CI and independent reviewer dispositions are recorded separately on the
candidate pull request. They are not inferred from these local results.
