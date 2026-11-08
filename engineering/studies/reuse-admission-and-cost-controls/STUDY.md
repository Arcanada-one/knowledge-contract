---
name: "reuse-admission-and-cost-controls"
title: "Reuse Economics: Controlled reuse: admission counterexamples and the cost of a cache hit"
short_title: "Reuse Economics"
subtitle: "Controlled reuse: admission counterexamples and the cost of a cache hit"
previous_title: "Controlled reuse: admission counterexamples and the cost of a cache hit"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Executable admission counterexamples and an analytical break-even calculation with explicit costs."
study_type: "analytical-engineering-study"
review_state: "internally-reviewed"
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="controlled-reuse-admission-counterexamples-and-the-cost-of-a-cache-hit"></a>

# Reuse Economics: Controlled reuse: admission counterexamples and the cost of a cache hit

## Abstract

Reusing a prepared knowledge artifact can avoid work, but a matching identifier or a high hit rate does not establish that reuse is appropriate or economical. This analytical study develops explicit admission conditions and counterexamples involving missing dependencies, changed search scope, current authority, time boundaries, and overlapping cost claims. A homogeneous cost model gives a conditional break-even identity. Public code supplies worked arithmetic examples and a finite synthetic checker with all nine named gates, including missing-gate counterexamples. It does not report measured model savings, production throughput, or a deployed authorization system. The contribution is an inspectable set of obligations and counterexamples, with explicit boundaries between analytical consequences and empirical claims requiring observations.

## Question and objects

The question is when a retained artifact can be used for a new request without losing its requirements, overstating its evidence, or hiding the cost of validation. The scientific models are developed in [Controlled knowledge reuse](../../../papers/controlled-knowledge-reuse/PAPER.md) and [Knowledge utility](../../../papers/knowledge-utility/PAPER.md). The [retained conditional-properties source](evidence/reuse-properties-source.json) records the original assumptions, arguments, and counterexamples behind this analysis.

A build can be represented as

\[
\operatorname{Compile}(b,q,S)\rightarrow(a,D,E,L),
\]

where \(b\) is a recipe, \(q\) the request, \(S\) the declared source snapshot, \(a\) the prepared revision, \(D\) its material dependencies, \(E\) evidence, and \(L\) coverage, loss, and stopping information. A later request \(q'\) requires a separate reuse decision under a current policy and context. Similarity may retrieve a candidate; it does not establish suitability.

Build dependencies explain how an artifact was obtained. Admission dependencies govern whether it can now be supplied or applied. A changed access decision can prohibit delivery without changing the artifact's text. A changed generator version need not require rebuilding every unaffected artifact. These decisions require explicit relevance rules rather than one undifferentiated freshness flag.

## Admission before optimization

The [status model](../../specifications/status-model/SPECIFICATION.md) distinguishes `pass`, `fail`, `unknown` and `not_applicable`. A mandatory obligation is discharged by `pass`, or by `not_applicable` together with an identified rule and evidence showing that exclusion is valid for the exact scope. Unsupported exclusion, missing observations and applicable unknowns do not discharge it. The nine gate classes used here are integrity, result class, task requirements, material dependency equivalence, current access, temporal policy, permitted transformations, modality delivery, and budget. The finite public checker deliberately makes all nine applicable; it therefore requires an explicit `pass` for every one and rejects `not_applicable` without a witness. It does not infer applicability from unrestricted text.

Partial content can be admissible when the request explicitly permits it and the gaps remain visible. That does not make the conditions attached to the selected content optional. High predicted utility also cannot turn a failed mandatory condition into permission. Economic optimization occurs within the set of admissible alternatives.

Reuse strategies include exact reuse, instantiation of a template, reuse after revalidation, rebuilding, bypassing the cache, and refusing reuse. These strategies are not a second operation-outcome vocabulary: the operation still reports `success`, `partial`, `refused`, `failed` or `unresolved` under its contract. A decision to revalidate is not itself permission to serve before the necessary check completes. An instantiated result has its own identity and must be checked after substitution.

## Counterexamples that determine the design

| Proposed shortcut | Counterexample | Required distinction |
| --- | --- | --- |
| Listed dependencies are unchanged, so the result is preserved | An omitted legend changes the meaning of an unchanged number or symbol | Dependency completeness is a substantive premise, not a manifest label |
| A negative answer has an empty dependency set | A new matching item is added after an exhaustive search returned none | Absence, count, and exact top-k depend on search-domain membership and policy |
| A previously accepted payload can be sent to another requester | The requester, tenant, resource scope, or permission has changed | Content identity and current delivery authority are separate |
| A live cache lifetime overrides an unavailable authority service | A permission was revoked while the authority result became unknown | Unknown current authority does not inherit an old success by default |
| A cached completion message completes another task | The message describes an earlier attempt and external effect | Retained content is not a new execution event |
| Frequent reads prove continuing validity | Repeated hits add no source assessment | Access statistics and validation time are separate |

The preservation claim is necessarily conditional. Suppose a sound prior assessment established properties \(P_1,\ldots,P_m\) of artifact \(a\) for request \(q\) in state \(s_0\). Their complete dependency and interpretation interface must remain equivalent in \(s_1\), and each property's request dependence must factor through declared components on which \(q\) and the new request \(q'\) agree. For every output \(a'\) allowed by the transformation relation \(T(a,a')\), the transformation must preserve those properties. These premises establish their retention, but admission for \(q'\) additionally requires that the retained properties entail discharge of every mandatory requirement of \(q'\), with valid inapplicability witnesses where used, and that current authorization and delivery obligations hold. An old verified property set cannot justify an uncovered new requirement. Omitting an actual dependency or assuming that the old assessment was sound invalidates a premise; a Boolean field called `complete_manifest` establishes neither premise. The [controlled-reuse theorem](../../../papers/controlled-knowledge-reuse/PAPER.md) states the corresponding conditional argument.

Suitability is also directional. A complete nonempty set may support an existential answer through an allowed projection. One known member does not establish the whole set, its count, or absence of other members. A symmetric similarity score cannot supply this missing implication.

## Time, concurrency, and state

Artifact lifecycle, residency, freshness, and current eligibility are different assessments. A valid retained revision may be cold or temporarily unavailable. A resident fresh artifact may be inaccessible to this requester. A historical answer can deliberately use a pinned old revision while still respecting current access restrictions.

A strict-current policy needs a declared point at which relevant source heads and authority are considered current. A bounded-stale policy needs an explicit allowed scope and age. Neither policy may silently ignore known withdrawal, corruption, incompatibility, or a material unresolved gap. A cache hit updates usage statistics; it does not reset the time when an underlying source was checked. [HTTP cache freshness](../../../reference/bibliography/BIBLIOGRAPHY.md#http-caching) and [stale-response extensions](../../../reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses) supply limited technical analogies, not permission to bypass knowledge or authority checks.

There is also a gap between checking and delivery. A permission or dependency can change after validation but before the result is supplied. An implementation must specify its consistency boundary, for example through a checked epoch, lease, or transactional publication protocol. Those mechanisms need their own concurrency tests. The analytical obligation here does not claim that a distributed service has already implemented them correctly.

## An exact cost model

Consider homogeneous requests with equal admissible quality and non-overlapping accounting categories over a fixed accounting horizon. Let \(N\) be the number of requests, \(G\) the cost of the cold admissible path, \(c_v\) additional candidate-search and admission cost per request, \(c_r\) the remaining cost of a usable reuse, and \(\rho\) the fraction of usable reuses. Let \(B\), \(MG\), \(I\), and \(S\) be preparation, additional background builds, invalidation, and storage costs. All costs use one declared unit and are nonnegative, with \(0\leq\rho\leq1\). The retained edition-1.0 examples used \(V,R,h\) for \(c_v,c_r,\rho\); their original data and code remain unchanged. Then

\[
C_0=NG,
\]

\[
C_1=B+Nc_v+N\rho c_r+N(1-\rho)G+MG+I+S.
\]

Writing \(F(N)=B+MG+I+S\) for overhead, which may depend on request count over the declared horizon, and \(d=\rho(G-c_r)-c_v\), subtraction gives

\[
C_0-C_1=Nd-F(N).
\]

Strict savings require \(Nd>F(N)\). The closed threshold \(\lfloor F/d\rfloor+1\) applies only when overhead \(F\), expected hit fraction \(\rho\), and unit costs are independent of \(N\) over that horizon, and \(d>0\). If \(d\leq0\), nonnegative overhead cannot be recovered through more requests in this homogeneous model. For actual observations, use the integer hit count \(H_N\): savings are \(H_N(G-c_r)-Nc_v-F(N)\). A fractional expected hit count is not an observed event count. If storage grows as \(S(N)=sN\), fixed other overhead \(F_0\) is recovered only when \(d>s\), with threshold \(\lfloor F_0/(d-s)\rfloor+1\); there is no such threshold when \(d\leq s\).

| Invented scenario | Parameters | Algebraic result |
| --- | --- | --- |
| High hit rate with expensive validation | \(N=100,\rho=0.9,G=10,c_r=1,c_v=9,F=0\) | Cold cost 1,000; reuse cost 1,090; loss 90 |
| Positive margin with preparation cost | \(N=100,\rho=0.9,G=10,c_r=1,c_v=1,F=100\) | Cold cost 1,000; reuse cost 390; savings 610 |
| Zero margin | \(N=100,\rho=0.5,G=10,c_r=2,c_v=4,F=100\) | The fixed loss of 100 remains |
| Storage increases with request count | Same positive-margin parameters, but \(F(N)=100+8N\) | At \(N=100\), reuse cost 1,190; loss 190; no profitable count under these constant rates |

These are exact arithmetic examples in invented cost units. They are not prices, measured token bills, or estimates of the project's performance. Heterogeneous requests require an appropriately stratified sum rather than substitution of incompatible averages.

## Utility and double counting

Compute savings alone are not net task value. Quality loss, additional review, delayed outcomes, and downstream harm require an explicit utility policy and evidence. If their values are unknown, assigning zero would create an unsupported benefit. If a route violates a hard constraint, a favorable monetary estimate does not admit it.

Costs also need a shared baseline. Suppose a cold operation costs ten units, provider caching reduces it to six, and using a prepared artifact reduces it to one. The two separately calculated savings, four and nine, cannot be added into thirteen units saved from a ten-unit operation. If the artifact hit eliminated the model call, a provider-cache saving on that nonexistent call is not another observed benefit. Resource events, retries, storage, and shared infrastructure need non-overlapping accounting or an explicit allocation rule.

No inference about causal contribution follows merely from counting citations, delivered artifacts, or completed tasks. The [editorial pilot](../editorial-skill-pilot/STUDY.md), for example, observed usable outputs under both conditions and a tie. That result cannot be turned into measured economic benefit without resource and outcome observations.

## Public examples and claim limits

The corrected [counterexample program](checks/check_admission_and_cost.py) names all nine mandatory gate classes. It checks a fully passing positive control and 27 separate missing, failed or unknown gate mutations, plus malformed inputs including a one-gate-only map and an unjustified `not_applicable`. The supplied states remain local inputs; this does not authenticate an authority service or establish real-world applicability. The exact rational cost calculations are worked examples of the identity, including linearly growing storage overhead, not empirical validation of economic assumptions. The small dependency and absence models illustrate counterexamples on invented inputs.

```bash
python3 checks/check_admission_and_cost.py
```

The [saved corrected result](checks/admission-and-cost-check.json) is a new deterministic demonstration. The earlier [edition-1.0 program](evidence/replay_reuse_counterexamples.py) and [result](evidence/public-reuse-counterexamples.json) remain byte-identical as historical evidence: that program tested only three supplied gates and erroneously accepted a nonempty subset when a required gate was omitted. Its six fail/unknown controls do not establish the missing-gate obligation. The corrected program supersedes that local gate demonstration without changing any historical model outcome. The [correction record](../review-corrections.json) identifies the new files separately.

The original property source is a Russian rendered-text view with separately recorded source and representation hashes in [origin.json](evidence/origin.json). The admission conditions, dependency counterexamples and temporal limits above are English summaries and the current argument; the strengthened new-request-coverage premise is an explicit correction, not a claim that the old source already proved it. The [evidence language index](../evidence-language-index.json) records individual file languages. None of the public programs reruns an earlier production system.

## Conclusion

Controlled reuse requires two decisions: whether a route satisfies its obligations, and whether it is preferable among admissible routes. The logical counterexamples identify inputs that cannot be omitted from the first decision. The cost identity specifies what must be measured for the second. The completed analytical result is useful precisely because it permits a negative answer: a cache can be correct but uneconomical, economical under invented assumptions but unmeasured in practice, or superficially efficient while inadmissible. Terminology is consolidated in the [glossary](../../../reference/glossary/GLOSSARY.md).
