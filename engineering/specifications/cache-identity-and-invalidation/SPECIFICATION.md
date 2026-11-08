---
name: "cache-identity-and-invalidation"
title: "Cache Validity: Cache Identity, Dependency Tracking, and Invalidation"
short_title: "Cache Validity"
subtitle: "Cache Identity, Dependency Tracking, and Invalidation"
previous_title: "Cache Identity, Dependency Tracking, and Invalidation"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Content, build and lookup identity, dependency changes and guarded publication and serving."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="cache-identity-dependency-tracking-and-invalidation"></a>

# Cache Validity: Cache Identity, Dependency Tracking, and Invalidation

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

This specification governs how a saved result is identified, found as a candidate, invalidated after change and admitted at a serve boundary. Equal bytes, equal recipes, semantic suitability and current authorization are separate relations.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). The architecture is supported by conditional arguments and bounded models, not by a claim of a deployed distributed coherence protocol.

**CCH-R001.** Every implementation MUST state its consistency assumptions and failure behavior.

See [controlled reuse](../../../papers/controlled-knowledge-reuse/PAPER.md).

## 2. Identity layers

| Identity | What it fixes | What it does not establish |
| --- | --- | --- |
| Content identity | Exact bytes or canonical structured value in a named hash domain | Meaning, authorship, truth or permission |
| Build identity | Declared inputs, recipe, parameters and relevant environment | Actual execution or deterministic output |
| Lookup identity | A candidate class for a query, recipient and policy | Eligibility of every retrieved candidate |
| Current head | The selected revision within a namespace and generation | Timeless suitability for all consumers |

**CCH-R002.** A lookup MUST be followed by request/artifact descriptor comparison and the required admission checks.

Negation, quantifiers, recipient, purpose and scope are not dispensable variations of a similar query.

**CCH-R003.** A digest collision assumption and the selected byte or canonical-value domain MUST be stated when digest equality is used as identity evidence.

The implemented byte domains are registered in the [status exchange profile](../status-model/SPECIFICATION.md#8-bounded-exchange-profile); an unnamed canonicalization is unsupported.

A request descriptor fixes the fields below. The artifact descriptor records the corresponding values for which the saved artifact was prepared and assessed.

| Descriptor component | Comparison rule |
| --- | --- |
| Purpose and recipient identifiers | Exact identities; aliases need an independently established identity mapping |
| Requirements/criterion references | Exact immutable revisions and digests, or a separately checked entailment of every new mandatory requirement |
| Representation and required profile references | Exact profile/version support or an explicit checked adapter with loss account |
| Subject, scope, quantifier and protected operators | Exact structure under the named representation profile, or an explicit scoped preservation argument; similarity is insufficient |
| Constraint and authority references | Complete current mandatory set, with no ignored constraint-bearing profile; current grants are rechecked |
| Required output/delivery form and budget | Actual delivered form satisfies the requested profile and actual resource bounds |
| Temporal mode and dependency snapshot | Requested historical/current/bounded-stale policy plus complete current read-set checks |

**CCH-R004.** The descriptor comparison MUST return an itemized `pass`, `fail`, `unknown` or justified `not_applicable` for the relevant components.

Missing fields, unknown profile semantics or an unproved implication remain unknown.

**CCH-R005.** The algorithm MUST NOT equate two requests merely because their lookup key, text embedding or source bytes agree.

Descriptor equality is a preliminary gate, not a grant of current authority. This architecture does not serialize full descriptors; a complete descriptor wire mapping remains a profile-specific obligation.

## 3. Dependency tracking

**CCH-R006.** The read set MUST contain every declared dependency material to the claimed reuse guarantee, including source revisions, required selectors, profiles, rules, request requirements, compiler behavior and authorization state.

Dependency kind determines the impact rule. Relocation of identical bytes can preserve content identity while changing accessibility; a changed interpretation can invalidate applicability without changing a source file.

**CCH-R007.** Negative results and exhaustive claims MUST also track their universe or index generation and completeness assumptions.

New content can invalidate “no match” or “all matches” without modifying any previously selected object. Top-k retrieval does not supply that completeness premise.

**CCH-R008.** Unknown impact MUST produce re-evaluation or a conservative unresolved result under the policy.

**CCH-R009.** It MUST NOT be inferred harmless simply because the old key still matches.

## 4. Change events and ordering

A change event identifies the affected dependency, previous and new revisions or epochs, event identity, ordering namespace and impact class.

**CCH-R010.** Epochs are nonnegative integers and a relevant change MUST strictly advance the affected dependency epoch even when its content bytes are unchanged.

An authority revocation changes admissibility without necessarily changing content.

The implemented `KCDependencyChange/v1` record in the [exchange schema](../../../schemas/contract-observation.schema.json) supplies `event_id`, `namespace`, `sequence`, `dependency_id`, `old_epoch`, `new_epoch`, old/new revision references, kind, impact, observer and time.

**CCH-R011.** `new_epoch` MUST exceed `old_epoch`; `revoked` events MUST carry `impact: blocked`.

Null revision references denote absence of an addressable revision, not established content equality. Event kinds are `revision_changed`, `revoked`, `availability_changed` and `unknown_change`. Impact uses the [status model](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies).

**CCH-R012.** A receiver MUST deduplicate an identical event identifier only when the complete event bytes agree, detect conflicting reuse of that identifier, and treat a missing or reordered sequence in its declared ordering namespace as a reconciliation requirement.

The profile serializes these facts; it does not provide event transport or certify complete event delivery. No inference of harmlessness follows from a missed event.

**CCH-R013.** If event loss is possible, reconciliation MUST compare observed dependency state with authoritative state before renewing affected admission claims.

**CCH-R014.** A disconnected system MAY serve under an explicitly bounded policy, but MUST NOT claim immediate global revocation when its consistency protocol cannot establish it.

## 5. Guarded publication and serving

A **head namespace** identifies one ordered stream of current-head decisions. Its **generation** is a nonnegative counter that strictly increases on every head change, including rollback, and every revocation applying to that head.

**CCH-R015.** Generation values MUST NOT be reused after rollback, restart, restore or counter exhaustion.

**CCH-R016.** A runtime unable to recover the counter safely MUST establish a fresh namespace and invalidate old read sets.

The exchange subset bounds integers at 2^53−1; exhaustion fails closed rather than wrapping.

**CCH-R017.** A worker's read set MUST contain the namespace and generation, every material dependency's exact revision and epoch, and relevant authority/policy epochs.

Completeness of that dependency set is an explicit premise of the guarantee, not a fact inferred from a cache key.

**CCH-R018.** Publication MUST make one linearizable decision over the following predicate: the current namespace and head generation equal the worker's expected values; every declared material dependency still has the observed epoch/revision; current authority and policy permit this exact output/use; and all required build checks remain satisfied.

**CCH-R019.** The head update and increment of generation MUST occur atomically with that decision.

A separate dependency check followed by a compare-and-set on the head alone is insufficient: revocation can occur between them.

**CCH-R020.** Every relevant revocation MUST advance its authority/dependency epoch and the affected head generation within the declared decision boundary.

**CCH-R021.** A late worker MUST NOT restore an older head, undo a revocation or publish against an unchanged-looking dependency after an intervening change.

**CCH-R022.** A deployment lacking an atomic boundary over these conditions MUST fail closed or explicitly offer a weaker named consistency profile; it cannot claim this strict guarantee.

**CCH-R023.** The serve guard MUST validate the exact output, relevant current dependency epochs and current authority at the actual serve consistency point.

Build-time validation does not authorize a later unguarded serve. Locks, transactions or a justified validation-and-commit protocol are mechanisms only when their scope covers the whole predicate. Remote effects outside that boundary retain their own reconciliation semantics.

**CCH-R024.** A lease MUST define scope, expiry, revocation behavior, clock assumptions and partition behavior.

A strict revocation claim cannot treat an unobservable revocation as harmless unless its explicitly adopted authorization semantics permit the stated delay.

The [reference model and regression tests](../../../tools/test_contract_profile.py) serialize the namespace, generation, dependency-epoch and revocation part of this predicate under one in-memory lock. They do not evaluate output-specific grants, semantic validity or build checks. They exhibit a late publisher, a changed dependency under a current head token, revocation between read and publish, concurrent publishers, exhaustion of either a head or dependency counter, and rollback without generation reuse. They are finite local checks, not evidence of distributed deployment or durable crash recovery.

## 6. Storage, recovery and observability

Residency and eligibility are independent. Eviction can remove a valid copy; retention can preserve an invalid one.

**CCH-R025.** Recovery MUST verify content identity and rebuild the current eligibility decision rather than restoring a historical positive verdict as current fact.

**CCH-R026.** Logs SHOULD record lookup candidate, compared descriptors, dependency observations, admission decision, publication generation and actual serve result.

**CCH-R027.** Logging MUST respect the recipient's disclosure rights.

Required audit retention is a separate policy from cache residence time.

## 7. Acceptance cases

Required tests include: identical query text with a changed recipient; changed source under a matching lookup key; a new object invalidating a negative result; a lost invalidation event found by reconciliation; a late build attempting to overwrite a newer head; expiry exactly at a hard deadline; and revocation between preliminary check and serve.

**CCH-R028.** Each test MUST identify the simulated or real consistency boundary.

The [reuse study](../../studies/reuse-admission-and-cost-controls/STUDY.md) reports the available evidence and its deployment limits. [RFC 9111](../../../reference/bibliography/BIBLIOGRAPHY.md#http-caching) is a reference for HTTP cache semantics, not proof that the semantic or authority checks defined here have been implemented. Existing bounded profiles and retained results are identified in the [compatibility appendix](../../../appendices/source-map/APPENDIX.md#4-protocol-compatibility).
