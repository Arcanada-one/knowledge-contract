---
name: "reuse-policy"
title: "Reuse Policy: Time, Authorization, and Decision Outcomes"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Temporal modes, conservative deadlines, authorization, decision outcomes and retention boundaries."
---

# Reuse Policy: Time, Authorization, and Decision Outcomes

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

**RUS-R014.** A reuse policy determines whether a saved result may satisfy a new request, what MUST be rechecked, and which time and authority constraints apply.

It operates on a specific artifact, recipient, purpose, requirements revision and observation time.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). A cache hit is only a candidate. The [compiled-artifact specification](../compiled-artifact-contract/SPECIFICATION.md) defines the saved result; [identity and invalidation](../cache-identity-and-invalidation/SPECIFICATION.md) defines its dependency and serve guards.

## 2. Admission before timing

**RUS-R001.** Before deciding freshness, the policy MUST establish semantic compatibility with the request, required dependency availability, applicable constraints, current disclosure authorization and any action-specific grant.

A fresh but inapplicable result is ineligible. A byte-identical object does not inherit the authority of another recipient.

A sufficient existing authorization is used within its scope; this specification does not require asking a user for the same permission at every pipeline step. It does require checking that the authorization still covers the actual action, subject and time.

## 3. Temporal modes

| Mode | Commitment | Continuing obligations |
| --- | --- | --- |
| Historical pinned | Describe the identified historical revision as historical | Current disclosure authorization and applicable hard restrictions |
| Current | Establish the relevant current source and policy state at the serve boundary | Dependency, scope and authority checks under the declared consistency model |
| Bounded staleness | Permit a named maximum age under an explicit policy | Hard restrictions, provenance, uncertainty and any mandatory revalidation |

**RUS-R002.** Service availability MUST NOT silently choose a weaker temporal mode.

Historical correctness does not authorize disclosure of a withdrawn or restricted record. A background refresh does not by itself make the old content eligible.

## 4. Time model and deadlines

**RUS-R003.** The policy MUST distinguish source-event time, source-observation time, artifact-build time, check time, authorization interval and storage time.

Updating a digest check does not make an old fact new. The relevant clock and uncertainty bounds belong to the observation.

For the bounded interval model, a check lies within `[checked.lower, checked.upper]` and the request time within `[now.lower, now.upper]`. The check is the policy-relevant observation, not a storage touch or unrelated digest check.

**RUS-R004.** Times MUST use one declared clock and unit.

**RUS-R005.** Bounds and durations MUST be finite; intervals require lower ≤ upper, and TTL and permitted maximum age require nonnegative values.

A TTL yields a **soft** deadline `checked.lower + ttl` unless the policy explicitly classifies that TTL as hard.

**RUS-R006.** A policy MUST identify each deadline's class and basis.

The effective hard deadline is the minimum of every applicable finite hard deadline, including hard TTL, grant expiry and a mandatory maximum-age bound. Reuse requires `now.upper < effective_hard_deadline`; equality closes the window. An explicit absence of all hard limits is not an unknown limit and does not waive other gates.

A soft deadline is reached at `now.upper >= soft_deadline`. Reaching it changes freshness to stale and requires `revalidate` before serving unless the request explicitly permits bounded stale serving. Under bounded staleness the conservative age is `now.upper - checked.lower`, anchored to that same policy-relevant check. `serve_stale` requires age strictly below the declared maximum age, no hard expiry or revocation, all other gates discharged, and a recorded refresh duty.

**RUS-R007.** A failed refresh MUST NOT reset either deadline.

**RUS-R008.** Invalid intervals (lower > upper), a definitely future check (`checked.lower > now.upper`), negative durations, incompatible clocks or unknown mandatory bounds MUST yield `unresolved` without an admitted serve.

**RUS-R009.** Where order itself is mandatory, overlapping intervals that cannot establish `checked.upper <= now.lower` also remain unresolved; an implementation MUST NOT invent a chronology from point estimates.

These interval rules do not claim distributed causal ordering.

## 5. Decision outcomes

The following tokens are **reuse decisions**, distinct from operation outcomes in the [status model](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies).

| Decision | Required behavior |
| --- | --- |
| `exact_reuse` | Serve only after every required gate and final serve guard pass within the chosen temporal mode |
| `revalidate` | Obtain current observations; no admitted serve before they discharge the gates |
| `rebuild` | Produce a new artifact under the current inputs/rules and assess it separately |
| `instantiate` | Produce and assess a new template instance with bound parameters |
| `refuse` | Report a known blocking condition at the permitted disclosure level |
| `unresolved` | Report missing, invalid or inconclusive mandatory observations; do not serve as admitted |
| `serve_stale` | Serve only under explicit bounded-staleness authorization, recording stale freshness, bound, observation basis and refresh duty |

**RUS-R010.** A stale fallback MUST NOT conceal known semantic invalidity, a hard expiry or revocation.

`serve_stale` differs from `revalidate`: the former permits delivery under a stated weaker temporal promise, the latter does not. Choosing a rebuild or refresh plan does not establish successful completion of that plan.

## 6. Cost, retention and measurement

Cost can influence an eligible choice, but cannot excuse a mandatory violation.

**RUS-R011.** A utility estimate MUST state its task, baseline, horizon, units and included costs.

**RUS-R012.** Build, retrieval, validation, maintenance and integration costs MUST NOT be counted twice.

Planned savings are estimates until measured.

Retention is a storage policy, not an eligibility policy. Popularity can justify keeping bytes longer; it does not extend the validity of their grounds. Negative results require especially explicit corpus scope and invalidation conditions.

## 7. Acceptance and evidence

Required cases include a current request with unavailable source-head evidence; a historical request after disclosure revocation; unknown clock bounds; equality at hard expiry; a soft TTL versus a hard TTL; invalid and overlapping clock bounds; a bounded-age limit measured from the relevant check; stale serving explicitly allowed and explicitly forbidden; refresh failure; a template instance with changed authority; and a low-cost option that violates a mandatory constraint.

The [reuse-admission and cost study](../../studies/reuse-admission-and-cost-controls/STUDY.md) distinguishes formal checks from measured operational savings. The [utility paper](../../../papers/knowledge-utility/PAPER.md) states conditional cost results and the assumptions needed for causal comparison. [RFC 5861](../../../reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses) provides an HTTP analogy for stale handling; it is not an authorization policy for knowledge or actions.

## 8. Compatibility

No illustrative TTL is a universal default.

**RUS-R013.** A deployment MUST choose and justify its policy for the task and risk.

Importing an older record preserves its original observations and adds unknown values where the new policy needs information not present in the source. A prior all-purpose validity flag cannot be losslessly decomposed into freshness, eligibility and authority without additional evidence.
