---
title: "Agent Situation: Draft Engineering Design"
status: "author-draft"
language: "en"
license: "CC-BY-4.0"
sources:
  - "Knowledge Contract project corpus and publication edition"
  - "Agent Situation — Dey 2001"
  - "Agent Situation — ROS Clock and Time"
  - "Agent Situation — ROS QoS Jazzy"
  - "Agent Situation — Ernst et al. 2026"
  - "Agent Situation — Sumers et al. 2024"
---

# Agent Situation: Draft Engineering Design

This is a nonnormative design proposal under RM18 Agent Application, dated 14 November 2026. It accompanies [Agent Situation](../../papers/agent-situation/PAPER.md), the [finite control study](../../engineering/studies/agent-situation-controls/STUDY.md) and an [unexecuted experiment protocol](EXPERIMENT.md). It introduces no normative requirement identifiers, native admission or new live task authority.

## 1. Purpose and implementation boundary

The target is a runtime that can initialize a bounded view of its circumstances, reconcile changes, and provide task-specific context to an LLM without confusing data, evidence and permission. The present reference implementation is a finite standard-library model. It receives synthetic observations; it neither discovers real accounts nor calls tools, models, sensors or external effect APIs.

Keep five components separate:

| Component | Responsibility | Candidate output |
| --- | --- | --- |
| Acquisition adapters | Read already authorized sources; record observation identity, timing and scope | Observation or explicit unavailable result |
| Situation reducer | Reconcile producer revisions, unknowns and conflicts; invalidate dependencies | Versioned state with reasons |
| Refresh planner | Select relevant overdue or invalid observations and avoid irrelevant rescans | Observation requests, wait or stop |
| Context projector | Include required dependency closure within a declared budget | Ready view, NOT_READY or NOT_FIT |
| Effect boundary | Apply the actual system's current permission, target-version and idempotency controls | External result receipt or unresolved outcome |

Only parts of the reducer, refresh planner and projector are modeled in the finite study. Its structural “ready” result is not a capability, authorization or execution receipt. Authentication, atomic external actions, hostile-source verification and calibrated utility optimization require separate implementations.

## 2. Startup profiles

A profile supplies required fields for a particular operation, optional fields, acquisition sources, clock assumptions, budgets and expiry policies. Avoid a universal all-or-nothing startup gate.

Suggested first profiles:

- **Conversational response:** current request, active role, session scope, relevant continuing goals, applicable constraints and unknowns that affect the answer.
- **Repository maintenance:** repository and current branch/revision, authorized work scope, in-flight CI or writes, tool availability, source-file dependencies and current completion evidence.
- **Browser task:** authenticated account scope when observable, current page/task state, permitted operation, pending transaction state and authoritative result evidence.
- **Physical agent:** local pose/frame, available sensors and actuators, operational limits, relevant scene observations and explicit missing global localization.

These are candidate profiles, not deployed integrations. Physical surroundings remain unobserved without an available authorized sensor. “Not applicable” is profile-specific; it is not the default for a failed read.

A startup controller loads trusted host metadata, reads the minimal critical sources, reconciles saved state, and returns a partial readiness record before a bounded deadline. Optional failed reads remain unknown/unavailable. A critical missing field produces an observation request or an explicit inability to perform that operation. Initialization can occur before user interaction only if the host exposes that lifecycle hook.

## 3. Candidate records and interfaces

An adapter observation carries field/entity identity, scope, producer identity, event identity, producer sequence or revision, value/unknown status, observation time, receipt time, clock domain and declared validity policy. A derived observation additionally carries the actual dependency revisions used to derive it. Binding to the current dependencies at receipt is invalid when derivation happened earlier.

Observation eligibility is a separate adapter concern: a sensor may require visibility and range; an API may require an available authorized read path. CoDRA provides a concrete precedent for observers whose applicability depends on other context. An eligibility failure produces unavailable/unknown evidence, not a false world-state value or a fresh timestamp for the old value. This dependency is proposed for a later adapter; the current finite model does not implement sensor eligibility.

The reducer retains sufficient provenance to explain why a field is current, unknown, stale or conflicted. It compares sequences only within the same producer/scope stream. Duplicate identity with identical content is idempotent; duplicate identity with different content is rejected or explicitly conflicted. Disagreement across independent sources remains visible unless a declared precedence rule resolves it.

Proposed interfaces are conceptual rather than a wire protocol:

- `observe(request, scope) -> observation | unavailable`
- `reduce(state, observation) -> state_revision, changed_fields, invalidated_dependents`
- `refresh_plan(state, task, now, policy) -> observations_to_request, reasons`
- `project(state, task, required_fields, budget) -> context_receipt | readiness_failure`
- `revalidate(receipt, current_state, critical_fields) -> valid | invalid | unresolved`

A context receipt names its scope, base state revision, selected records and source/dependency pins, mandatory closure, budget accounting and omissions. It is an inspectable output of the projector, not an externally trusted security token. Real adapters need serialization/schema checks, authenticated producers and transaction semantics before an external system could rely on it.

## 4. Refresh policy

Use four independently tunable frequencies: acquisition, reduction, projection and model invocation. Updating a producer heartbeat need not call an LLM. Expiring a task-irrelevant record need not interrupt the user. A changed prerequisite of an imminent action needs prompt treatment.

| Class | Candidate trigger | Example |
| --- | --- | --- |
| Stable, revision-addressed material | Referenced revision changes or task requests another revision | Published specification or source blob |
| Volatile task state | Relevant event plus TTL backstop | Build status, active page or queue item |
| Derived conclusion | Any pinned prerequisite changes | Plan based on a previous repository head |
| Scope and authority evidence | Account/scope change, expiry, revocation and before effect | A simulated grant in tests; actual policy in a later adapter |
| Source health | Deadline/liveliness signal | Unavailable connector, without inferring entity absence |
| Unresolved effect | Authoritative reconciliation query | Timeout after a request whose outcome is unknown |

TTL is an accepted age policy, not a promise that the value stays true. The first implementation uses explicit deterministic rules. Adaptive priorities are a later experimental condition and must be frozen before comparison. If deadlines, observation budgets and task requirements conflict, return a visible degraded state rather than silently extending validity.

The planned fixed-versus-selective comparison shares the same task-conditioned projector, ranking, serializer, validity limits, guards and budgets. Only optional acquisition scheduling varies. Record the common implementation hash and separate policy configurations before execution; a simultaneous projector change prevents attributing the outcome to refresh alone.

Event streams can lose, reorder or duplicate messages. A cursor represents processed events, not complete knowledge of the world. Recovery after restart needs a declared snapshot/cursor protocol. A clock jump requires clock-domain-aware invalidation; comparing arbitrary wall-clock timestamps is insufficient.

## 5. Projection and effect use

The mandatory closure is computed from the current decision's declared dependencies. Optional information competes only for remaining capacity. The finite runner uses abstract integer costs. A model adapter must measure actual serialized input, tools, history, expected tool results, output allowance and margin against the reader's budget.

If the closure exceeds budget, return NOT_FIT with required cost and unresolved obligations. If required evidence is missing, stale, cross-scope or conflicted, return NOT_READY with specific reasons. Do not “solve” either outcome by deleting the controlling condition or converting uncertainty into a confident summary.

A delta view identifies its base revision. A receiver that lacks that base requests a snapshot. Context placement and semantic compression need downstream tests: inclusion is not correct interpretation. The proposed pilot therefore scores both the selected evidence and the resulting answer/action proposal.

Before an effect, actual runtime controls assess current authorization, critical revisions and the operation's external preconditions. The check/effect race remains unless the external service supplies an atomic condition, transaction or appropriate idempotency mechanism. A successful local comparison cannot substitute for that external mechanism.

## 6. Intentions and communication

A candidate intention contains a standing/current goal reference, trigger, task scope, prerequisites, expected result, cost ceiling and stop condition. Examples include preparing an authorized draft, refreshing a needed stale observation, or resuming work after an expected event.

The initial runtime integration should produce reviewable candidates and decision records before broader proactive behavior is evaluated. It can choose to wait or ask a targeted question. A remembered user preference is evidence of a preference; whether it authorizes a particular new external action is a separate determination.

Do not store hidden model reasoning as a prerequisite of this design. Concise decisions, evidence references and observable state transitions are sufficient for the proposed audit.

## 7. Integration with existing Knowledge Contract artifacts

| Existing artifact | Reused role | New work that remains |
| --- | --- | --- |
| Context Package | Declared purpose, reader, dependency closure, delivery budget and receipt | Temporal binding from state revisions to each delivered view |
| Status Model | Separate observations, dimensions and exchange profiles | Candidate situation profile, only after semantics are reviewed |
| Cache Validity | Identity, revision and invalidation conditions | Event/expiry adapters for situation-specific dependencies |
| Interaction and Memory | Conversation, durable memory and authorized state transitions | Startup/resume and action-outcome lifecycle |
| Current Authority / RM19 | Current scope and effect authority remain separate | Concrete runtime adapter and effect-time evidence |
| Agent Application / RM18 | Applied comparison and consumer evidence | Finite controls, then bounded pilot and independent review |

The existing RM18 prerequisites remain RM14, RM15 and RM17. The table identifies conceptual links without changing the prerequisite graph. Finite evidence does not establish RM18 acceptance or a live Muneral consumer.

## 8. Iteration outputs and acceptance questions

1. **Authored source draft:** paper, source matrix, ordered inventory and this design. Check whether every borrowed claim has a primary source and every proposed mechanism is labelled.
2. **Finite reference controls:** replay actual fixtures, preserve development defects and discriminating mutations, and bind the report to exact source hashes. Ask whether an always-refuse or stale-accepting implementation would fail.
3. **One offline adapter:** choose a repository-state sandbox with synthetic scope and deterministic event traces. Demonstrate cold start, replay, conflict, lost event and unknown outcome without external effects.
4. **Exploratory agent pilot:** freeze the policy, task manifest, model, budget and oracle before execution; compare against the strong typed baseline and publish all allocated outcomes.
5. **Separate review and confirmation:** resolve findings, use new held-out templates and appropriate non-author assessment, then decide whether a normative profile is justified.
6. **Site delivery:** publish reviewed source and clearly labelled summaries through existing build/review/readback mechanisms. A source PR or local check is not a production receipt.

Each iteration should improve an artifact or resolve an explicit research question. If adaptive maintenance adds complexity without measured benefit, retain the simpler deterministic design. Cost and performance remain unmeasured until the actual comparison is executed.
