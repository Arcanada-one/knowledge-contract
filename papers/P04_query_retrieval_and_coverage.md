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

The paper proposes a profile for moving from a human or agent query to a bounded answer set with checkable grounds. It separates relevance, support, search completeness and applicability. It links a query plan (`QueryPlan`), a candidate set, three independent coverage reports (`CoverageReport`), pinned sources and stop rules. It allows a useful partial answer and does not treat "nothing found" as "nothing known". Its properties hold only under explicit premises: a finite domain, a query parsed in advance, and author-marked metadata. Only an authored finite model was executed; no real-book search has been run.

## Claims and their basis

- The three coverage reports are addressed independently. Basis type: finite-test. Scope: the authored finite model, 97 checks, 97 passed. Five finite enumerations cover 352 configurations, which is not 352 independent experiments.
- A negative conclusion is allowed only for an explicitly finite domain with current pins, a complete survey and all evaluations negative. Basis type: proof-under-premises. It does not extend to missed pages, hidden data, OCR errors or subject interpretation. Linked MM_A0372 was NOT read.
- A second agent wrote 12 minimal API probes and first found 2 defects: an 8-byte PNG signature accepted as a sufficient image, and an irrelevant fact's origin entering the evidence groups. After fixes, 11 probes passed and 1 passed with a limitation. Basis type: finite-test. Not a human review, not an independent implementation.
- An engineering cross-check of the RU10 release maps all 427 recognised pages; the selected rule supports are 123 blocks on 69 pages out of 2746 blocks, which is not a share of the book's meanings. Basis type: authors-domain-assessment. It is a one-assistant self-check by the kit authors, not independent confirmation. That agents select ready rules and skills is NOT VERIFIED: a design statement, no run record.
- A budget stop issues no completeness certificate (the operational profile MM_A0383 was linked, NOT read), and deduplicated copies are not independent evidence (uniqueness is declared, not statistically shown). Basis type for both: authors-domain-assessment; design rules, not measured on real retrieval.
- Hypotheses H12-01 to H12-08 each have a strong alternative and a revision condition. Basis type: hypothesis; no results.

## Limits

- No real corpus search, no comparison with BM25, dense or hybrid retrieval on independent labels, and no cost measurement.
- 36 system scenarios and 9 sequential walkthroughs were planned and not executed.
- Query recognition, server-side vector search, OCR/VLM and products were not run; automatic semantic search and recall over the whole book are not assessed.
- A structural SQL-like query over normalised data may solve a task more simply; then no advantage is claimed.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The research synthesis crosswalk is integrated only as authors-domain-assessment. A proposed addendum on separating file, source, meaning and index coverage has no executed result.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Its abstract states the status but not the executed basis; this page follows the corrected, evidence-bound wording of the round-two editorial card. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
