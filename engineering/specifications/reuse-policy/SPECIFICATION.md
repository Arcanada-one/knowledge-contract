---
name: "reuse-policy"
title: "Reuse Policy: Time, Authorization, and Decision Outcomes"
artifact: "engineering-specification"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Temporal modes, conservative deadlines, authorization, decision outcomes and retention boundaries."
---

# Reuse Policy: Time, Authorization, and Decision Outcomes

**Author:** Pavel Valentov · **Publication edition:** 1.0

## 1. Purpose and conformance

A reuse policy determines whether a saved result may satisfy a new request, what must be rechecked, and which time and authority constraints apply. It operates on a specific artifact, recipient, purpose, requirements revision and observation time.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). A cache hit is only a candidate. The [compiled-artifact specification](../compiled-artifact-contract/SPECIFICATION.md) defines the saved result; [identity and invalidation](../cache-identity-and-invalidation/SPECIFICATION.md) defines its dependency and serve guards.

## 2. Admission before timing

Before deciding freshness, the policy MUST establish semantic compatibility with the request, required dependency availability, applicable constraints, current disclosure authorization and any action-specific grant. A fresh but inapplicable result is ineligible. A byte-identical object does not inherit the authority of another recipient.

A sufficient existing authorization is used within its scope; this specification does not require asking a user for the same permission at every pipeline step. It does require checking that the authorization still covers the actual action, subject and time.

## 3. Temporal modes

| Mode | Commitment | Continuing obligations |
| --- | --- | --- |
| Historical pinned | Describe the identified historical revision as historical | Current disclosure authorization and applicable hard restrictions |
| Current | Establish the relevant current source and policy state at the serve boundary | Dependency, scope and authority checks under the declared consistency model |
| Bounded staleness | Permit a named maximum age under an explicit policy | Hard restrictions, provenance, uncertainty and any mandatory revalidation |

Service availability MUST NOT silently choose a weaker temporal mode. Historical correctness does not authorize disclosure of a withdrawn or restricted record. A background refresh does not by itself make the old content eligible.

## 4. Time model and deadlines

The policy MUST distinguish source-event time, source-observation time, artifact-build time, check time, authorization interval and storage time. Updating a digest check does not make an old fact new. The relevant clock and uncertainty bounds belong to the observation.

For the bounded interval model, let a check occur within `[checked.lower, checked.upper]`, and let a request's current time lie within `[now.lower, now.upper]`. A TTL-based deadline is conservatively anchored at `checked.lower + ttl`. The effective hard deadline is the minimum of applicable finite hard deadlines. Reuse requires `now.upper < effective_hard_deadline`; equality closes the window. A soft deadline is reached when `now.upper >= soft_deadline`.

An explicitly absent time limit does not waive other gates. Unknown mandatory time is unresolved, not an infinite deadline. Invalid intervals and incompatible chronology MUST be rejected. A different distributed time model requires its own declared semantics rather than pretending these interval rules provide causal ordering.

## 5. Decision outcomes

| Decision | Required behavior |
| --- | --- |
| Exact reuse | Serve only after all required checks and the final serve guard succeed |
| Revalidate before reuse | Obtain the missing current observations; do not serve as admitted beforehand |
| Rebuild | Create a new artifact under the current inputs or rules |
| Instantiate | Produce and assess a new template instance with bound parameters |
| Refuse | Report a known blocking condition at the permitted disclosure level |
| Unresolved | Report which mandatory observation is missing or inconclusive |

If bounded stale serving while refreshing is allowed, the decision MUST explicitly record stale freshness, its permitted bound and the refresh duty. This differs from revalidate-before-reuse. A refresh failure does not renew the old result's deadlines. Known invalidity or hard revocation cannot be concealed by a stale fallback.

## 6. Cost, retention and measurement

Cost can influence an eligible choice, but cannot excuse a mandatory violation. A utility estimate MUST state its task, baseline, horizon, units and included costs. Build, retrieval, validation, maintenance and integration costs must not be counted twice. Planned savings are estimates until measured.

Retention is a storage policy, not an eligibility policy. Popularity can justify keeping bytes longer; it does not extend the validity of their grounds. Negative results require especially explicit corpus scope and invalidation conditions.

## 7. Acceptance and evidence

Required cases include a current request with unavailable source-head evidence; a historical request after disclosure revocation; unknown clock bounds; equality at hard expiry; stale serving explicitly allowed and explicitly forbidden; refresh failure; a template instance with changed authority; and a low-cost option that violates a mandatory constraint.

The [reuse-admission and cost study](../../studies/reuse-admission-and-cost-controls/STUDY.md) distinguishes formal checks from measured operational savings. The [utility paper](../../../papers/knowledge-utility/PAPER.md) states conditional cost results and the assumptions needed for causal comparison. [RFC 5861](../../../reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses) provides an HTTP analogy for stale handling; it is not an authorization policy for knowledge or actions.

## 8. Compatibility

No illustrative TTL is a universal default. A deployment MUST choose and justify its policy for the task and risk. Importing an older record preserves its original observations and adds unknown values where the new policy needs information not present in the source. A prior all-purpose validity flag cannot be losslessly decomposed into freshness, eligibility and authority without additional evidence.
