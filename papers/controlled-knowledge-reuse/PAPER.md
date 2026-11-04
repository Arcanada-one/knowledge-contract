---
name: "controlled-knowledge-reuse"
title: "Knowledge Contracts and the Admission of Prepared Knowledge"
artifact: "scientific-paper"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "The conditions under which saved knowledge may support a new task, recipient or execution."
---

# Knowledge Contracts and the Admission of Prepared Knowledge

**Author:** Pavel Valentov · **Publication edition:** 1.0

## Abstract

Preparing knowledge in advance can reduce repeated work, but a previously acceptable artifact is not automatically acceptable for a new task. This paper defines a knowledge contract as an explicit account of requirements, constraints, grounds, permitted transformations, and verification obligations. It distinguishes that contract from its professional specializations and from a prepared artifact produced under it. Reuse is modeled as a directed admission relation, evaluated for a particular request and state. We prove a conditional preservation result requiring complete material dependencies, equivalent conditions, and a property-preserving transformation. Counterexamples cover changed permissions, incomplete dependencies, negative search results, and races between admission and delivery. The contribution is a precise boundary between reusable preparation and current authorization, including cases where rebuilding or rejection is required. The argument does not establish automatic discovery of every semantic dependency, industrial coordination guarantees, or a universal economic advantage from caching.

**Keywords:** knowledge contract; compilation; reuse admission; constraints; dependencies; current authorization.

## 1. Research question and relation to caching

A system may prepare a summary, context package, workflow, or professional instruction once and use it repeatedly. Repetition saves work only if the prepared result remains suitable. Identical request text can hide a changed recipient, policy, source revision, or time interpretation.

We ask: **when does an earlier verification justify a new use of a prepared artifact?** The problem resembles caching, but the cached object carries semantic and normative obligations as well as bytes. HTTP caching provides explicit rules for freshness and reuse [1], and extensions describe limited stale-serving behavior [2]. Those protocols are relevant comparisons; their guarantees do not automatically apply to knowledge interpretation or authorization.

The contribution is a contract model that makes the extra admission obligations explicit. It treats reuse as a decision under conditions rather than a consequence of similarity, popularity, or storage location.

## 2. Contracts and their professional specialization

A **knowledge contract** specifies a bounded use: its objective, requirements, mandatory constraints, admissible grounds, permitted transformations, expected result, and verification or stopping conditions. Its content can be represented in different formats. The scientific concept does not depend on one schema version or transport envelope.

Constraints are first-class obligations. They can limit scope, resources, time, recipient, authority, interpretation, or allowed operation. A preference can guide selection among admissible options. A mandatory constraint cannot be compensated by a high utility score. If a mandatory condition is unknown, the corresponding admission has not passed.

The contract does not itself establish truth, grant authority, or supply a missing capability. It states what must be supported and checked. A structurally valid contract can still contain a false premise or an unimplementable demand.

In a professional profile, a **role** specifies expected responsibilities; a **competency** specifies an ability under stated conditions, while a competency assessment binds supporting evidence to a particular executor; a **skill** is a reusable procedure with conditions, steps, and checks; and a **blueprint** organizes roles, procedures, and decision points for a class of work. These are the project's operational definitions, not a claim of one universal external taxonomy.

A **Work Item** instantiates an objective with actual requirements and outputs. A **capability** concerns an available operation. **Authorization** concerns permission to perform it in the current context. A role can be responsible for an outcome without possessing every capability or permission needed to produce it. A skill description does not establish that an executor meets a competency requirement, and a successful attempt does not establish that ability across every task in the described class.

## 3. Preparation and the reuse relation

Let \(q\) include the task, requirements, referents, recipient, isolation scope, resource budget, and time interpretation. Let \(S\) be a pinned source state and \(b\) a preparation recipe. A preparation attempt produces, when successful,

\[
\operatorname{Compile}(b,q,S)\to(a,D,E,L),
\]

where \(a\) is an artifact revision, \(D\) its declared dependencies, \(E\) its verification evidence, and \(L\) its coverage, losses, and unresolved conditions. Preparation can fail or produce an explicitly partial result. A content hash checks bytes under a declared serialization; it does not establish truth or deterministic regeneration.

For a new request \(q'\), policy \(p\), and current state \(s\), write

\[
a\rightsquigarrow_{p,s}q'
\]

when the artifact is admitted for that use. This relation is directed. A complete artifact may support an authorized narrower projection; a partial artifact does not support a broader task merely because the same topic is mentioned.

Possible decisions include reuse unchanged, instantiate with checking, revalidate, rebuild, bypass reuse, and reject the requested use. Revalidation is an outstanding obligation, not permission to deliver before the check. An instantiated result has its own content identity and actual-output checks.

Build dependencies and admission dependencies differ. A generator version can matter for provenance or a known defect; current permission can matter at every delivery. Neither invalidating everything after every tool update nor ignoring all interpretation changes is a justified general policy.

## 4. Conditional preservation theorem

Let \(P_1,\ldots,P_m\) be the properties previously verified for artifact \(a\) in state \(s_0\). Assume:

1. \(D\) contains every state input material to these properties and their interpretation.
2. The new state \(s_1\) agrees with \(s_0\) on the complete observations of \(D\) relevant to each property.
3. A permitted transformation \(T\), including the identity transformation, preserves each \(P_j\) in \(s_1\).
4. Independent current admission conditions, including authorization and delivery requirements, pass for the new use.

Then the transformed artifact retains the verified properties for the declared new use, and the stated admission conditions hold.

**Proof.** For each \(j\), completeness of \(D\) and equality of its relevant observations imply that changing from \(s_0\) to \(s_1\) does not change \(P_j(a,\cdot)\). Thus \(P_j(a,s_1)\) holds. Property preservation gives \(P_j(T(a),s_1)\). The remaining admission conditions hold by the fourth assumption. This establishes the finite selected set, not additional unverified properties. ∎

The theorem is deliberately conditional. A manifest labeled “complete” does not prove its completeness. Natural-language interpretation, hidden dependencies, and current authority need their own justification. The theorem also does not make a false premise true: preservation can maintain a faithful record of a mistaken source.

## 5. Dependencies and scope counterexamples

Dependencies can concern content fields, relations, alternative grounds, interpretation rules, normative bases, representations, and search scope. Fine granularity can avoid unnecessary rebuilding only when it preserves completeness for the selected properties.

Negative, exhaustive, counted, and ranked answers expose a common failure. Suppose an artifact states that no record satisfies a predicate. Recording only previously returned record identifiers is insufficient: a new matching record changes the answer without modifying any earlier result. The relevant dependency includes the searched scope, visibility, predicate, and any completeness assumptions. Exact top-ranked results additionally depend on ranking and tie rules. Approximate search does not become exhaustive because its output is cached.

Multimodal dependencies can concern an image revision, region, legend, or transformation. Correcting a symbol can invalidate an unchanged textual interpretation. Moving identical bytes may require a locator or delivery check without changing semantic content. These cases require different responses.

Alternative grounds also matter. Losing one source need not invalidate a conclusion if an independently sufficient permitted ground remains. A dependency traversal can identify affected artifacts, but deciding whether they remain supported requires the declared support rule and current assessments.

## 6. State, time, and delivery

Lifecycle, residency, freshness, and reuse eligibility are separate dimensions. An artifact can be ready and resident but unauthorized for a particular recipient. Eviction can change latency without changing its content. A recent cache hit is evidence of use, not of renewed validation.

Time policies must be explicit. **Strict current use** requires the relevant current conditions at a declared admission point. **Historical pinned use** preserves a past state for the requested purpose while still respecting present access and revocation conditions. **Bounded stale use** permits specified age or divergence only where the contract allows it. Known revocation, corruption, or incompatibility is not repaired by an unexpired time-to-live.

Checking immediately before delivery is insufficient for a strong current-state guarantee if a material condition can change between the check and the protected operation. For example, a permission can pass, then be withdrawn, then the artifact can be sent. Every individual step can be implemented as described while the desired current-admission claim fails.

A stronger guarantee requires a declared admission point and a coordination mechanism that binds the relevant evaluation to that point: a coherent snapshot, suitable lock, valid lease, or equivalent protocol under stated assumptions. The guarantee concerns that point and scope; it does not promise that the world will remain unchanged afterward.

Publication has a related race. A slow preparation attempt must not replace a newer artifact merely because it finishes later. Generation checks and protected publication can prevent that overwrite under their storage assumptions. Repeated or reordered invalidation events can be handled idempotently, but lost events require reconciliation or independent validation. Event deduplication alone does not recover missing information.

## 7. Economic and practical limits

Admission first determines which routes are permitted. Cost or predicted utility can then rank those routes. A cheap inadmissible result is not a valid optimization candidate. Reuse may reduce repeated preparation while adding storage, validation, invalidation, reconstruction, and coordination costs.

Comparisons should include a valid cold path and account for the same required quality and authority conditions. Provider-level caching, retrieval caching, prepared context, and professional artifacts are different units of reuse. Savings attributed to the same avoided operation must not be counted repeatedly across layers.

The present result is the conditional admission argument and its counterexamples. It establishes no universal speedup, cost reduction, or production concurrency guarantee. Those are workload- and implementation-specific claims that require their own measurements and failure models. Repeated successful reuse does not by itself raise the truth or completeness status of the underlying knowledge.

## 8. Connections to the published engineering work

The [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) examines finite admission decisions and accounting controls. The [contract profile conformance study](../../engineering/studies/contract-profile-conformance/STUDY.md) addresses supported representations. The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) addresses closure and actual delivery.

Machine interfaces and their compatibility versions belong in the [engineering core specification](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md). The shared [glossary](../../reference/glossary/GLOSSARY.md), [constrained transformations](../constrained-transformations/PAPER.md), and [knowledge utility](../knowledge-utility/PAPER.md) complete the conceptual links.

## References

1. Fielding, R., Nottingham, M., and Reschke, J. *HTTP Caching*. RFC 9111, 2022. <https://www.rfc-editor.org/rfc/rfc9111>
2. Nottingham, M. *HTTP Cache-Control Extensions for Stale Content*. RFC 5861, 2010. <https://www.rfc-editor.org/rfc/rfc5861>
