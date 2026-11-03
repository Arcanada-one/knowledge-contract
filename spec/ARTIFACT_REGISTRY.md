---
artifact_id: MM_A0220
revision_id: MM_A0220-entry-en-r1
title_en: "Registry of Shared Artifacts: Identity, Fields and Obligations"
title_ru: "Реестр общих артефактов: идентичность, поля и обязанности"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/ARTIFACT_REGISTRY.md
---

# Registry of Shared Artifacts: Identity, Fields and Obligations

| Field | Value |
| --- | --- |
| Artifact id | MM_A0220 (permanent) |
| Entry page revision | MM_A0220-entry-en-r1 |
| Full text | [Russian original](ru/ARTIFACT_REGISTRY.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification defines a registry of shared artifact types for the Meaning Management model. Registry version 0.1 lists 34 conceptual types: 30 introduced earlier and four added explicitly. A common envelope, `mm-envelope/0.1`, makes an addressable, immutable revision, and profiles set the requirements for each kind of record. The text separates five levels of representation, from artifact type down to physical placement, and defines a four-state value for known, unknown, not-applicable and withheld fields. It declares itself a concept draft that develops toward the draft Knowledge Contract v3 (`3.0.0-draft.1`), and it does not announce a ready API or a completed v3 schema.

## Claims and their basis

- The registry separates five levels: artifact type, representation profile, logical object, immutable revision, and representation or placement. Each level states what it does not imply. Basis type: not-a-claim (normative definition).
- Registry version 0.1 has 34 types, and the common envelope is mandatory in every row. Payload fields are a minimum signature that may be refined. Basis type: not-a-claim.
- `KnowledgeValue` has four forms: `known`, `unknown`, `not_applicable`, `withheld`. A value is required only for `known`; an empty list means known absence in a stated scope; null is not a universal unknown. Basis type: not-a-claim.
- Immutability applies to a stored revision. A mutable `CacheEntry` has generations and snapshots, and moving the same copy changes only the placement registry. Basis type: not-a-claim.
- A local script checks finite records and deliberately damaged variants across four main demonstration groups plus identity checks. The text gives no run counts of its own. Basis type: finite-test (denominator not stated in this text).
- Whether the typed approach beats ordinary versioned metadata, provenance, search and application validators is open. The text says advantage, completeness and universality still need evidence and trials. Basis type: hypothesis.

## Limits

- Structural correctness of a record does not establish that its content is true, and `known` means a value is recorded, not independently verified.
- The checking script is not a full JSON Schema or SHACL processor, resolver or extraction system.
- System-level cases remain planned or illustrated; none is reported as observed in operation.
- Reading an envelope does not establish conformance with Knowledge Contract v2 or with the future v3.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The specification's front matter gives status `concept_draft`, document version 0.2, registry version 0.1.
- Which of the 34 type signatures will survive into v3 is open: the text says future types and carrier may change with justification and migration.

## Relation to the full text

This page summarises the specification's own statements; every rule, number and limit above comes from the Russian text, not from outside material. No separate editorial review wording exists for specifications yet, so no reviewed status wording is applied here.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
