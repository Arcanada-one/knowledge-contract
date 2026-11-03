---
artifact_id: MM_A0960
revision_id: MM_A0960-entry-en-r1
title_en: "Knowledge Bases and Contract Evolution"
title_ru: "Версии оснований знания и эволюция контрактов"
language: en
status: scientific draft
scientific_status: normative_architecture_requirement_with_proposed_metadata_profile
license: CC-BY-4.0
full_text: ru/KNOWLEDGE_EVOLUTION_CONTRACT.md
---

# Knowledge Bases and Contract Evolution

| Field | Value |
| --- | --- |
| Artifact id | MM_A0960 (permanent) |
| Entry page revision | MM_A0960-entry-en-r1 |
| Full text | [Russian original](ru/KNOWLEDGE_EVOLUTION_CONTRACT.md), language: Russian |
| Status | scientific draft; the specification states its own status as `normative_architecture_requirement_with_proposed_metadata_profile`; not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification states a requirement for recording which versions of contracts, profiles and rules a knowledge or decision card was created under, and for handling later change. A card keeps the exact versions used at creation; checks against newer rules are recorded separately, and provenance and earlier revisions are never rewritten. The text defines version layers, creation and change records, an impact graph, a review process and a proposed metadata profile with a local validator. It states that the contract family does not yet have approved production schemas, so the document sets requirements and a bounded profile only.

## Claims and their basis

- Every new card keeps the exact versions of the contracts, profiles and rules used at creation; a later check under new rules is a separate record. Basis type: not-a-claim (normative requirement).
- A new rule version can make an old card incomplete for a given use without making its content false; the result of reassessment is a local value (`current_compatible`, `restricted`, `requires_review`, `blocked`, `unknown`) mapped onto existing status axes. Basis type: not-a-claim (normative definition).
- Creation versions may be `pinned`, `not_applicable` or `unknown`; `unknown` is allowed only for an explicitly marked legacy import, and substituting the current version for an unknown one is forbidden. Basis type: not-a-claim (normative rule).
- The local metadata validator checks finite properties only: pin form, no `unknown` for a new card, a required meaning-management pin, addressed review links, unique domain profiles, unchanged creation metadata for one card revision, and preserved review-history prefix. Basis type: finite-test (synthetic examples; the text names 24 examples plus eight separately written probes).
- A first failure is kept visible: the initial 0.1 proposal forbade `latest` only for contract pins, an independent check showed `latest` accepted in two revision fields, and revision 0.2 fixed this. The text calls this a specific repair, not proof of immutability, and not a held-out test. Basis type: finite-test (negative result, then fix).

## Limits

- The validator does not establish authenticity of recorded provenance, truth of knowledge, real compatibility of contracts, completeness of the impact graph, or current rights.
- The example contract documents are fictional, not published versions of any contract.
- Real registries, community changes and server migration keep separate acceptance conditions.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The specification gives its status as a normative architecture requirement with a proposed metadata profile (version 0.2), not as a published standard.

## Relation to the full text

This page summarises the specification's own statements. Its own status wording is given in the status row above. No separate editorial review wording exists for specifications yet.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
