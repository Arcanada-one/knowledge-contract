---
artifact_id: MM_A0226
revision_id: MM_A0226-entry-en-r1
title_en: "Policy for Permissible Reuse"
title_ru: "Политика допустимого повторного использования"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/REUSE_POLICY.md
---

# Policy for Permissible Reuse

| Field | Value |
| --- | --- |
| Artifact id | MM_A0226 (permanent) |
| Entry page revision | MM_A0226-entry-en-r1 |
| Full text | [Russian original](ru/REUSE_POLICY.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

This specification (version 1.0) defines a temporal policy for when a previously prepared knowledge result may be reused. The policy is relative to a concrete request, recipient, artifact revision and accepted rule version. It names three time modes (`strict_current`, `historical_pinned`, `bounded_stale`), defines soft and hard deadlines computed from the last sufficient check, and sets a priority order in which prohibitions and current access come before cost savings. The evidence status is stated as a proposed policy with a bounded executable profile.

## Claims and their basis

- Order of checks: prohibitions and current access, then material conditions, result requirements, permissible transformations, time mode, budget, and economic benefit last; saving never cancels earlier obligations. Basis type: not-a-claim (normative rule).
- Three time modes are distinguished, and an unexpired TTL is not proof that nothing changed. Basis type: not-a-claim (normative definition).
- Deadlines count from the last sufficient check, not from the last read; the minimum of applicable deadlines and the request limit applies; a missing deadline is not permission. Issuance on the old basis is allowed only while the upper time bound is strictly below the effective hard deadline, so equality means the window is closed. Basis type: not-a-claim (normative rule).
- Check scenarios are given for a synthetic answer profile (soft 300 s, hard 900 s): access at 100 s and 200 s does not move deadlines, a dependency expiring at 250 s limits issuance, a hard revocation at 120 s stops it. The text says these stay `planned` or `illustrated` until executed and independently checked. Basis type: not-a-claim.
- The table of profile durations is a historical illustrative set from draft 0.3. Basis type: hypothesis (starting values for experiments; correctness is subject to experimental checking).

## Limits

- No production TTL is established. The listed values are not normative and not derived from production data.
- Passing arithmetic checks does not establish optimality of any TTL or completeness of a dependency manifest.
- Real books, network authorities, clocks, distributed issuance, load and causal savings remain separate checks.
- The policy governs use of knowledge only; it does not authorise a physical action, publishing on a user's behalf, or a repeated payment.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Open by the specification's own account: calibration of any numeric candidate, which needs recorded origin, task family, update distribution, quality and cost metrics, and a pilot kept separate from a confirming sample.

## Relation to the full text

This page summarises the specification's own statements; it adds no claims. The full text marks itself `concept_draft`. No separate editorial review wording exists for specifications yet.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).
