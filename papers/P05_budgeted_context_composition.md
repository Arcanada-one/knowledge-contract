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

The paper studies how to compose a context from a fixed set of candidates under limited resources. It proposes a conditional model in which requirements, joint grounds, mandatory dependencies, permitted transformations and the actual representation form one object of verification. Ranking single fragments does not establish that their union is sufficient. The main result is a specification, conditional properties, counter-models, a finite executable model and a comparison plan. Executed: 101 finite checks and 17 API probes. Empirical advantage on real books, people, models or products is not established.

## Claims and their basis

- Ranking does not settle sufficiency: two ingredients from different dishes do not meet a one-dish condition. Basis type: finite-test, authored vectors; real-query failure rates are not measured.
- The finite check had 101 checks: 24 authored vectors, 68 negative controls, 5 enumerations over 576 configurations (not independent experiments), 2 constructed counter-models and 2 boundary checks. Basis type: finite-test. Separately, 17 API probes were written without the authored vectors or expected answers; the first run gave 13 pass and 4 findings, the repeat on the same inputs 17 passes. Authorship separation within one session is not an independent replication.
- A special case (cover requirements with at most k independent unit-cost packages) contains SET COVER and is NP-hard. A scheme and a legend may each be insufficient yet together close a requirement, so diminishing returns cannot be assumed. Basis type for both: proof-under-premises; hardness of real queries and effect frequency are not established.
- A closure lemma (an addendum, not in the Russian text): the smallest mandatory closure in a finite graph is the fixed point of adding needed vertices. Basis type: proof-under-premises (fixed vertices, ALL-type edges, complete edges). A machine check enumerated all 512 graphs on three vertices; beyond that the lemma rests on the written proof.
- An engineering cross-check of the RU10 release: a structural validator rejects a control omission of a critical condition (selftest, K08-condition-1). Basis type: authors-domain-assessment (one-assistant self-check by the kit authors, not independent). Minimality, optimality and token reduction are not established; the meaning of the crosswalk's "R01 exposes the whole core" is NOT VERIFIED.
- Eight hypotheses H13 have status `empirical_result_absent`. Basis type: hypothesis; no results.

## Limits

- The unit is UTF-8 bytes of deterministic JSON, not model tokens, human reading or time under load.
- Exact selection covers subsets of at most 16 given representations, canonical order only.
- Cited external submodular-optimisation theorems are quoted with premises, not proved here and not verified by the writer.
- 36 system scenarios and 9 sequential walkthroughs were not executed; sample size, effects and thresholds are unjustified, and causal usefulness is not established.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- A proposal on ALL/ANY alternatives (hypothesis) awaits executed results.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). This page follows the corrected, evidence-bound wording of the round-two editorial card; it adds the executed counts and drops "independent" for the probe separation. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
