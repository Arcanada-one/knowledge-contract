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

The paper concerns how a stored conclusion should be revised when one of its premises changes. Its central counterexample: the old justification may be outdated, other support may remain, a confirmed opposite premise may appear, or data may be insufficient, so a mark "source changed" does not show that a claim is false. The executable profile is limited to structured claims and declared rules. A check on real acquired sources has its own scope and does not measure arbitrary OCR quality, language understanding or industrial agents. The executed basis is an authored finite check on three public documents, reported below with its first failures.

## Claims and their basis

- On three public documents (NIST, NOAA, and a USDA collection from which one recipe fragment was checked), development ran 73/73. The first separately written set (R0) gave 22/24, positive decisions 7/8. After two fixes the repeat (R1) gave 24/24 and 8/8; later total 75/75. Basis type: finite-test. R1 is a known-set regression; 24 variants are not 24 independent sources.
- The bare engine admitted 2 of 2 wrongly trusted markup cases; the source-admission guard rejected 2 of 2. Basis type: finite-test.
- On 12 shared cases a simple direct baseline admitted 7/7 positive candidates (first model 6/7, corrected 7/7). Basis type: finite-test. Superiority is not established.
- Reuse bound to the source head worked in 2 of 2 cases. Basis type: finite-test. General robustness to premise changes is not proven.
- Absence of known proof yields `unknown` or a limited negative, not negation. Basis type: finite-test. First failure kept: a receipt without read target evidence was marked `current`, then corrected to `unknown`.
- Acyclicity is a representation property, not truth of data. Basis type: authors-domain-assessment.

## Limits

- No control case has reference outcome `refuted`, so sensitivity to genuine refutation is not measured.
- All six OCR quality reports in a later pilot carry CER/WER `null`: no benchmark was run, not zero error.
- Origin groups are declared attribution, not statistical independence; the one-team test order is not external replication.
- The finite-graph argument is conditional on true premises and correct rule semantics.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- A proposed addendum on evaluating evidence by origin and exact target awaits executed results; choosing dependency types stays open.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). It has no abstract section; the card proposes one, and the Abstract here rests on the opening section plus that proposal. This page follows the card's evidence-bound wording, which adds the executed counts, first failures and baseline parity. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
