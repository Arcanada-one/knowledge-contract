---
artifact_id: MM_A0227
revision_id: MM_A0227-entry-en-r1
title_en: "Content Types and Independent Classification Axes"
title_ru: "Типы содержания и независимые оси классификации"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/SEMANTIC_TYPES.md
---

# Content Types and Independent Classification Axes

| Field | Value |
| --- | --- |
| Artifact id | MM_A0227 (permanent) |
| Entry page revision | MM_A0227-entry-en-r1 |
| Full text | [Russian original](ru/SEMANTIC_TYPES.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification (version 0.7) proposes how to keep apart the differences that matter for search, explanation, document preparation, visual comparison and work execution. It offers ten analytical axes, eight canonical facets of a `MeaningObject`, and a profile for multimodal content. It keeps the 34 general artifact types and the `mm-envelope/0.1` envelope from the artifact registry, and does not add new general types. Practical scope is text and images; audio and video are described only in theory. The text calls the result a working model open to checking and revision.

## Claims and their basis

- One tree of knowledge kinds is insufficient: a figure can describe a device, show an error and quote someone else's solution. Basis type: not-a-claim (design rationale).
- The ten axes are listed with canonical placement of eight facets (`content_kinds`, `discourse_functions`, `aboutness`, `source_position`, `semantic_operators`, `assessment_refs`, `governance_refs`, plus representation modes), attribution as a record, and application scope as a view. Basis type: not-a-claim (normative definition).
- Independence of axes means separate responsibility of fields and a ban on unjustified transitions; it is not statistical independence. Basis type: not-a-claim.
- Missing information is expressed as `unknown`, `not_applicable` or `withheld` with a reason, never as an empty list; an empty `authority_refs` does not confirm permission to act. Basis type: not-a-claim (normative rule).
- Checks run on finite synthetic fixtures for limited structural properties only; the text states this is not a machine-learning or vision-model run, not an annotator study and not processing of three books. Basis type: finite-test (no denominator is given in the specification text itself).

## Limits

- An exhaustive classification of all meanings is not proven; the number of axes is not claimed to be correct.
- Success in structural checks does not establish reference resolution, extraction correctness, faithfulness to the source, interpretation, sufficiency or action results; OCR quality is not carried over to topology.
- A conditional proof of requirement preservation holds only for a known sufficient protected set and does not prove completeness of a wrongly assembled set.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Open by the specification's own account: a future trial must fix the corpus, instructions, vocabularies, references and metrics before evaluation, separate tuning from control, and compare against good OCR, captions and plain page transfer.

## Relation to the full text

This page summarises the specification's own statements; it adds no claims. The full text marks itself `concept_draft`. No separate editorial review wording exists for specifications yet.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
