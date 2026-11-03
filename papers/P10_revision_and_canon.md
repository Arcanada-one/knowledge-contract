---
artifact_id: MM_A0207
revision_id: MM_A0207-entry-en-r1
title_en: "Revision of Knowledge, Versions and Acceptance of Norms"
title_ru: "Пересмотр знания, версии и принятие норм"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P10_revision_and_canon.md
---

# Revision of Knowledge, Versions and Acceptance of Norms

| Field | Value |
| --- | --- |
| Artifact id | MM_A0207 (permanent) |
| Entry page revision | MM_A0207-entry-en-r1 |
| Full text | [Russian original](ru/P10_revision_and_canon.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper sets rules for changing knowledge, its grounds, norms and chosen representations, connecting them with history, publication and current admission. A finite revision model passed 73 checks with fixed inputs (73 passed, 0 failed); three model defects were found and fixed during preparation. In one observation of a file operation, a separate copy failed finalisation in a previous update (301 of 302 save operations succeeded) and the service gave no cause; the full archive still matched the canonical sources (348 of 348 hashes). No real distributed backend, authentication, books or classifier were used, and 36 subject and load setups remain planned and not executed. Superiority over simply replacing the last record is not shown.

## Claims and their basis

- Seven coordinates are distinguished: existence of content, assessment of its grounds, applicability, normative acceptance, package publication, choice of current state and completion of delivery. Success on one does not change another. Basis type: authors-domain-assessment; seven is not claimed necessary or complete.
- The finite machine passed 73 checks (24 authored vectors, 39 negative controls, 5 finite enumerations, 5 positive), covering properties CP01-CP12. Basis type: finite-test. The counts 73 and 66 (configurations) use different units.
- Three defects of the first model version were found by the authors and fixed: a boolean accepted as an integer receipt generation, a receipt confirmed without an observed publication effect, and the path `.` accepted as a manifest member. Basis type: finite-test. A second agent's look at 12 boundary observations found no new blocking defects; this is not human expert review.
- In the single R0015 observation, one separate copy stayed at an old version while the archive was intact (348 of 348); cause not disclosed; conditional replacement then succeeded. Basis type: finite-test; one operation, not repeated.
- Dependency analysis distinguishes AND/OR structures of sufficient grounds. Basis type: authors-domain-assessment; completeness of dependency discovery was not measured.
- Four hypotheses (separated states, typed dependencies, partial-publication reconciliation, versioned canon) are untested. Basis type: hypothesis.

## Limits

- Authentication and atomic external storage are assumptions, not results.
- Real acceptance, deployment and rollback of a contract registry were not run.
- Counts of sources, graph nodes or passed checks do not show superiority.
- Results of the 36 planned setups are absent, as are 9 sequential reviews.
- Two numbers from different instruments (786/12 and 772/0) are not comparable.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- The glossary lacks a row for `CanonSnapshot`; a later layout amendment is not merged into the paper.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Its opening paragraph, which serves as its abstract, omits executed results and first failures; this page follows the corrected, evidence-bound wording from the editorial review. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
