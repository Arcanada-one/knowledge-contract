---
artifact_id: MM_A0209
revision_id: MM_A0209-entry-en-r1
title_en: "Knowledge Compilation: Preparing Results and the Admissibility of Reuse"
title_ru: "Компиляция знания: подготовка результатов и допустимость повторного использования"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P12_compilation_caching_and_reuse.md
---

# Knowledge Compilation: Preparing Results and the Admissibility of Reuse

| Field | Value |
| --- | --- |
| Artifact id | MM_A0209 (permanent) |
| Entry page revision | MM_A0209-entry-en-r1 |
| Full text | [Russian original](ru/P12_compilation_caching_and_reuse.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper treats reuse of prepared results of extraction, retrieval, composition and professional preparation as a separate admission operation. A prepared result keeps the work done, but reusing it requires a match with the new request, current constraints, required grounds and the recipient's profile. The paper formalises this boundary, distinguishes levels of recomputation, and states conditional properties, an economic formulation, strong alternatives and grounds for refutation. The outcome is a research model and a finite executable profile. Effectiveness on real books, causal usefulness and industrial correctness remain hypotheses. The one measured result, a local paired pilot, found no stable gain.

## Claims and their basis

- The central question has two halves: admissibility of carrying a result between requests, which admits conditional proofs, and efficiency at full cost, which stays a hypothesis. Basis type: hypothesis.
- Main conditional property: if the checked properties are finite, the dependency set contains every input affecting them, inputs and interpretation are equivalent, and the transformation preserves them, they hold after reuse. Completeness cannot be shown for natural language by a `complete_manifest` flag. Basis type: proof-under-premises.
- Local exact-versus-off pilot: three pairs, 144 measured requests each, 432 exact-mode reads; latency ratios 1.0185, 0.9982, 0.8017; median 0.9982. No stable gain; no semantic compiler or model, so no token or compilation saving is claimed. Basis type: finite-test.
- In 30 targeted cases (60 executions, run R42) no listed violation occurred, yet 36 assessments stayed unresolved and 12 had an unknown new condition; the simple branch equalled the graph branch in 30 of 30, with a shared validator. Basis type: finite-test.
- A synthetic cost example (10000 versus 1740 units; break-even at N=18) is arithmetic on invented parameters; a second example gives a loss of 10849. Basis type: finite-test.
- The contribution is a problem formulation; novelty of the integration is not established. Basis type: authors-domain-assessment.

## Limits

- Not established: completeness of dependency manifests for natural language, quality of expected-outcome references, real error rates, causal usefulness.
- The pilot is one local runtime, not production latency, and did not compare a compilation level with an exact-match cache.
- The false "no match" rule for search is a design rule; its error rate is not measured.
- Untested refutation criteria: harm to rare cases, utility-assessment cost above the gain, false completeness after insertion on real content.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- This English page is a summary, not a translation, and does not replace the Russian original.
- Late synthesis still needs the formal properties document behind the conditional property and evidence for later reuse obligations.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Where the editorial card corrects status wording of its abstract (which omits the negative pilot), this page follows the corrected, evidence-bound wording. Later material does not raise its status. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
