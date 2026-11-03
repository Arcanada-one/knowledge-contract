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

The paper proposes a profile of the semantic object (`MeaningObject`) and a protocol for verifiable extraction. The profile ties content to specific source editions, operator scopes, composite grounds, alternative readings and separate assessments. The central hypothesis is that such binding can reduce reuse errors in declared task classes; the hypothesis admits a negative result, since for plain retrieval detailed markup may cost more than it helps. The main edition prepared a model, a protocol, limited example records and a test design. Its target is knowledge contract v3 (`3.0.0-draft.1`). No automatic extraction was run on full books in the main text.

## Claims and their basis

- The example registry holds 24 semantic objects in 101 local records, with 30 planned cases and nine editorial walkthroughs. Basis type: not-a-claim; these are counts of development artefacts, not extraction quality.
- The closure of a finite pinned graph reaches a fixed point and is the least closure. Basis type: proof-under-premises (finite graph, given roots and required edges). It says nothing about whether the annotator included every needed edge; a missed legend stays missed.
- The other formal properties are structural consequences of the chosen discipline. Basis type: authors-domain-assessment, not proved novelty.
- The plan H01-H08 tests eight hypotheses (operator scopes, composite grounds, alternatives, scoped dependencies, local revision, separate assessments, extraction versus inference, profile depth), each with refuting observations. Basis type: hypothesis; none confirmed.
- Appendix slices on pre-structured input exposed first failures that stay visible: seven assessment records of variant B had incompatible `target.scope` and top-level `scope`; four initial `unknown` values for variant A were attributed to the assessor's incomplete recognition and were not rewritten to `met`; in one earlier round a required `source_conditions` field was missing. Basis type: finite-test; denominators are those counts.

## Limits

- No production quality, throughput, universal text/image equivalence or accuracy on real books is claimed.
- A structural validator checks pinned references and declared fields, not whether an image was read correctly.
- No real pairs of OCR and verified transcription exist for the three books, and no independent assessment; the causal effect of OCR is not established.
- No cost measurement compares annotation with reading the source. Novelty is not claimed for attribution, conditions or graphs alone; an adapter over an existing formalism may suffice.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Open: the report behind a later layout check was not available; that check concerns file layout only, not extraction fidelity.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Where the editorial card corrects status wording of its abstract (executed appendix slices that a "not run" statement would understate), this page follows the corrected, evidence-bound wording and says so here. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
