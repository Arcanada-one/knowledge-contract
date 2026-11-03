---
artifact_id: MM_A0222
revision_id: MM_A0222-entry-en-r1
title_en: "Compiled Artifact Contract"
title_ru: "Контракт скомпилированного артефакта"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/COMPILED_ARTIFACT_CONTRACT.md
---

# Compiled Artifact Contract

| Field | Value |
| --- | --- |
| Artifact id | MM_A0222 (permanent) |
| Entry page revision | MM_A0222-entry-en-r1 |
| Full text | [Russian original](ru/COMPILED_ARTIFACT_CONTRACT.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification defines `CompiledArtifact`, a stored derived result of a declared extraction, selection, transformation or assembly of knowledge. It links the result to its representation, build recipe, dependencies, requirements and evidence, so that people and agents can reuse it under stated conditions. It defines a bounded profile, `i16-compiled-artifact/0.1`, with a published JSON Schema and a finite checking program. It adds no new type to the shared registry. The text calls itself a research specification and says the schema and program are not an industrial service or a universal solver of meaning.

## Claims and their basis

- Four contracts (`CompiledArtifact`, `BuildRecipe`, `DependencyManifest`, `TemplateContract`) are existing registry types, and the bounded profile adds no 35th type. A compiled artifact is an immutable revision and does not establish current admission for every recipient. Basis type: not-a-claim (normative definition).
- There are six result kinds (`answer`, `template`, `context_package`, `contract_bundle`, `retrieval_result`, `dependency_closure`), each with a minimum and a forbidden inference; for example, a zero approximate-search result does not prove absence. Basis type: not-a-claim.
- Coverage is always relative to a pinned requirement set; supported slots and gaps form a disjoint partition of required slots, and `no_match` needs a declared exhaustive scope. Basis type: not-a-claim.
- Validation has five levels, from structure to current admission, and success at one level does not establish the next. Basis type: not-a-claim.
- The text names 16 conditional properties with counterexamples in a separate formal document that this page does not reproduce. Basis type: not-a-claim for this page.
- The migration function returns `migration_required` with a loss report and creates no target artifact. Basis type: not-a-claim.

## Limits

- Words such as required and forbidden set rules of this project profile; they do not declare that the external guarantees needed in production are achieved.
- Audio, video, arbitrary graphic formats and arbitrary substitution programs are not declared implemented in 0.1; a PNG example does not show recognition of graphics.
- No production resolver, full migration of old records, or extraction engine exists, and full real books are absent.
- Listing a negative case is not evidence that a test was run; actual runs are reported elsewhere.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The front matter gives version 1.0, status `concept_draft`, evidence status `proposed_contract_with_bounded_executable_profile`.
- Time-to-live policy, final cache keys and the invalidation protocol are handed to later work.

## Relation to the full text

This page summarises the specification's own statements; every rule, number and limit above comes from the Russian text, not from outside material. No separate editorial review wording exists for specifications yet, so no reviewed status wording is applied here.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
