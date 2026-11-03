---
artifact_id: MM_A0201
revision_id: MM_A0201-entry-en-r1
title_en: "Query, Retrieval and Verifiable Coverage"
title_ru: "Запрос, извлечение и проверяемое покрытие"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P04_query_retrieval_and_coverage.md
---

# Query, Retrieval and Verifiable Coverage

| Field | Value |
| --- | --- |
| Artifact id | MM_A0201 (permanent) |
| Entry page revision | MM_A0201-entry-en-r1 |
| Full text | [Russian original](ru/P04_query_retrieval_and_coverage.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper proposes a profile for moving from a human or agent query to a bounded answer set with checkable grounds. It separates the relevance of a candidate, support for the answer's conditions, completeness of the search, and applicability of the result. The profile links a query plan (`QueryPlan`), a candidate set, three independent coverage reports (`CoverageReport`), pinned source references and stop rules. It allows a useful partial answer and does not treat "nothing found" as "nothing known". Its properties hold only under explicit premises: a finite domain, a query parsed in advance, and author-marked metadata. Only an authored finite model was executed; no search over real books and no comparison with strong alternatives has been run.

## Claims and their basis

- The three coverage reports are independent; the candidate-set report does not support the later two. Basis type: finite-test. Scope: the authored finite model, 97 checks, 97 passed; five finite enumerations cover 352 configurations, which is not 352 independent experiments.
- A negative conclusion is allowed when the domain is explicitly finite, pins are current, the survey is complete and all evaluations are negative. Basis type: proof-under-premises. It does not extend to missed pages, hidden data or OCR errors.
- A second agent wrote 12 minimal API probes and first found 2 defects (an 8-byte PNG signature accepted as a sufficient image; the origin of an irrelevant fact entering the evidence groups). After fixes: 11 pass, 1 pass with limitation. Basis type: finite-test. Not a human review, not an independent implementation.
- A budget stop issues no completeness certificate. Basis type: authors-domain-assessment; a design rule, not measured on real retrieval.
- Deduplicated copies are not independent evidence; uniqueness is declared, not statistically shown. Basis type: authors-domain-assessment.
- Hypotheses H12-01 to H12-08 each have a strong alternative and a revision condition. Basis type: hypothesis; no results.

## Limits

- No real corpus search, no comparison with BM25, dense or hybrid retrieval on independent labels, no cost measurement.
- 36 system scenarios and 9 sequential walkthroughs were planned, not executed.
- Query recognition, server-side vector search, OCR/VLM and products were not run; correct subject markup is a premise.
- A structural SQL-like query over normalised data may solve a task more simply; then no advantage is claimed.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Proposed late additions on separating file, source, meaning and index coverage await executed results.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Its abstract states the status but not the executed basis; this page follows the corrected, evidence-bound wording of the editorial card, which adds the 97/97 check, the 12 probes with their first defects, and the limits above. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
