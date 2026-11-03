---
artifact_id: MM_A0202
revision_id: MM_A0202-entry-en-r1
title_en: "Context Composition under a Limited Budget"
title_ru: "Составление контекста при ограниченном бюджете"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P05_budgeted_context_composition.md
---

# Context Composition under a Limited Budget

| Field | Value |
| --- | --- |
| Artifact id | MM_A0202 (permanent) |
| Entry page revision | MM_A0202-entry-en-r1 |
| Full text | [Russian original](ru/P05_budgeted_context_composition.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper studies how to compose a context from a fixed set of candidates under limited resources. It proposes a conditional model in which query requirements, joint grounds, mandatory dependencies, permitted transformations and the actual representation form one object of verification. Ranking single fragments does not establish that their union is sufficient. The main result is a specification, conditional properties, counter-models, an executable finite model and a plan for a comparative study. Empirical advantage on real books, people, models or products is not established. The measured basis is an authored finite check plus API probes; real model tokens, OCR/VLM and human trials were not measured.

## Claims and their basis

- Ranking does not settle sufficiency: two ingredients from different dishes do not meet a one-dish condition. Basis type: finite-test, on authored vectors.
- The finite check had 101 checks: 24 authored vectors, 68 negative controls, 5 enumerations over 576 configurations (not independent experiments), 2 constructed counter-models, 2 algorithm-boundary checks. Basis type: finite-test.
- Seventeen API probes were written by an author who did not use the authored vectors or expected answers. First run: 13 pass, 4 findings; repeat on the same inputs: 17/17. Basis type: finite-test. Separation of authorship within one session is not an independent replication.
- A special case (cover requirements with at most k independent unit-cost packages) contains SET COVER and is NP-hard. Basis type: proof-under-premises. It says nothing about every real query.
- Diminishing returns cannot be assumed: a scheme and a legend may each have zero sufficiency yet together close a requirement. Basis type: proof-under-premises, as a constructed counter-model; frequency not measured.
- Eight hypotheses H13 have status `empirical_result_absent`. Basis type: hypothesis.

## Limits

- The unit is UTF-8 bytes of deterministic JSON, not real model tokens, human reading or time under load.
- Exact selection covers subsets of at most 16 given representations in canonical order only.
- Cited external theorems are quoted with their premises, not proved here, and not verified for this page.
- 36 system scenarios and 9 sequential walkthroughs were not executed; sample size, effects and thresholds are unjustified. A simpler method may be preferable.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- A proposed closure lemma and a proposal on ALL/ANY alternatives await placement after executed results.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Where its abstract understates what was run, this page follows the corrected, evidence-bound wording of the editorial card and says so: it adds the 101 checks and the 17 probes with first-run findings, and drops the word "independent" for the probe separation. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
