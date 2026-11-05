---
name: "controlled-knowledge-reuse"
title: "Knowledge Contracts and the Admission of Prepared Knowledge"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "The conditions under which saved knowledge may support a new task, recipient or execution."
---

# Knowledge Contracts and the Admission of Prepared Knowledge

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

Preparing knowledge in advance can reduce repeated work. Whether a prepared artifact can be used again depends on the new task, its requirements, and the current conditions of use. This paper defines a knowledge contract as an explicit account of requirements, constraints, grounds, permitted transformations, and verification obligations. It separates the contract from its professional specializations and from the artifact prepared under it. We model reuse as a directed admission relation for a particular request and state. The conditional preservation theorem identifies sufficient conditions for a new use: sound prior verification, complete material dependencies, agreement on relevant request components, coverage of the new requirements, preservation by every permitted transformation output, and discharge of current-use conditions. Counterexamples address changed requests and permissions, incomplete dependencies, negative search results, and races between admission and delivery. The model distinguishes reusable preparation from current authorization, including cases that require rebuilding or rejection. It does not establish automatic discovery of every semantic dependency, industrial coordination guarantees, or a universal economic advantage from caching.

**Keywords:** knowledge contract; compilation; reuse admission; constraints; dependencies; current authorization.

## 1. Research question and relation to caching

A summary, context package, workflow, or professional instruction may be prepared once and used repeatedly. Repetition saves work only while the prepared result remains suitable. Even identical request text can refer to a changed recipient, policy, source revision, or time interpretation.

We ask: **when does an earlier verification justify a new use of a prepared artifact?** The problem resembles caching, with additional obligations: cached knowledge must meet the semantic and normative requirements of its new use.

HTTP caching provides explicit rules for freshness and reuse [1], and extensions describe limited stale-serving behavior [2]. These protocols offer useful comparisons, but their guarantees do not automatically cover knowledge interpretation or authorization.

The contract model makes those additional admission obligations explicit. Similarity, popularity, and storage location do not by themselves decide reuse. Incremental build correctness already requires consistency between a result and its complete task dependencies [3]. The theorem below follows the same dependency discipline and adds separate requirements for coverage of a new knowledge request and current authority. A successful build alone establishes neither.

## 2. Contracts and their professional specialization

A **knowledge contract** specifies a bounded use: its objective, requirements, mandatory constraints, admissible grounds, permitted transformations, expected result, and verification or stopping conditions. Its content can be represented in different formats. The scientific concept does not depend on one schema version or transport envelope.

Constraints are first-class obligations. They may restrict scope, resources, time, recipient, authority, interpretation, or the allowed operation. A preference may guide selection among admissible options. A high utility score cannot compensate for failure to satisfy a mandatory constraint. If a mandatory condition is unknown, the corresponding admission has not passed.

The contract does not itself establish truth, grant authority, or supply a missing capability. It states what must be supported and checked. A structurally valid contract can still contain a false premise or an unimplementable demand.

In a professional profile, the following terms have distinct functions:

| Term | Function |
| --- | --- |
| **role** | Specifies expected responsibilities. |
| **competency** | Specifies an ability under stated conditions. |
| Competency assessment | Binds supporting evidence to a particular executor. |
| **skill** | Is a reusable procedure with conditions, steps, and checks. |
| **blueprint** | Organizes roles, procedures, and decision points for a class of work. |

These are the project's operational definitions, not a claim of one universal external taxonomy.

A **Work Item** instantiates an objective with actual requirements and outputs. A **capability** concerns an available operation. **Authorization** concerns permission to perform it in the current context.

A role can be responsible for an outcome without possessing every capability or permission needed to produce it. A skill description does not establish that an executor meets a competency requirement. Likewise, a successful attempt does not establish that ability across every task in the described class.

## 3. Preparation and the reuse relation

Let \(q\) include the task, requirements, referents, recipient, isolation scope, resource budget, and time interpretation. Let \(S\) be a pinned source state and \(b\) a preparation recipe. A preparation attempt produces, when successful,

\[
\operatorname{Compile}(b,q,S)\to(a,D,E,L),
\]

where \(a\) is an artifact revision, \(D\) its declared dependencies, \(E\) its verification evidence, and \(L\) its coverage, losses, and unresolved conditions.

Preparation can fail or produce an explicitly partial result. A content hash checks bytes under a declared serialization; it does not establish truth or deterministic regeneration.

For a new request \(q'\), policy \(p\), and current state \(s\), write

\[
a\rightsquigarrow_{p,s}q'
\]

when the artifact is admitted for that use. The relation is directed: a complete artifact may support an authorized narrower projection, while a partial artifact does not support a broader task solely because both concern the same topic.

The admission decision may be to reuse unchanged, instantiate with checking, revalidate, rebuild, bypass reuse, or reject the requested use. A decision to revalidate leaves a check outstanding; it does not permit delivery before that check. An instantiated result has its own content identity and requires checks on the actual output.

Build and admission have different dependencies. A generator version can matter for provenance or a known defect, while current permission can matter at every delivery. Neither invalidating everything after every tool update nor ignoring all interpretation changes is a justified general policy.

## 4. Conditional preservation theorem

Fix an admission policy \(p\). Let \(P_1(x,q,s),\ldots,P_m(x,q,s)\) be properties of an artifact revision \(x\), request \(q\), and state \(s\), interpreted under fixed semantics. For each property, let \(\delta_j(s)\) be its relevant state observation and \(\kappa_j(q)\) its relevant request observation. Let the complete mandatory requirements of the new request be partitioned as

\[
R(q')=R_{\mathrm{artifact}}(q')\cup R_{\mathrm{use}}(q').
\]

The first group concerns the artifact properties justified by preparation; the second contains independent conditions to be discharged at current use, including authorization and delivery. Requirement discharge has the [applicability paper's meaning](../semantic-objects-and-context/PAPER.md#3-context-and-applicability): a passing assessment or a justified exemption for the exact subject and scope, never an unsupported or unknown condition. Assume:

1. **Sound prior verification.** \(P_j(a,q,s_0)\) actually holds for every \(j\). The presence of a positive receipt is not itself this premise.
2. **Complete and unchanged observations.** The manifest \(D\) contains every state input material to the selected properties and their interpretation. For every relevant \(x,q,s\), each property factors as \(P_j(x,q,s)=\widehat P_j(x,\kappa_j(q),\delta_j(s))\) for a fixed predicate \(\widehat P_j\). Moreover \(\delta_j(s_0)=\delta_j(s_1)\) and \(\kappa_j(q)=\kappa_j(q')\). This expresses completeness for request components as well as state components.
3. **Preservation for every permitted transformation output.** The permitted transformation is a relation \(T\), possibly the identity. For every \(a'\) with \(T(a,a')\), and every \(j\), \(P_j(a,q',s_1)\Rightarrow P_j(a',q',s_1)\).
4. **Coverage of the new artifact requirements.** Under the fixed assessment semantics, the selected properties suffice to discharge every requirement in \(R_{\mathrm{artifact}}(q')\). Explicitly, for every relevant output \(x\),

   \[
   \bigwedge_{j=1}^{m} P_j(x,q',s_1)
   \Rightarrow
   \bigwedge_{r\in R_{\mathrm{artifact}}(q')}
   \operatorname{Discharged}_r(x,q',s_1).
   \]

5. **Current independent admission.** For every proposed output \(a'\) with \(T(a,a')\), every requirement in \(R_{\mathrm{use}}(q')\) is discharged for that output at the declared current admission point. A check for another recipient, representation, or generation does not satisfy this premise.

Then every such output \(a'\) retains all selected properties for \((q',s_1)\), and all requirements in \(R(q')\) are discharged. It is therefore admitted under the specified policy and scope.

**Proof.** By assumptions 1–2, for each \(j\),

\[
P_j(a,q,s_0)
=\widehat P_j(a,\kappa_j(q),\delta_j(s_0))
=\widehat P_j(a,\kappa_j(q'),\delta_j(s_1))
=P_j(a,q',s_1).
\]

Thus \(P_j(a,q',s_1)\) holds. Assumption 3 transfers it to every permitted transformation output \(a'\). Assumption 4 discharges the new artifact requirements, and assumption 5 discharges the independent current-use requirements. Their union is the complete declared requirement set, so no mandatory requirement remains outside the argument. ∎

Two counterexamples explain why unchanged state alone is insufficient. An artifact can establish Boolean condition \(A\) while a new request also requires \(B\), which is false; preserving \(A\) does not cover \(B\). Separately, the property “the artifact's referent equals the requested referent” can hold for \(q\) and fail for \(q'\) without any source-state change. The first case violates requirement coverage; the second violates request-observation agreement.

The theorem is deliberately conditional. A manifest labeled “complete” does not prove its completeness, a checker can be unsound, and an unjustified coverage implication cannot authorize a new task. The result quantifies over successful permitted outputs; it does not promise that \(T\) has any output or terminates. Natural-language interpretation, hidden dependencies, and current authority need their own justification. Preservation also cannot make a false premise true: it can maintain a faithful record of a mistaken source. For a genuinely narrower requirement set with unchanged interpretations and assessments, [mandatory strengthening](../semantic-objects-and-context/PAPER.md#proposition-3-mandatory-strengthening-narrows-certified-applicability) supplies the corresponding subset implication; a change of request is not automatically such a narrowing.

## 5. Dependencies and scope counterexamples

A dependency can concern a content field, relation, alternative ground, interpretation rule, normative basis, representation, or search scope. Recording dependencies at finer granularity can avoid unnecessary rebuilding, but only if the manifest remains complete for the selected properties.

Negative, exhaustive, counted, and ranked answers expose a common dependency error. Suppose a saved artifact states that no record satisfies a predicate. If its manifest records only previously returned identifiers, a new matching record can change the answer without changing any earlier result.

The dependency therefore includes the searched scope, visibility, predicate, and completeness assumptions. Exact top-ranked results also depend on ranking and tie rules. Caching the output of an approximate search does not make that search exhaustive.

Multimodal dependencies can include an image revision, region, legend, or transformation. A corrected symbol can invalidate a textual interpretation even when the text itself is unchanged. Moving identical bytes, however, may require a locator or delivery check without changing semantic content. The required response depends on which property changed.

Losing one source need not invalidate a conclusion if an independently sufficient permitted ground remains. A traversal of dependencies can identify the affected artifacts. Deciding whether they remain supported requires the declared support rule and current assessments.

## 6. State, time, and delivery

Lifecycle, residency, freshness, and reuse eligibility answer different questions. An artifact may be ready and resident yet unauthorized for a particular recipient. Eviction can change latency without changing its content. A recent cache hit records use, not renewed validation.

Time policies must be explicit:

| Policy | Conditions |
| --- | --- |
| **Strict current use** | Requires the relevant current conditions at a declared admission point. |
| **Historical pinned use** | Preserves a past state for the requested purpose while still respecting present access and revocation conditions. |
| **Bounded stale use** | Permits specified age or divergence only where the contract allows it. |

Known revocation, corruption, or incompatibility is not repaired by an unexpired time-to-live.

A check immediately before delivery does not establish a strong current-state guarantee if a material condition can change before the protected operation. A permission check may pass, the permission may then be withdrawn, and the artifact may still be sent. Each step can behave as specified while the intended current-admission claim fails.

A stronger guarantee requires a declared admission point and a mechanism that binds the relevant evaluation to that point. A coherent snapshot, suitable lock, valid lease, or equivalent protocol can provide this coordination under stated assumptions. The guarantee applies to that point and scope. It does not promise that the world remains unchanged afterward.

Publication has a related race: a slow preparation attempt must not replace a newer artifact merely because it finishes later. Generation checks and protected publication can prevent this overwrite under their storage assumptions.

Repeated or reordered invalidation events can be handled idempotently. Lost events require reconciliation or independent validation; event deduplication alone does not recover missing information.

## 7. Economic and practical limits

Admission determines which routes are permitted. Cost or predicted utility can then rank those routes. A cheap but inadmissible result is not a valid optimization candidate. Reuse may reduce repeated preparation while adding costs for storage, validation, invalidation, reconstruction, and coordination.

Comparisons should include a valid cold path, with all compared routes held to the same required quality and authority conditions. Provider-level caching, retrieval caching, prepared context, and professional artifacts reuse different units. Savings from the same avoided operation must not be counted more than once across these layers.

The result established here is a conditional admission argument with counterexamples. It establishes no universal speedup, cost reduction, or production concurrency guarantee. Those workload- and implementation-specific claims require their own measurements and failure models. Repeated successful reuse does not by itself raise the truth or completeness status of the underlying knowledge.

## 8. Connections to the published engineering work

The [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) examines finite admission decisions and accounting controls. The [contract profile conformance study](../../engineering/studies/contract-profile-conformance/STUDY.md) addresses supported representations. The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) addresses closure and actual delivery.

Machine interfaces and their compatibility versions belong in the [engineering core specification](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md). The shared [glossary](../../reference/glossary/GLOSSARY.md), [constrained transformations](../constrained-transformations/PAPER.md), and [knowledge utility](../knowledge-utility/PAPER.md) complete the conceptual links.

## References

1. Fielding, R., Nottingham, M., and Reschke, J. *HTTP Caching*. RFC 9111, 2022. <https://www.rfc-editor.org/rfc/rfc9111>
2. Nottingham, M. *HTTP Cache-Control Extensions for Stale Content*. RFC 5861, 2010. <https://www.rfc-editor.org/rfc/rfc5861>
3. Mokhov, A., Mitchell, N., and Peyton Jones, S. “Build Systems à la Carte.” *Proceedings of the ACM on Programming Languages* 2(ICFP), article 79, 2018, 1–29. [Author's copy](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf). <https://doi.org/10.1145/3236774>
