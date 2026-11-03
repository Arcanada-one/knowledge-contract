---
artifact_id: MM_A0221
revision_id: MM_A0221-entry-en-r1
title_en: "Identity, Dependencies and Invalidation"
title_ru: "Идентичность, зависимости и инвалидирование"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/CACHE_IDENTITY_AND_INVALIDATION.md
---

# Identity, Dependencies and Invalidation

| Field | Value |
| --- | --- |
| Artifact id | MM_A0221 (permanent) |
| Entry page revision | MM_A0221-entry-en-r1 |
| Full text | [Russian original](ru/CACHE_IDENTITY_AND_INVALIDATION.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification sets out how a stored, derived result is addressed, found as a candidate, revised when its basis changes, and admitted for a new delivery. It separates payload identity, build identity, lookup identity and a mutable current head, and treats byte equality, recipe equality, meaning compatibility, sufficiency for a request and authority to deliver as different relations. It also covers negative and top-k results, change events, late workers and restore. The result is a research specification with a finite executable profile; the text states that a real distributed system is not yet implemented.

## Claims and their basis

- A hash does not prove origin, truth or a current grant. Digests are compared with algorithm, domain and profile version. Basis type: not-a-claim (normative definition).
- A negative, exhaustive or ranked result carries its scope, predicate, profile, index generation and confirmed observation boundary, since adding a matching object can change the result. Basis type: not-a-claim.
- The same event ID with the same bytes is handled idempotently; the same ID with different content is a conflict that ends trust in that range until reconciled. Basis type: not-a-claim.
- If the affected set cannot be proven, a conservative object or scope reset applies; its cost and false revisions are to be measured separately. Basis type: not-a-claim.
- Under stated premises (complete dependency set, correct oracle, consistent guard, fencing), the model must not allow current publication or delivery that was forbidden before check point L. Basis type: proof-under-premises. Successful examples do not show the premises hold in a real service.
- Minimal checks cover negation and quantifiers, tenants, null versus absence, gaps, lost tail, revocation before TTL, a late worker and restore after revocation; the text gives no counts itself. Basis type: finite-test (denominator not stated in this text).

## Limits

- No distributed system is implemented. The finite model assumes a trusted sequential oracle and an atomic check-and-change operation; a distributed transaction, barrier or lease needs separate implementation and analysis.
- A watermark marks a processed boundary in its own scope; it does not prove completeness of subject knowledge.
- After check point L, already-read information is not promised to disappear at the recipient.
- Conformance with RFC 8785 or another external serialisation standard is not claimed from the use of JSON.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The front matter gives version 1.0, status `concept_draft`, evidence status `research_proposal_with_bounded_executable_profile`.
- Publication of sources, index and events under partial failure is handed to a later pass and is not settled here.

## Relation to the full text

This page summarises the specification's own statements; every rule, number and limit above comes from the Russian text, not from outside material. No separate editorial review wording exists for specifications yet, so no reviewed status wording is applied here.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
