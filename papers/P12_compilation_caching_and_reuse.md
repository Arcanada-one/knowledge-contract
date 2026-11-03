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

The paper treats reuse of prepared results of extraction, retrieval, composition and professional preparation as a separate admission operation. Reusing a prepared result requires a match with the new request, current constraints, required grounds and the recipient's profile. The paper formalises this boundary, distinguishes levels of recomputation, and states conditional properties, an economic formulation, strong alternatives and grounds for refutation. The outcome is a research model and a finite executable profile. Effectiveness on real books, causal usefulness and industrial correctness remain hypotheses. The one measured efficiency result, a local paired pilot, found no stable gain.

## Claims and their basis

- The central question has two halves: admissibility of carrying a result between requests, which admits conditional proofs, and efficiency at full cost, which stays a hypothesis. Basis type: hypothesis.
- Main conditional property: if the checked properties are finite, the dependency set contains every input affecting them, and the transformation preserves them, they hold after reuse. It is a conditional lemma with a justification and a finite model check, not a mechanised proof; the justification was not read (NOT VERIFIED), and completeness for real content is not claimed. Basis type: proof-under-premises.
- Local exact-versus-off pilot: three pairs, 144 measured requests each, 432 exact-mode reads; latency ratios 1.0185, 0.9982, 0.8017; median 0.9982. No stable gain; no semantic compiler or model, so no token or compilation saving. Basis type: finite-test.
- In R42 all 60 executions matched expected outcomes and no listed violation occurred, yet 36 assessments kept an unresolved mapping and 12 an unknown new condition. The simple branch equalled the graph branch in all 30 cases, with a shared validator. A synthetic cost example gives 10000 versus 1740 units with break-even at N=18; a second example gives a loss of 10849. Basis type: finite-test.
- The contribution is a problem formulation; novelty of the integration is not established. Basis type: authors-domain-assessment.
- A later cross-check by the kit authors, self-checked by one assistant and not independent, reports 13 of 14 first text results passing all conditions (one violation fixed in a separate attempt) and 14 of 14 technical replays against knowledge contracts. Context economy is not measured. Basis type: authors-domain-assessment.

## Limits

- Not established: completeness of dependency manifests for natural language, real error rates, causal usefulness.
- The pilot is one local runtime and did not compare a compilation level with an exact-match cache.
- The false "no match" rule for search is a design rule; its error rate is not measured.
- Untested: harm to rare cases, utility-assessment cost above the gain, false completeness after insertion on real content; token cache and server-side reuse authorisation are also untested.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- This English page is a summary, not a translation, and does not replace the Russian original.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.
- Late synthesis still needs the formal properties document behind the conditional property.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03. Where the editorial card corrects the abstract's status wording, this page follows it. The late synthesis row is only an authors' self-check. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
