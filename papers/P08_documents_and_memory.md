---
artifact_id: MM_A0205
revision_id: MM_A0205-entry-en-r1
title_en: "Documents, Representations and Long-Term Memory"
title_ru: "Документы, представления и долговременная память"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P08_documents_and_memory.md
---

# Documents, Representations and Long-Term Memory

| Field | Value |
| --- | --- |
| Artifact id | MM_A0205 (permanent) |
| Entry page revision | MM_A0205-entry-en-r1 |
| Full text | [Russian original](ru/P08_documents_and_memory.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper treats a document as a defined representation of knowledge for a purpose, audience and genre, and asks what editing and memory must preserve: conditions of applicability, dependent paragraphs, source locators and current permission to use. It separates three levels of result: a specification of obligations, a finite local execution over trusted, already interpreted units, and future empirical work. The execution checks declared dependencies, current admission and the actual Markdown/JSON projection. It does not check whether a quotation matches its primary source or whether the markup is true.

## Claims and their basis

- Quotation fidelity, factual truth, completeness and current validity are independent coordinates (not statistical independence). Basis type: authors-domain-assessment.
- Checking only an edited paragraph gives false acceptance when a stale conclusion remains elsewhere; the whole selected set, explicit conflicts and the delivered projection must be checked. Basis type: authors-domain-assessment. The example was built by the authors; it is not an error rate.
- Restoring a snapshot returns data for comparison but does not restore permissions, provided current state is not overwritten by the old snapshot. Basis type: authors-domain-assessment (conditional, not a proof).
- The last verification layer processed 917 records in three books, with 19,305 field checks and no violations in each of two passes; a control outcome of 15/16 is kept. Basis type: finite-test, local and deterministic. The 1,834 repeated materialisations are not independent observations.
- Two first failures remain visible: in an early load attempt, consistency of the later SQLite readback was not confirmed; and a local replay of 28 journal operations on a navigation book did not reproduce the full readable file (three alt-text copies also changed). Basis type: finite-test, one book each.
- Four hypotheses (fewer contradictions after edits, fewer misapplied caveats, cheaper partial updates, fewer uses of outdated decisions) are planned, not tested. Basis type: hypothesis.

## Limits

- A fabricated but self-consistent trusted input would be accepted.
- Nothing is established about real books, reader comprehension, or a production permission and recovery mechanism.
- Restoration is logical only, not physical erasure or recovery of external copies.
- External studies were not replicated.
- Open: automatic dependency discovery, faithfulness of free paraphrase, locator transfer after OCR.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- A later engineering amendment on artifact layout is not merged into the paper.
- Underlying run reports were not checked; the numbers come from the paper's appendix text.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). It has no abstract section, so this page uses the abstract proposed in the editorial review, which adds the finite results, the two first failures and what is not established. This page follows that evidence-bound wording. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
