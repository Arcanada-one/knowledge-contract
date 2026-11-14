---
name: "agent-situation-controls"
title: "Context Controls: Finite Checks of Situation State and Context Projection"
short_title: "Context Controls"
subtitle: "Finite Checks of Situation State and Context Projection"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "research-draft"
description: "Executed authored finite controls for a small situation-state model, including a preserved development defect and corrected premise binding."
sources:
  - "Knowledge Contract project corpus and publication edition"
---

# Context Controls: Finite Checks of Situation State and Context Projection

**Author:** Pavel Valentov · **Publication edition:** 1.1 · **Review state:** author-produced evidence with bounded same-controller review and harness repair; independent acceptance NOT_VERIFIED.

## 1. Question and bounded claim

This study asks whether a small deterministic model preserves its declared observation-time, scope, dependency and context-budget rules on explicitly authored finite inputs. It accompanies the proposed [Agent Situation](../../../papers/agent-situation/PAPER.md) architecture. It does not test whether an LLM understands its environment better, completes more real tasks or saves money.

The corrected implementation matched **21 of 21 authored control outcomes** and detected **three of three deliberately disabled guards**, without mutation-run exceptions. The first 18-control suite had also passed, yet a subsequent review found a real delayed-derivation defect. Both facts are material: the revised cases demonstrate a correction, while the initial false reassurance limits what any finite pass can establish.

## 2. Materials and provenance

All observations, expected values and programs in this study were newly authored for this finite demonstration. No third-party dataset, private account, external service or live permission source was used. Code follows the repository's Apache-2.0 terms and original prose/evidence its existing attribution policy.

The initial [design input](checks/DESIGN_INPUT.md) records eighteen intended control families before implementation in this working session. This chronology is an author record, not an independent preregistration. The implementing agent also wrote the runner and literal [expected outcomes](checks/expected.json). A second agent inspected the paper and code under the same controller/model family, reproduced two defects and rechecked the correction. That separation is useful review, but actual independence remains NOT_VERIFIED.

The [origin manifest](evidence/origin.json) binds every current evidence file by exact SHA-256 and byte size. Its original three entries are unchanged; its exact initial bytes are preserved in the [historical origin](development/inventory-baseline/origin.json). The historical [payload manifest](MANIFEST.json) identifies the prototype at that execution, including the preserved development version. The original [finite-run record](evidence/finite-run.json) contains source digests, runtime, command, complete operation traces, expected outcomes, counts and limitations. Its recorded runtime is Python 3.12.14. The historical execution records and payload manifest remain unchanged; the current origin adds the dated successor records. The original runner's exact bytes are also retained in [inventory-baseline](development/inventory-baseline/README.md); the current runner and its successor execution are bound separately by the [inventory repair receipt](evidence/20261114-inventory-receipt.json).

## 3. Model and execution method

The reference model uses one nonnegative integer clock domain and synthetic scope/source labels. It maintains per-producer sequence order, source-attributed values, explicit unknown/conflict states, TTL policy and local dependency-version pins. Its projector computes required closure, checks readiness and fits optional records only into remaining abstract capacity.

The model makes no external requests. It has no authentication, real grants, effect dispatcher, LLM, distributed clock protocol or durable recovery. A source label is a fixture identifier. A structurally ready false permission fixture does not authorize anything.

The runner evaluates hand-authored expectations and exits nonzero when an ordinary control fails or an intended broken variant is not detected. The three broken variants disable freshness, mandatory dependency closure or scope checking. Their observed mismatches are intentional negative controls; they are not unexpected runtime exceptions.

| Control group | Cases | Observed scope |
| --- | --- | --- |
| Time, uncertainty and replay | 1–4 | TTL boundary, genuine refresh, unknown versus false/zero, replay age and clock anomalies |
| Ordering and conflicting sources | 5–7 | Older/equal producer sequence, independent conflict and duplicate identity |
| Dependency and event relevance | 8–10 | Relevant versus unrelated updates, heartbeat behavior and account scope |
| Context capacity and omission | 11–13 | Exact-fit closure, one-unit-short failure, unknown mandatory records and stable optional order |
| Critical use and unresolved outcomes | 14–18 | Revocation fixture, changed prerequisite, expiry backstop, targeted refresh and unknown effect result |
| Review-added regression controls | 19–21 | Delayed derivation with missing/obsolete/impossible pins, valid delayed positive, modified snapshot rejection |

The 87 compared top-level result fields are nested checks within these controls. They are not 87 independent samples. The three mutants are a separate denominator; combining them with ordinary controls into one success percentage would be misleading.

## 4. Preserved failure and correction

In the original model, a derived observation was bound to whatever dependency version was current when it arrived. Review executed this sequence:

1. Observe `a = old` at time 0.
2. Replace it with `a = new` at time 5.
3. At time 10 receive `b = derived from OLD a`, whose declared observation time is 0.
4. Ask for a context requiring `b`.

The original implementation returned `KNOWN` and `READY`, binding the old derivation to version 2 of its premise. The initial eighteen controls had not covered this arrival ordering. The [reproduced counterexample](development/v1/delayed-derivation-counterexample.json), original source and initial passing record remain in [development/v1](development/v1/README.md).

The repair requires explicit premise pins instead of binding at receipt. Missing pins produce `UNBOUND_DEPENDENCIES`; obsolete pins produce `INVALIDATED`; a pin to a premise first received after the declared derivation time produces `INVALID_DERIVATION_TIME`. Control 20 confirms that a delayed derivation with matching, temporally available premises can still be `READY`. Thus the repair is not an indiscriminate rejection of every delayed observation.

A second review probe removed version entries from an issued snapshot and changed a prerequisite. The old validator returned `VALID`. The corrected validator compares against the canonical contents of a locally issued snapshot and rejects modified or omitted pin data. This is an in-process integrity check, not cryptographic authentication or a distributed security boundary.

The [review record](../../../reviews/agent-situation/20261114-REVIEW.md) retains the original findings, exact source hashes, correction dispositions and the separate same-controller recheck.

## 5. Results

A continuation review found a separate defect in the runner's completeness claim: removing only the last registered callable let a truncating pairing execute 20 of 21 fixtures and still report success. It also counted all 87 fixture fields instead of the 84 belonging to executed controls. The complete historical 21/21 execution is not invalidated by this omission probe; the defect concerns what the harness would accept after registration loss. The [inventory review](../../../reviews/agent-situation/20261114-INVENTORY.md) records the isolated probe and correction.

The successor validates a one-to-one correspondence between declared IDs, callable registrations and fixtures before execution, binds negative controls by ID, checks the complete executed inventory and counts actual performed field predicates. Nine behavioral checks cover complete/reordered registration, missing/extra/mismatched/duplicate entries and unperformed-comparison accounting. Neither the situation model nor its literal expected outcomes changed.

| Observation | Actual result | Interpretation |
| --- | --- | --- |
| Initial authored suite | 18/18 matched | The initial suite missed a real delayed-derivation defect |
| Initial disabled guards | 3/3 detected | The selected freshness, closure and scope cases discriminated those variants |
| Review counterexample | Obsolete derivation incorrectly returned READY | A concrete failure outside the initial suite's arrival-order coverage |
| Corrected authored suite | 21/21 matched; 0 failed | Eighteen original controls plus three identified review additions |
| Corrected disabled guards | 3/3 detected; 0 exceptions | The selected negative controls remain discriminating |
| Separate internal recheck | 21/21 and 3/3 | Same-controller non-author inspection and execution; independence NOT_VERIFIED |
| Inventory omission probe | 20/20 reported success against 21 fixtures | A separate harness completeness and accounting defect, preserved as adverse evidence |
| Inventory repair replay | 21/21; 3/3 mutants; 87 performed field predicates | Same finite model and expected outcomes, with validated registration |
| Inventory/accounting controls | 9/9 | Separate behavioral checks of the repaired harness; same-controller authorship |
| LLM/network/effect calls in the model | 0 | No agent-performance or real-world action experiment occurred |

These outcomes establish only the recorded finite predicates. They do not estimate a population failure rate, prove complete correctness, establish the paper's empirical hypothesis or validate a live consumer. There is no measured LLM token cost, monetary saving or production utility result.

## 6. Reproduction without rewriting retained evidence

From the repository root, copy the study to a temporary execution directory. The runner writes both its JSON report and a compact execution record; running a copy keeps the committed historical evidence unchanged.

```sh
KC_SITUATION_RUN="$(mktemp -d)"
cp -R engineering/studies/agent-situation-controls/. "$KC_SITUATION_RUN/"
python3 -B "$KC_SITUATION_RUN/checks/check_agent_situation.py" --evidence "$KC_SITUATION_RUN/evidence/finite-run.json"
python3 -B -m unittest discover -s engineering/studies/agent-situation-controls/checks -p test_inventory.py -v
```

Expected terminal summary: `FINITE_CONTROLS_PASS`, 21/21 controls and 3/3 detected disabled guards. Timestamps, runtime strings and command paths may differ on replay; compare declared outcomes and source hashes rather than requiring identical evidence bytes across environments.

The archived development version is intentionally defective. Its initial runner demonstrates the original eighteen passing cases; the preserved counterexample identifies the missed behavior. Do not overwrite that record with a corrected result.

## 7. Limits and next research step

The checks use authored, implementation-informed scenarios. Source sequences, version counters and clocks exist inside one process; there is no independent producer attestation. Conflicts are handled conservatively without an authority-ranking resolver. The derivation-time feasibility rule uses this model's receipt history and can be more conservative than a real distributed system with authenticated historical evidence.

Required closure is only as complete as the declared graph. Abstract integer budgets are not token accounting. A model can misinterpret a correct context, and an always-refusing system can appear conservative while being useless. The proposed [agent experiment](../../../roadmap/agent-situation/EXPERIMENT.md) therefore includes valid completion, unnecessary refusal, stale actions and full maintenance costs, with a strong deterministic baseline.

That experiment remains unexecuted. This study supports continued development and review of the finite design, not normative admission, broader autonomy or publication of a proven agent improvement.
