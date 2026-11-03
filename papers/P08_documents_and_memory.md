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

- Quotation fidelity, factual truth, completeness and current validity are independent coordinates, not in the statistical sense. Basis type: authors-domain-assessment.
- Checking only an edited paragraph gives false acceptance when a stale conclusion remains elsewhere. The whole selected set, conflicts and delivered projection must be checked. Basis type: authors-domain-assessment. The example is author-built, not an error rate.
- Restoring a snapshot returns data but does not restore permissions, if current state is not overwritten. Basis type: authors-domain-assessment (conditional, not a proof).
- The last verification layer processed 917 records in three books, with two passes of 19,305 field checks and no field violations. Basis type: finite-test, local and deterministic. The repeated materialisation does not create 1,834 independent semantic observations. A control outcome of 15/16 is kept together with a separate correction.
- First failures stay visible. In an early load attempt, consistency of the later SQLite readback was not confirmed. A local replay of 28 ledger operations on a navigation book did not reproduce the full readable file, and three alt-text copies also changed. A late failure after the CURRENT pointer replacement, before fsync completed, was also found. Basis type: finite-test, one book each.
- The RU10 release cross-check: 13 of 14 first answers passed the narrow conditions, and the T09 rejection is kept with a separate corrected attempt. Basis type: authors-domain-assessment, a one-assistant self-check.

## Limits

- Nothing is established about real books, reader comprehension, or a production permission and recovery mechanism.
- Restoration is logical only, not physical erasure or recovery of external copies.
- Four hypotheses (fewer contradictions, fewer misapplied caveats, cheaper partial updates, fewer outdated decisions) are planned, not tested; external studies were not replicated.
- Open: automatic dependency discovery, free paraphrase, locator transfer after OCR, long-term service operation.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.
- The crosswalk content is a one-assistant self-check, not independent confirmation.
- Underlying run reports were not opened; figures come from the appendix text. A later artifact-layout amendment is not merged.

## Relation to the full text

The Russian full text is the unchanged terminology edition of 2026-11-03. It has no abstract section, so this page uses the abstract proposed in the editorial review and follows its evidence-bound wording. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
