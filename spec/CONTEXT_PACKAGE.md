---
artifact_id: MM_A0223
revision_id: MM_A0223-entry-en-r1
title_en: "ContextPackage: Specification and Bounded Executable Profile"
title_ru: "ContextPackage: спецификация и ограниченный исполнимый профиль"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/CONTEXT_PACKAGE.md
---

# ContextPackage: Specification and Bounded Executable Profile

| Field | Value |
| --- | --- |
| Artifact id | MM_A0223 (permanent) |
| Entry page revision | MM_A0223-entry-en-r1 |
| Full text | [Russian original](ru/CONTEXT_PACKAGE.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification defines `ContextPackage`, a versioned package of statements and conditions prepared for one intent and one bounded use. It lets a reader check provenance, coverage, dependencies, scope of applicability and budget. The text lists 13 groups of required fields, a coverage vocabulary, a separate stop-reason vocabulary, and budget and validation rules. It states that it keeps the status of a research proposal. A bounded profile, `i14-context-package/0.1`, defines a finite serialisation, a local recipient and a validator. Successful validation grants no authority to act and does not confirm physical execution.

## Claims and their basis

- A package has 13 field groups: identity, intent, snapshot, candidates, selection, dependencies, coverage, exclusions, transformations, evidence, budgets, validation and completion. Basis type: not-a-claim (normative definition).
- Coverage statuses are `supported`, `partial`, `unsupported`, `conflicted` and `unknown`; the text calls them a project proposal. Slots of one result are tied to a common subject identity. Basis type: not-a-claim.
- `stop_reason` has five values (`completed`, `clarification_needed`, `budget_insufficient`, `retrieval_limit`, `stale_evidence`) and describes how processing ended, not whether the answer is true. Basis type: not-a-claim.
- Budget estimates and measurements are stored separately, and required conditions are not trimmed to fit. Basis type: not-a-claim.
- The bounded profile was executed: 94 of 94 checks passed, comprising 14 positive, 77 negative and three finite enumerations. Only UTF-8 bytes were measured. Basis type: finite-test (94 checks).

## Limits

- Model tokenisation, external products and remote delivery were not measured.
- A passing validation does not show that a recipient understood the package, nor a causal contribution of its content.
- A high utility estimate does not allow dropping a unit, a legend or an access right.
- A digest match confirms integrity only against a trusted expected value.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The front matter gives version 0.4, status `concept_draft`, evidence status `research_proposal_with_bounded_executable_profile`.
- Reuse of packages through compilation and caching is handed to later work and is not settled here.

## Relation to the full text

This page summarises the specification's own statements; every rule, number and limit above comes from the Russian text, not from outside material. No separate editorial review wording exists for specifications yet, so no reviewed status wording is applied here.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
