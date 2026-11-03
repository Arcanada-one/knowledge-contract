---
artifact_id: MM_A0198
revision_id: MM_A0198-entry-en-r1
title_en: "Semantic Objects, Sources and Verifiable Extraction"
title_ru: "Смысловые объекты, источники и проверяемое извлечение"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P01_semantic_objects_and_extraction.md
---

# Semantic Objects, Sources and Verifiable Extraction

| Field | Value |
| --- | --- |
| Artifact id | MM_A0198 (permanent) |
| Entry page revision | MM_A0198-entry-en-r1 |
| Full text | [Russian original](ru/P01_semantic_objects_and_extraction.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper proposes a profile of the semantic object (`MeaningObject`) and a protocol for verifiable extraction. The profile ties content to specific source editions, operator scopes, composite grounds, alternative readings and separate assessments. The central hypothesis is that such binding can reduce reuse errors in declared task classes; it admits a negative result, since for plain retrieval detailed markup may cost more than it helps. The main edition prepared a model, a protocol, limited example records and a test design, and ran no automatic extraction on full books. The appendix keeps limited executed slices over structured material, which do not establish extraction from free text.

## Claims and their basis

- The example registry holds 24 semantic objects in 101 local records. Basis type: not-a-claim; these are counts of development artefacts, not extraction quality, and no extraction pipeline was run on them.
- The closure of a finite pinned graph reaches a fixed point and is the least closure. Basis type: proof-under-premises (finite graph, given roots and required edges). A missed legend stays missed.
- The other local formal properties are structural consequences of the chosen discipline. Basis type: authors-domain-assessment, not proved novelty.
- The central hypothesis and the plan H01-H08 each have refuting observations. Basis type: hypothesis; none confirmed.
- Appendix slices on structured input exposed first failures that stay visible: seven assessment records of variant B had incompatible `target.scope` and top-level `scope`; four initial `unknown` values for variant A were attributed to the assessor and were not rewritten to `met`; in one earlier round a required `source_conditions` field was missing. Basis type: finite-test; structured inputs only.
- The release cross-check bound rules to 124 exact byte selectors, which include one block reuse (123 distinct blocks). Basis type: authors-domain-assessment; this is naming and byte binding, not extraction quality. The crosswalk phrase about 40 author semantic checks is NOT VERIFIED and is not used.

## Limits

- No production quality, throughput, universal text/image equivalence or accuracy on real books is claimed.
- A structural validator checks pinned references and declared fields, not whether an image was read correctly.
- No real pairs of OCR and verified transcription exist for the three books; OCR accuracy against the original PDF was not measured.
- No cost measurement compares annotation with reading the source.

## Status and what is open

- The late research synthesis gate is OPEN. Independent semantic review of this text has NOT been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The sources MM_A0275, MM_A0263 and MM_A0274 (behind the registry counts) and the gap map MM_A5300 (behind the appendix slices) were NOT read by the card writer; claims resting on them keep the limited wording above.
- The research crosswalk is integrated but is a one-assistant self-check by the kit authors, not independent confirmation.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Where the editorial card corrects the status wording of its abstract (executed appendix slices that a "not run" statement would understate), this page follows the corrected, evidence-bound wording and says so here. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
