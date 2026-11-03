---
artifact_id: MM_A0228
revision_id: MM_A0228-entry-en-r1
title_en: "Independent Statuses, Assessment Scopes and Transitions"
title_ru: "Независимые статусы, области оценки и переходы"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/STATUS_MODEL.md
---

# Independent Statuses, Assessment Scopes and Transitions

| Field | Value |
| --- | --- |
| Artifact id | MM_A0228 (permanent) |
| Entry page revision | MM_A0228-entry-en-r1 |
| Full text | [Russian original](ru/STATUS_MODEL.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification (model version `status-model/0.1`) argues that a single global label such as "ready", "valid" or "reliable" is insufficient, because it mixes presence of data, semantic support, execution, external effects, currency and scientific status. It introduces 22 independent axes with addressable observations and rules for change, and describes several of them: coverage of a request, run phase and outcome, stop reason, effect observation, check result, research status, case status and data origin. The text calls itself a design model, not a ready industrial schema.

## Claims and their basis

- A single global status is insufficient; statuses are separate axes, each relative to pinned requirements, target, scope and snapshot. Basis type: not-a-claim (design rationale and normative definition).
- Coverage uses `supported`, `partial`, `unsupported`, `conflicted` and `unknown`; coverage reports are addressed separately per stage (candidate set, context package, output), because assembly may drop found conditions. Basis type: not-a-claim (normative definition).
- Operation outcome, stop reason, effect observation and check result are different things: `finished` does not settle the fate of a remote action, `failed` does not mean rollback. Basis type: not-a-claim (normative rules).
- Research status keeps the vocabulary `concept_draft`, `protocol_frozen`, `results_available`, `reviewed`, with a required scope; `reviewed` requires references to author, subject, method and conclusion. Basis type: not-a-claim (normative rule).
- Case status uses `planned`, `illustrated`, `executed`, `validated`; a failed run still counts as executed, and an illustration on an artificial fragment does not confirm work on a real book. The text states that 320 cases remain `planned` and 18 general examples are illustrations. Basis type: not-a-claim (status statement with stated counts).
- A public claim of a supported scenario must name profile, scope, inputs, limits, system version, protocol and the actual type of evidence; a document status or a passing structural validator does not support a claim that a system works. Basis type: not-a-claim (normative rule).

## Limits

- The model is not a finished industrial schema and does not itself establish any result for a system.
- The old `validation_status` field is kept only as a short field for early illustrations; a bare `passed` without a subject does not show contract suitability.
- Local finite checks described in the text do not replace system trials or checks on real material.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Open by the specification's own account: planned system trials remain planned, and real-book cases are not executed.

## Relation to the full text

This page summarises the specification's own statements; it adds no claims. The full text marks itself `concept_draft`. No separate editorial review wording exists for specifications yet.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
