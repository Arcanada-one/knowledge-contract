---
name: "cache-identity-and-invalidation"
title: "Cache Identity, Dependency Tracking, and Invalidation"
artifact: "engineering-specification"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Content, build and lookup identity, dependency changes and guarded publication and serving."
---

# Cache Identity, Dependency Tracking, and Invalidation

**Author:** Pavel Valentov · **Publication edition:** 1.0

## 1. Purpose and conformance

This specification governs how a saved result is identified, found as a candidate, invalidated after change and admitted at a serve boundary. Equal bytes, equal recipes, semantic suitability and current authorization are separate relations.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). The architecture is supported by conditional arguments and bounded models, not by a claim of a deployed distributed coherence protocol. Every implementation MUST state its consistency assumptions and failure behavior. See [controlled reuse](../../../papers/controlled-knowledge-reuse/PAPER.md).

## 2. Identity layers

| Identity | What it fixes | What it does not establish |
| --- | --- | --- |
| Content identity | Exact bytes or canonical structured value in a named hash domain | Meaning, authorship, truth or permission |
| Build identity | Declared inputs, recipe, parameters and relevant environment | Actual execution or deterministic output |
| Lookup identity | A candidate class for a query, recipient and policy | Eligibility of every retrieved candidate |
| Current head | The selected revision within a namespace and generation | Timeless suitability for all consumers |

A lookup MUST be followed by descriptor comparison and the required admission checks. Negation, quantifiers, recipient, purpose and scope are not dispensable variations of a similar query. A digest collision assumption and canonicalization procedure MUST be stated when digest equality is used as identity evidence.

## 3. Dependency tracking

The read set MUST contain every declared dependency material to the claimed reuse guarantee, including source revisions, required selectors, profiles, rules, request requirements, compiler behavior and authorization state. Dependency kind determines the impact rule. Relocation of identical bytes can preserve content identity while changing accessibility; a changed interpretation can invalidate applicability without changing a source file.

Negative results and exhaustive claims MUST also track their universe or index generation and completeness assumptions. New content can invalidate “no match” or “all matches” without modifying any previously selected object. Top-k retrieval does not supply that completeness premise.

Unknown impact MUST produce re-evaluation or a conservative unresolved result under the policy. It MUST NOT be inferred harmless simply because the old key still matches.

## 4. Change events and ordering

A change event identifies the affected dependency, previous and new revisions or epochs, event identity, relevant ordering scope and impact class. An implementation MUST state how it detects lost, duplicate and reordered events. Event delivery alone does not establish that all cached derivatives were reconsidered.

If event loss is possible, reconciliation MUST compare observed dependency state with authoritative state before renewing affected admission claims. A disconnected system MAY serve under an explicitly bounded policy, but it cannot promise immediate global revocation unless its protocol actually provides it.

## 5. Guarded publication and serving

A worker records the generation and dependency read set used for its build. Before updating a mutable head, it MUST verify that the publication guard still holds. A late worker cannot restore an older head after a newer revision or revocation.

The serve decision MUST bind the exact output to the relevant current dependencies and authorization at a declared consistency point. A check at build time followed by an unguarded later serve leaves a time-of-check/time-of-use gap. Locks, transactions, leases or validation-and-commit protocols can address this under different assumptions; merely naming one is not an implementation.

A lease MUST define its scope, expiry, revocation behavior, clock assumptions and partition behavior. An implementation claiming strict revocation cannot simultaneously treat an unobservable revocation as harmless during a lease unless its stated authorization semantics permit that delay.

## 6. Storage, recovery and observability

Residency and eligibility are independent. Eviction can remove a valid copy; retention can preserve an invalid one. Recovery MUST verify content identity and rebuild the current eligibility decision rather than restoring a historical positive verdict as current fact.

Logs SHOULD record lookup candidate, compared descriptors, dependency observations, admission decision, publication generation and actual serve result. Logging must respect the recipient's disclosure rights. Required audit retention is a separate policy from cache residence time.

## 7. Acceptance cases

Required tests include: identical query text with a changed recipient; changed source under a matching lookup key; a new object invalidating a negative result; a lost invalidation event found by reconciliation; a late build attempting to overwrite a newer head; expiry exactly at a hard deadline; and revocation between preliminary check and serve. Each test must identify the simulated or real consistency boundary.

The [reuse study](../../studies/reuse-admission-and-cost-controls/STUDY.md) reports the available evidence and its deployment limits. [RFC 9111](../../../reference/bibliography/BIBLIOGRAPHY.md#http-caching) is a reference for HTTP cache semantics, not proof that the semantic or authority checks defined here have been implemented. Existing bounded profiles and retained results are identified in the [compatibility appendix](../../../appendices/source-map/APPENDIX.md#protocol-compatibility).
