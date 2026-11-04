---
name: "reuse-admission-and-cost-controls"
title: "Controlled reuse: admission counterexamples and the cost of a cache hit"
artifact: "engineering-study"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Executable admission counterexamples and an analytical break-even calculation with explicit costs."
study_type: "analytical-engineering-study"
review_state: "internally-reviewed"
---

# Controlled reuse: admission counterexamples and the cost of a cache hit

## Abstract

Reusing a prepared knowledge artifact can avoid work, but a matching identifier or a high hit rate does not establish that reuse is appropriate or economical. This analytical study develops explicit admission conditions and counterexamples involving missing dependencies, changed search scope, current authority, time boundaries, and overlapping cost claims. A homogeneous cost model gives an exact break-even condition. Newly supplied public code reproduces the arithmetic and finite logical examples with invented inputs. It does not report measured model savings, production throughput, or a deployed authorization system. The completed contribution is an inspectable set of obligations and counterexamples that an implementation can test, together with a precise account of which empirical conclusions require further observations.

## Question and objects

The question is when a retained artifact can be used for a new request without losing its requirements, overstating its evidence, or hiding the cost of validation. The scientific models are developed in [Controlled knowledge reuse](../../../papers/controlled-knowledge-reuse/PAPER.md) and [Knowledge utility](../../../papers/knowledge-utility/PAPER.md). The [retained conditional-properties source](evidence/reuse-properties-source.json) records the original assumptions, arguments, and counterexamples behind this analysis.

A build can be represented as

\[
\operatorname{Compile}(b,q,S)\rightarrow(a,D,E,L),
\]

where \(b\) is a recipe, \(q\) the request, \(S\) the declared source snapshot, \(a\) the prepared revision, \(D\) its material dependencies, \(E\) evidence, and \(L\) coverage, loss, and stopping information. A later request \(q'\) requires a separate reuse decision under a current policy and context. Similarity may retrieve a candidate; it does not establish suitability.

Build dependencies explain how an artifact was obtained. Admission dependencies govern whether it can now be supplied or applied. A changed access decision can prohibit delivery without changing the artifact's text. A changed generator version need not require rebuilding every unaffected artifact. These decisions require explicit relevance rules rather than one undifferentiated freshness flag.

## Admission before optimization

Let each mandatory gate return `pass`, `fail`, or `unknown`. Full admission requires `pass` for every applicable gate. A missing mandatory gate is not an implicit pass. Relevant gates include integrity, result class, task requirements, material dependency equivalence, current access, temporal policy, permitted transformations, modality delivery, and budget.

Partial content can be admissible when the request explicitly permits it and the gaps remain visible. That does not make the conditions attached to the selected content optional. High predicted utility also cannot turn a failed mandatory condition into permission. Economic optimization occurs within the set of admissible alternatives.

Useful outcomes include exact reuse, instantiation of a template, reuse after revalidation, rebuilding, bypassing the cache, and rejection. A decision to revalidate is not itself permission to serve before the necessary check completes. An instantiated result has its own identity and must be checked after substitution.

## Counterexamples that determine the design

| Proposed shortcut | Counterexample | Required distinction |
| --- | --- | --- |
| Listed dependencies are unchanged, so the result is preserved | An omitted legend changes the meaning of an unchanged number or symbol | Dependency completeness is a substantive premise, not a manifest label |
| A negative answer has an empty dependency set | A new matching item is added after an exhaustive search returned none | Absence, count, and exact top-k depend on search-domain membership and policy |
| A previously accepted payload can be sent to another requester | The requester, tenant, resource scope, or permission has changed | Content identity and current delivery authority are separate |
| A live cache lifetime overrides an unavailable authority service | A permission was revoked while the authority result became unknown | Unknown current authority does not inherit an old success by default |
| A cached completion message completes another task | The message describes an earlier attempt and external effect | Retained content is not a new execution event |
| Frequent reads prove continuing validity | Repeated hits add no source assessment | Access statistics and validation time are separate |

The preservation claim is necessarily conditional. Suppose a finite property set \(P\) depends only on a complete declared dependency interface \(D\), relevant inputs and interpretation remain equivalent, and transformation \(T\) preserves those properties. Under these premises, \(P(a)\) implies \(P(T(a))\) in the new declared scope. Omitting an actual dependency invalidates the premise. Accepting a Boolean field called `complete_manifest` does not establish completeness for natural-language content.

Suitability is also directional. A complete nonempty set may support an existential answer through an allowed projection. One known member does not establish the whole set, its count, or absence of other members. A symmetric similarity score cannot supply this missing implication.

## Time, concurrency, and state

Artifact lifecycle, residency, freshness, and current eligibility are different assessments. A valid retained revision may be cold or temporarily unavailable. A resident fresh artifact may be inaccessible to this requester. A historical answer can deliberately use a pinned old revision while still respecting current access restrictions.

A strict-current policy needs a declared point at which relevant source heads and authority are considered current. A bounded-stale policy needs an explicit allowed scope and age. Neither policy may silently ignore known withdrawal, corruption, incompatibility, or a material unresolved gap. A cache hit updates usage statistics; it does not reset the time when an underlying source was checked.

There is also a gap between checking and delivery. A permission or dependency can change after validation but before the result is supplied. An implementation must specify its consistency boundary, for example through a checked epoch, lease, or transactional publication protocol. Those mechanisms need their own concurrency tests. The analytical obligation here does not claim that a distributed service has already implemented them correctly.

## An exact cost model

Consider homogeneous requests with equal admissible quality and non-overlapping accounting categories. Let \(N\) be the number of requests, \(G\) the cost of the cold admissible path, \(V\) additional candidate-search and admission cost per request, \(R\) the remaining cost of a usable reuse, and \(h\) the fraction of usable reuses. Let \(B\), \(MG\), \(I\), and \(S\) be preparation, additional background builds, invalidation, and storage costs. All are in one declared unit and nonnegative. Then

\[
C_0=NG,
\]

\[
C_1=B+NV+NhR+N(1-h)G+MG+I+S.
\]

Writing \(F=B+MG+I+S\) and \(d=h(G-R)-V\), subtraction gives

\[
C_0-C_1=Nd-F.
\]

Strict savings therefore require \(Nd>F\). For fixed expected \(h\) and \(d>0\), the first profitable integer request count is \(\lfloor F/d\rfloor+1\). If \(d\leq0\), nonnegative fixed costs cannot be recovered through more requests in this model. For actual observations, use the integer hit count \(H_N\): savings are \(H_N(G-R)-NV-F\). A fractional expected hit count is not an observed event count.

| Invented scenario | Parameters | Algebraic result |
| --- | --- | --- |
| High hit rate with expensive validation | \(N=100,h=0.9,G=10,R=1,V=9,F=0\) | Cold cost 1,000; reuse cost 1,090; loss 90 |
| Positive margin with preparation cost | \(N=100,h=0.9,G=10,R=1,V=1,F=100\) | Cold cost 1,000; reuse cost 390; savings 610 |
| Zero margin | \(N=100,h=0.5,G=10,R=2,V=4,F=100\) | The fixed loss of 100 remains |

These are exact arithmetic examples in invented cost units. They are not prices, measured token bills, or estimates of the project's performance. Heterogeneous requests require an appropriately stratified sum rather than substitution of incompatible averages.

## Utility and double counting

Compute savings alone are not net task value. Quality loss, additional review, delayed outcomes, and downstream harm require an explicit utility policy and evidence. If their values are unknown, assigning zero would create an unsupported benefit. If a route violates a hard constraint, a favorable monetary estimate does not admit it.

Costs also need a shared baseline. Suppose a cold operation costs ten units, provider caching reduces it to six, and using a prepared artifact reduces it to one. The two separately calculated savings, four and nine, cannot be added into thirteen units saved from a ten-unit operation. If the artifact hit eliminated the model call, a provider-cache saving on that nonexistent call is not another observed benefit. Resource events, retries, storage, and shared infrastructure need non-overlapping accounting or an explicit allocation rule.

No inference about causal contribution follows merely from counting citations, delivered artifacts, or completed tasks. The [editorial pilot](../editorial-skill-pilot/STUDY.md), for example, observed usable outputs under both conditions and a tie. That result cannot be turned into measured economic benefit without resource and outcome observations.

## Reproduction and claim limits

The public [counterexample program](evidence/replay_reuse_counterexamples.py) uses exact rational arithmetic and small invented dependency and admission models. It verifies the three cost identities, the strict expected break-even threshold, a high-hit-rate loss, an omitted-dependency counterexample, a changed-domain negative-answer counterexample, and rejection of six failed or unknown gate mutations alongside a positive control.

```bash
python3 evidence/replay_reuse_counterexamples.py
```

The [saved result](evidence/public-reuse-counterexamples.json) is a new deterministic demonstration for this edition. It does not rerun an earlier production system. The program's gate values are supplied inputs, not authenticated authorization. The original property source is a retained rendered-text view with separately recorded source and representation hashes in [origin.json](evidence/origin.json).

## Conclusion

Controlled reuse requires two decisions: whether a route satisfies its obligations, and whether it is preferable among admissible routes. The logical counterexamples identify inputs that cannot be omitted from the first decision. The cost identity specifies what must be measured for the second. The completed analytical result is useful precisely because it permits a negative answer: a cache can be correct but uneconomical, economical under invented assumptions but unmeasured in practice, or superficially efficient while inadmissible. Terminology is consolidated in the [glossary](../../../reference/glossary/GLOSSARY.md).
