---
artifact_id: MM_A0208
revision_id: MM_A0208-entry-en-r1
title_en: "Evaluation, Counterexamples and the Limits of Claims"
title_ru: "Проверка, контрпримеры и границы утверждений"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P11_evaluation_and_falsification.md
---

# Evaluation, Counterexamples and the Limits of Claims

| Field | Value |
| --- | --- |
| Artifact id | MM_A0208 (permanent) |
| Entry page revision | MM_A0208-entry-en-r1 |
| Full text | [Russian original](ru/P11_evaluation_and_falsification.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper proposes a programme for testing meaning management as a whole process: request, retrieval, coverage assessment, bounded package, application, observable result, and back-tracing with revision. The scientific question is whether explicit meaning objects, conditions, dependencies and provenance help a person or a model reach a better-grounded result under limited source access and budget. The paper states what is to be checked and what would refute each hypothesis. It does not answer the question: local targeted comparisons against a strong flat implementation gave equal statuses and no superiority. An appendix keeps runs R37-R44, including first failures.

## Claims and their basis

- The question is open; the six hypotheses in the paper's table remain hypotheses, with no comparison on a representative or independent load. Basis type: hypothesis.
- Local graph-versus-flat comparisons gave equal results and no superiority: 30 of 30 pairs (R42), 8 pairs (R43), 51 pairs (R44). None is representative, independent or blind; in R42 both branches share one validator. Basis type: finite-test.
- The first integration checks in R44 gave 15 of 16 expected outcomes (one expectation was wrong); the result was not replaced by 16 of 16. Basis type: finite-test.
- The split into eight verification subjects and three separate coverage reports are design decisions backed by constructed counterexamples, not measured on real queries. Basis type: authors-domain-assessment.
- Preservation of obligations under exact reuse holds only for immutable content, matching requirements and passed admission checks; the justification is in another document. Basis type: proof-under-premises.
- No observations on real users exist; for agents only limited local model answers (R43: 16, R44: 10; not blind). Basis type: authors-domain-assessment.

## Limits

- Conclusions concern observable behaviour for given inputs and versions, not understanding.
- The catalogue of 320 synthetic plans and 18 prepared illustrations is not a sample of solved tasks.
- Results on well-known books cannot exclude prior model exposure to the text.
- A pilot in the related reuse paper compared exact reuse with a no-cache mode (median latency ratio 0.9982, no stable gain); it did not compare a compilation level with an exact-match cache, so that falsification criterion has not been applied.
- Passed technical checks are not evidence of superiority.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- This English page is a summary, not a translation, and does not replace the Russian original.
- Late synthesis still needs the formal properties behind the reuse row.
- Held inconsistency: the appendix gives one corpus audit as 5 594 flags and 169 ledger rows and elsewhere as 5 538 flags and 174 ledger edits; unexplained.
- Held contradiction, not reconciled: this paper reports 51 A/B pairs in R44, whereas the P13 paper reports 5 pairs and 24 projections for R44.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Where the editorial card corrects status wording of its abstract (which does not say the question is unanswered or report the equal A/B results), this page follows the corrected, evidence-bound wording. Later material does not raise status. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
