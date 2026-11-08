---
name: "retrieval-and-context-composition"
title: "Context Assembly: Retrieval, Coverage, and Context Composition under Resource Limits"
short_title: "Context Assembly"
subtitle: "Retrieval, Coverage, and Context Composition under Resource Limits"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Search coverage, finite context selection, dependency closure and the limits of greedy composition."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="retrieval-coverage-and-context-composition-under-resource-limits"></a>

# Context Assembly: Retrieval, Coverage, and Context Composition under Resource Limits

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

A relevant passage is not necessarily a sufficient context, and a complete dependency graph is not evidence that its conditions survived delivery. This paper asks what can be justified about a context assembled from a declared search result under resource limits. We separate search assurance, support for requirements, feasibility of the delivered representation, and verification of the resulting answer. A finite model represents alternative groups of jointly necessary grounds, mandatory dependency closure, transformations, and measured resource budgets. We make explicit that support in the selected closure must be preserved or re-established in the actual representation; a manifest alone does not discharge that obligation. Three conditional results describe a scoped optimum from complete finite enumeration, a set-cover special case, and the classical cardinality-greedy guarantee under submodularity. Counterexamples distinguish joint-ground complementarity, mandatory coverage, shared costs, and loss during rendering. The contribution is a bounded account of selection and delivery obligations, not a new general approximation algorithm. The method combines deductive arguments with separately identified synthetic verification examples. Neither these examples nor exact selection over a finite decision space establish semantic annotation correctness, exhaustive retrieval from an unexamined corpus, recipient understanding, or empirical superiority of a language model.

**Keywords:** retrieval; context composition; coverage; dependency closure; resource budget; submodularity.

## 1. The question between retrieval and answering

A retrieval system proposes material that may support an answer. The original retrieval-augmented generation formulation combines external retrieval with a generative model [1]. That architecture does not itself certify that every necessary condition reached the generator or survived its answer.

Our question is: **what can be certified about a bounded context assembled from a declared search result?** Four judgments are needed. Did the search procedure examine the required scope? Do the available grounds support the requirements? Does the actual delivered representation retain that support while meeting resource and admission conditions? Does the final answer preserve the required content?

These judgments are related but not interchangeable. Returning ten plausible passages does not prove that an eleventh exception does not exist. Fitting a token limit does not prove that the recipient notices a warning. A completed search does not make contradictory sources consistent. Similarly, computing a dependency closure does not show that a renderer transmitted every material condition.

The contribution is to separate those obligations within one finite composition model and to identify where a conclusion exceeds its premises. Set-cover difficulty and the submodular-greedy approximation bound are established results [2, 3], not new complexity or approximation theorems claimed here. Their role is to delimit what transfers to this problem and what does not.

The method is deductive: define the selection and delivery objects, state conditional results, and test omitted assumptions with constructed cases. A separately documented verification package exercises finite abstract instances. It is not a trial of a live retriever, a model-generated summary, or a deployed Knowledge Contract service. The engineering connections and unmeasured questions remain explicit in Section 7.

## 2. Query, scope, and coverage

A query record fixes an intent, referents, time interpretation, requirements, permitted source scope, and answer form. Its requirements are obligations to establish or communicate, rather than merely words to match. A request for one supporting example has different obligations from a request for all examples, a count, or a statement that none exists.

Let \(S\) be the declared source snapshot and \(C\) the returned candidate set. Search assurance concerns the procedure that produced \(C\). An exhaustive finite scan under a specified predicate can support completeness within \(S\); a top-ranked sample generally cannot. Changes to access visibility, scope membership, predicates, or ranking rules can change the answer even if previously returned records are unchanged.

Coverage is assessed relative to a pinned requirement set \(R\). For each requirement we distinguish supported, partial, unsupported, conflicted, and unknown. These are reporting categories with explicit criteria, not a universal many-valued logic. “Unsupported in this package” does not mean false, absent from the whole corpus, or impossible to establish.

Coverage should be recorded at three boundaries: the registered source base, the retrieved candidates, and the delivered package. A fourth check concerns the actual answer or action proposal. Keeping these reports distinct locates loss: missing from the base, missed by retrieval, omitted during composition, or ignored during generation.

**Table 1. Assessment boundaries and claims they do not establish alone.**

| Boundary | What is assessed | What that assessment does not establish alone |
| --- | --- | --- |
| Source and search scope | Which snapshot, visibility rules, predicate, and search procedure were examined | That an unexamined source or hidden record contains no relevant exception |
| Candidate support | Whether a valid group supports each pinned requirement | That all supporting conditions survive transformation and delivery |
| Delivered context | The actual representation, retained obligations, admission conditions, and measured cost | That the recipient understood or used those obligations |
| Answer or action proposal | Whether the actual result satisfies the stated task checks | General correctness on other tasks or authority to execute an action |

A status applies to its exact boundary and revision. Failure to find support at one boundary must not be relabeled as a proof of absence at another. Unknown validity remains an outstanding assessment, not a passing support group.

## 3. Composition with joint grounds and dependencies

Let \(V\) be a finite set of candidate object revisions. For a selected subset \(A\subseteq V\), let \(\operatorname{cl}(A)\) denote its mandatory dependency closure under a fixed, declared graph. A requirement \(r\) can have alternative supporting groups \(\mathcal G_r\). A group contains jointly necessary grounds, not merely individually relevant fragments.

The dependency graph ranges over a fixed finite universe containing the candidate revisions and the dependency revisions they may require. Closure includes the selected roots and follows every declared mandatory edge. A reference whose required revision is unavailable is a missing obligation, not a leaf that can silently be ignored. Closure completeness is relative to this declared graph; it does not prove that every material semantic dependency has been discovered.

Under fixed assessments, define support by

\[
\operatorname{Supports}(r,A)
\iff \exists G\in\mathcal G_r:\ G\subseteq\operatorname{cl}(A)
\ \land\ \operatorname{Valid}(G,r).
\]

The validity predicate includes the relevant interpretation and applicability checks. Listing a group does not prove that its members support the requirement. In empirical use, that judgment requires independently assessed evidence or a sound supported rule.

A composition decision \(z\) includes selected content, permitted transformations, ordering, modality, and delivery form. Its actual representation is \(\operatorname{Render}(z)\), with declared cost \(c\). Feasibility requires mandatory support, all other admission conditions, and

\[
c(\operatorname{Render}(z))\leq B.
\]

For feasibility, mandatory support must concern the **actual delivered representation**, not only the roots or their abstract closure. Write \(\operatorname{DeliveredSupports}(r,z)\) when a valid supporting group and its task-relevant mandatory conditions are retained in, or correctly transformed into, the representation produced by the decision. That assessment needs a justified preservation argument or checks on the actual output. It is not inferred from membership in a manifest. A separately permitted retrieval route may satisfy an obligation only if the consumer can actually use it within the declared access and resource limits.

A decision may therefore satisfy the closure-based support formula and still be infeasible: a summarizer can drop an exception, a renderer can truncate a condition, or a linked residual can be unavailable to the recipient. Conversely, an authorized transformation need not preserve every source byte when it demonstrably preserves the required observations. The final answer remains a separate assessment even after delivered support passes.

The budget may be a vector: tokens, bytes, recipient time, or another measured resource. In that case the budget inequality is interpreted componentwise, with each measured component compared to its corresponding bound. Different units should not be silently added. An unmeasured required component is unresolved. A scalar objective requires a declared conversion or priority rule.

Costs need not be additive over fragments. Two selected objects can share a dependency, so summing their separately closed sizes double-counts it. Conversely, a delivery format can introduce headings, repeated legends, or fixed overhead. The delivered representation, rather than the unformatted fragments, is the relevant accounting object.

Least graph closure is also relative to the chosen granularity. The [projection study](../../engineering/studies/executable-projections-and-revision/STUDY.md#counterexample-to-claim-level-minimality) found extra claims inside a shared qualification even when their dedicated nodes were absent from the selected closure. A least entity set therefore need not be claim-minimal or cheapest to deliver.

## 4. Exactness and special-case guarantees

### Proposition 1. Complete finite selection gives a scoped optimum

Let \(Z\) be a finite, explicitly declared decision space. Suppose feasibility and objective value are evaluated correctly for every member. If enumeration finishes and returns a feasible member with maximal objective, that member is optimal in \(Z\). If enumeration finishes with no feasible member, no feasible member exists in \(Z\).

**Proof.** Every possible decision in the declared space has been checked. A better feasible decision or any feasible decision in the second case would therefore have appeared in the enumeration, contradicting the stated result. ∎

This establishes neither completeness of \(Z\) relative to all possible summaries nor correctness of semantic annotations. The declared decisions must include the representation and transformation alternatives to which the optimum claim applies; enumerating only roots is insufficient when unexamined renderings can change feasibility or value. If execution stops early and a feasible candidate has been verified, that candidate is an incumbent. If none has been verified, there is no established incumbent. Early stopping alone establishes neither optimality nor infeasibility; an independent sound bound or certificate would be a separate justification.

### Proposition 2. A restricted composition problem contains set cover

Consider unit-cost, independent packages, no transformations or dependencies, and the requirement to cover every obligation using at most \(k\) packages. Given a set-cover instance with universe \(U\) and subsets \(F_1,\ldots,F_n\), create one requirement per element of \(U\) and one package per \(F_i\), supporting exactly those requirements. The construction is polynomial, and selected packages cover all requirements exactly when their corresponding subsets cover \(U\).

This reduction transfers the known combinatorial difficulty of set cover [2] to this special case. It does not imply that every practical query is difficult, that extraction itself is formally solved, or that a heuristic has a particular approximation ratio.

### Proposition 3. The cardinality-greedy bound requires submodularity

For this proposition the ground set is finite, each selected element consumes one cardinality unit, and greedy evaluates exact marginal gains. It takes the permitted number of steps unless every element has already been selected. In the latter case, monotonicity makes the full ground set optimal. A rule that stops after seeing zero marginal gains without establishing the proposition's premises is not covered.

Let \(f\) be a nonnegative, monotone, submodular set function with \(f(\varnothing)=0\). With at most \(k\geq1\) selected elements and no other constraints, greedy selection by greatest marginal gain achieves at least

\[
\left(1-\left(1-\frac1k\right)^k\right)\operatorname{OPT}
\geq (1-1/e)\operatorname{OPT}.
\]

**Argument.** Let \(O\) be an optimal set. At step \(i\), monotonicity gives \(\operatorname{OPT}=f(O)\leq f(A_i\cup O)\). Submodularity bounds the gain from \(A_i\) to \(A_i\cup O\) by the sum of at most \(k\) current single-element marginal gains. The best next gain is therefore at least \((\operatorname{OPT}-f(A_i))/k\). Each step reduces the remaining gap by a factor no greater than \(1-1/k\). Iterating from the empty set gives the bound. This is the classical result of Nemhauser, Wolsey, and Fisher [3], not a new theorem of the present model. ∎

The result does not cover arbitrary size-based greedy selection, nonadditive costs, or arbitrary mandatory closure. Those settings need their own justified algorithms and assumptions. An approximation to an optional-value objective is not permission to miss a mandatory requirement. Before applying the bound to a derived objective, prove its stated properties on the actual ground set and show that its feasible family is the one in the proposition.

## 5. Counterexamples to convenient assumptions

Joint grounds need not be submodular. Suppose a requirement needs both a rule \(a\) and a condition \(b\). Let \(f(\varnothing)=f(\{a\})=f(\{b\})=0\), but \(f(\{a,b\})=1\). Adding \(b\) to the empty set yields no gain; adding it after \(a\) yields one. This violates diminishing returns. Individual ranking can therefore discard both members of the only useful pair.

Feasible root selections need not be downward-closed because coverage is mandatory. Consider one requirement whose only supporting group is \(\{a\}\), no dependencies, and a budget large enough for \(a\). The selection \(A=\{a\}\) is feasible, but its subset \(\varnothing\) does not cover the requirement. This counterexample uses the same closure-based support definition as §3.

Selected roots and delivered objects must not be confused. Removing a required condition from a root set can leave its closure unchanged because another selected root still requires it. Removing that condition from the actual delivered set is different: the resulting delivery may fail the closure obligation. A method justified for downward-closed feasible selections cannot be imported without checking which of these objects its guarantee concerns.

Budget pressure does not remove these obligations. If two mandatory grounds and an exception cost seven units in total and the budget is five, deleting the exception produces a smaller but inadmissible package. A feasible reformulation might exist, but it must be constructed and checked. Failure of one heuristic to find it is not proof of impossibility.

Shared dependencies illustrate a separate accounting issue. In a constructed instance, two roots each cost one unit and both require a condition costing three units. The sum of their separately closed costs is eight, but their union costs five when the shared condition is transmitted once and there is no other overhead. A format that repeats that condition has a different cost. This example refutes modular root-cost accounting for the union representation; it does not by itself refute submodularity of an objective. Joint grounds, shared costs, and mandatory feasibility are distinct reasons to check an algorithm's hypotheses.

The delivery boundary has its own counterexample. A root and its required exception may both belong to the computed closure, while the renderer transmits only the root. A closure-only checker can pass the selection even though the delivered context fails the requirement. The correct repair is to check retained support or construct a valid transformed representation, not to relabel the smaller delivery as complete.

Finally, declared coverage can be invalidated by new information. Support is monotone only under explicitly fixed grounds, applicability judgments, and conflict rules. An added contradictory source or a changed requirement can require reassessment even when old passages remain available.

## 6. Stopping and measurement

A useful result reports its scope and stopping reason. Distinct outcomes include a verified complete package, an explicitly partial package, a need for clarification, insufficient resources, an exhausted search limit, and stale or conflicting evidence. Stopping after a limit does not establish absence. A useful partial answer is possible when the answer form permits it and its uncovered obligations remain visible.

A complete-package claim should identify the selected supporting group for each mandatory requirement, the exact input and output revisions, the relevant preservation or output checks, and the resource measurements. A hash identifies bytes; it does not establish semantic validity. A solver that explored only part of its declared decision space reports that limit rather than treating an empty result as an infeasibility certificate.

Evaluation should compare methods under the same requirement snapshot, source scope, delivery constraints, and outcome rubric. Relevant baselines include ranked selection with dependency repair, selection of complete supporting groups, and exact enumeration on small instances. Removing dependencies or truncating delivery supplies ablations, not necessarily competitive baselines.

Measures should distinguish retrieval misses, invalid support groups, omitted dependencies, budget violations, and final-answer failures. Report denominators and uncertainty, including the number of cases that could not be adjudicated. Counting selected fragments or citing a larger source list does not measure sufficiency.

The mathematical results here hold for the declared finite model. They establish neither universal end-to-end answer correctness nor measured superiority on people, models, or production workloads. Recipient understanding and attention require separate observation, even when representation cost is measured exactly.

## 7. Connections to the published engineering work

The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) supplies exhaustive fixed-graph closure checks for all-required dependencies, plus historical layout and preliminary delivery checks. Its root-subset enumeration is not a budgeted composition optimizer. Those historical studies do not evaluate alternative supporting groups or resource-constrained selection. The [finite verification note](../../reviews/retrieval-context/REVIEW.md) accompanying this revision adds newly authored abstract cases and a reproducible checker for explicit selection and delivery boundaries. It is not a historical replay, a semantic extraction evaluation, or a production selection study. It supplies no measured comparison of language models or end-to-end retrieval methods. The [projection study](../../engineering/studies/executable-projections-and-revision/STUDY.md) supplies the distinct counterexample to claim-level minimality. The [contract profile conformance study](../../engineering/studies/contract-profile-conformance/STUDY.md) concerns structural validation, which must remain distinct from semantic sufficiency.

The [glossary](../../reference/glossary/GLOSSARY.md) gives common terminology. [Evidence and falsification](../evidence-and-falsification/PAPER.md) specifies evaluation obligations; [knowledge utility](../knowledge-utility/PAPER.md) explains why a composition objective must state its baseline, horizon, and resource accounting.

## 8. Conclusion

A retrieval result, an abstractly supported selection, a feasible delivered context, and a satisfactory final answer are different objects of assessment. Their checks must remain tied to the declared requirements, source snapshot, interpretation, representation, and recipient. In particular, a computed dependency closure cannot certify a delivery that loses a material condition.

Complete enumeration provides an optimum only within a finite declared decision space and only with correct feasibility and value assessments. The set-cover reduction explains a restricted source of combinatorial difficulty. The classical greedy bound applies under its cardinality and submodularity assumptions, not to every budgeted selection procedure. Joint grounds, mandatory coverage, and actual representation costs must be examined separately.

The practical result is a set of explicit proof and measurement obligations: justify support, verify its preservation into delivery, account for resources in their stated units, and report what a stopping condition leaves unresolved. The finite examples help detect particular mistakes in those obligations. They do not replace semantic assessment, independent review, or measurement of actual agent outcomes.

## References

1. Lewis, P., et al. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *Advances in Neural Information Processing Systems* 33, 2020. <https://arxiv.org/abs/2005.11401>
2. Karp, R. M. “Reducibility Among Combinatorial Problems.” In *Complexity of Computer Computations*, 1972, 85–103. <https://doi.org/10.1007/978-1-4684-2001-2_9>
3. Nemhauser, G. L., Wolsey, L. A., and Fisher, M. L. “An Analysis of Approximations for Maximizing Submodular Set Functions—I.” *Mathematical Programming* 14, 1978, 265–294. <https://doi.org/10.1007/BF01588971>
