---
artifact_id: MM_A0224
revision_id: MM_A0224-entry-en-r1
title_en: "Family of Contracts for Operations on Meanings and Knowledge"
title_ru: "Семейство контрактов операций над смыслами и знаниями"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/CONTRACT_FAMILY.md
---

# Family of Contracts for Operations on Meanings and Knowledge

| Field | Value |
| --- | --- |
| Artifact id | MM_A0224 (permanent) |
| Entry page revision | MM_A0224-entry-en-r1 |
| Full text | [Russian original](ru/CONTRACT_FAMILY.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification defines a family of contracts that tie knowledge to the actions allowed on it: preserving a source, extracting meaning, aligning an illustration with text, retrieving, preparing bounded context, handing it over, explaining, doing work, revising and reusing a result. A contract states under which inputs and conditions an operation is admissible, what it keeps and changes, which outcomes are allowed and how they are confirmed. The text defines 17 operation profiles and five outcomes. It declares itself a concept draft (edition 0.9) aligned with the draft Knowledge Contract v3.

## Claims and their basis

- A contract binds an operation to a version, a scope and a requirements snapshot; structural correctness of a record does not mean its content is true. Basis type: not-a-claim (normative definition).
- There are 17 operation profiles, from Preserve to Reuse. The text says they are a set of possible operations, not seventeen mandatory stages of every request. Basis type: not-a-claim.
- The five outcomes are success, partial, refused, failed and unresolved. Partial does not pass a success edge automatically. Basis type: not-a-claim.
- Human and agent recipients receive the same result, conditions, grounds, gaps and next step, in different forms. Basis type: not-a-claim.
- Practical usefulness of the family is a hypothesis. It must be compared with a good structured summary, ordinary search, graph dependencies and a strong typed workflow at a comparable budget. Negative results are possible. Basis type: hypothesis.

## Limits

- The historical bounded grammar was checked on authors' examples only; an industrial executor and a universal predicate solver are not implemented.
- 48 planned scenarios, 14 counterexample analyses and six end-to-end routes do not raise the status of 320 earlier items or 18 earlier illustrations.
- The fixture and validator check consistency of authored records; they do not observe a perceptual model at work.
- The practical path covers text and images; audio and video are in the theoretical model only.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The text gives edition 0.9 and status `concept_draft`; no front matter is present in the source.
- Compatibility with Knowledge Contract v2 is a migration boundary, not a settled mapping.

## Relation to the full text

This page summarises the specification's own statements; every rule, number and limit above comes from the Russian text, not from outside material. No separate editorial review wording exists for specifications yet, so no reviewed status wording is applied here.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
