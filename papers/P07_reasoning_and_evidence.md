---
artifact_id: MM_A0204
revision_id: MM_A0204-entry-en-r1
title_en: "Reasoning, Justification and Revision of Conclusions"
title_ru: "Рассуждение, обоснование и пересмотр выводов"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P07_reasoning_and_evidence.md
---

# Reasoning, Justification and Revision of Conclusions

| Field | Value |
| --- | --- |
| Artifact id | MM_A0204 (permanent) |
| Entry page revision | MM_A0204-entry-en-r1 |
| Full text | [Russian original](ru/P07_reasoning_and_evidence.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper concerns revising a stored conclusion when one of its premises changes. Its central counterexample: a mark "source changed" does not show that a claim is false, since the old justification may be outdated, other support may remain, an opposite premise may be confirmed, or data may be insufficient. The executable profile covers structured claims and declared rules only. A check on real acquired sources has its own scope and does not measure OCR quality, language understanding or industrial agents. The executed basis is an authored finite check on three public documents.

## Claims and their basis

- On three public documents (NIST, NOAA, and one recipe fragment of a USDA collection), development ran 73/73. The first separately written set (R0) gave 22/24 (positive decisions 7/8). After two fixes the repeat (R1) gave 24/24 and 8/8, then 75/75 after later changes. Basis type: finite-test. R1 is a known-set regression, not new independent confirmation; 24 variants are not 24 independent sources.
- The bare engine admitted 2 of 2 wrongly trusted markup cases; the source-admission guard rejected 2 of 2. On 12 shared cases a simple direct baseline admitted 7/7 positive candidates (first model 6/7, corrected 7/7); superiority is not established. Basis type: finite-test.
- Reuse bound to the source head worked in 2 of 2 cases; consequences of a changed premise are not proven. Absence of known proof yields `unknown` or a limited negative, not negation; first failure: `current` for a receipt without read target evidence became `unknown`. Alternative grounds are kept separately; completeness of automatically found ones is unproven. Basis type: finite-test.
- Acyclicity is a representation property, not truth of data; finite-graph checkability is a conditional argument with examples, not a machine proof. Basis type: authors-domain-assessment.
- Engineering cross-check of the RU10 release: change grounds are recorded in self-assessments of 14 cases; checking single cases found three distinct defects in the saved producer-side graph (lost polarity and scope, a wrong negation flag, example columns read as a definition). Basis type: authors-domain-assessment. A one-assistant self-check by the kit authors, not independent; the three findings are not an error rate and none became working rules.
- Correct choice of dependency type is the next object of refutation: a flawless closure over misclassified relations is possible. Basis type: hypothesis.

## Limits

- No control case has reference outcome `refuted`, so sensitivity to genuine refutation is not measured.
- All six OCR quality reports of a later pilot carry CER/WER `null`: no benchmark ran, not zero error.
- Origin groups are declared attribution, not statistical independence; one-team test order is not external replication.
- Evaluation covers given candidates, not generation of answers.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- A proposed addendum (a technical pass creates no support) is a hypothesis awaiting executed results.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter, links aside). It has no abstract section; this Abstract rests on the opening section plus the card's proposal. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
