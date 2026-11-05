---
name: "retrieval-and-context-composition"
title: "Retrieval, Coverage, and Context Composition under Resource Limits"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Search coverage, finite context selection, dependency closure and the limits of greedy composition."
---

# Retrieval, Coverage, and Context Composition under Resource Limits

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

Retrieving relevant fragments and assembling a sufficient context are different problems. A retrieved fragment can be pertinent while omitting a mandatory exception; a package can cover declared requirements without demonstrating that the search was exhaustive. This paper gives a finite model of requirements, alternative supporting groups, mandatory dependencies, representations, and resource limits. We distinguish search assurance, requirement coverage, composition feasibility, and actual output verification. Conditional results characterize exact finite selection, a set-cover special case, and the limited applicability of a classical submodular-greedy guarantee. Counterexamples show why jointly necessary grounds and shared dependencies defeat common additive assumptions. The contribution is a precise contract for what a retrieval-and-composition result establishes, including meaningful stopping outcomes. Domain evaluations and executable selectors are separate engineering objects; the present argument establishes no general empirical advantage for a retrieval method or language model.

**Keywords:** retrieval; context composition; coverage; dependency closure; resource budget; submodularity.

## 1. The question between retrieval and answering

A retrieval system proposes material that may support an answer. The original retrieval-augmented generation formulation combines external retrieval with a generative model [1]. That architecture does not itself certify that every necessary condition reached the generator or survived its answer.

Our question is: **what can be certified about a bounded context assembled from a declared search result?** We separate four judgments: whether the search procedure examined the required scope; whether the available grounds support the requirements; whether the delivered representation fits the resource constraints; and whether the final answer preserves the required content.

These judgments are related but not interchangeable. Returning ten plausible passages does not prove that an eleventh exception does not exist. Fitting a token limit does not prove that the recipient notices a warning. A completed search does not make contradictory sources consistent.

## 2. Query, scope, and coverage

A query record fixes an intent, referents, time interpretation, requirements, permitted source scope, and answer form. Its requirements are obligations to establish or communicate, rather than merely words to match. A request for one supporting example has different obligations from a request for all examples, a count, or a statement that none exists.

Let \(S\) be the declared source snapshot and \(C\) the returned candidate set. Search assurance concerns the procedure that produced \(C\). An exhaustive finite scan under a specified predicate can support completeness within \(S\); a top-ranked sample generally cannot. Changes to access visibility, scope membership, predicates, or ranking rules can change the answer even if previously returned records are unchanged.

Coverage is assessed relative to a pinned requirement set \(R\). For each requirement we distinguish supported, partial, unsupported, conflicted, and unknown. These are reporting categories with explicit criteria, not a universal many-valued logic. “Unsupported in this package” does not mean false, absent from the whole corpus, or impossible to establish.

Coverage should be recorded at three boundaries: the registered source base, the retrieved candidates, and the delivered package. A fourth check concerns the actual answer or action proposal. Keeping these reports distinct locates loss: missing from the base, missed by retrieval, omitted during composition, or ignored during generation.

## 3. Composition with joint grounds and dependencies

Let \(V\) be a finite set of candidate object revisions. For a selected subset \(A\subseteq V\), let \(\operatorname{cl}(A)\) denote its mandatory dependency closure under a fixed, declared graph. A requirement \(r\) can have alternative supporting groups \(\mathcal G_r\). A group contains jointly necessary grounds, not merely individually relevant fragments.

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

The budget may be a vector: tokens, bytes, recipient time, or another measured resource. Different units should not be silently added. A scalar objective requires a declared conversion or priority rule.

Costs need not be additive over fragments. Two selected objects can share a dependency, so summing their separately closed sizes double-counts it. Conversely, a delivery format can introduce headings, repeated legends, or fixed overhead. The delivered representation, rather than the unformatted fragments, is the relevant accounting object.

Least graph closure is also relative to the chosen granularity. The [projection study](../../engineering/studies/executable-projections-and-revision/STUDY.md#counterexample-to-claim-level-minimality) found extra claims inside a shared qualification even when their dedicated nodes were absent from the selected closure. A least entity set therefore need not be claim-minimal or cheapest to deliver.

## 4. Exactness and special-case guarantees

### Proposition 1. Complete finite selection gives a scoped optimum

Let \(Z\) be a finite, explicitly declared decision space. Suppose feasibility and objective value are evaluated correctly for every member. If enumeration finishes and returns a feasible member with maximal objective, that member is optimal in \(Z\). If enumeration finishes with no feasible member, no feasible member exists in \(Z\).

**Proof.** Every possible decision in the declared space has been checked. A better feasible decision or any feasible decision in the second case would therefore have appeared in the enumeration, contradicting the stated result. ∎

This establishes neither completeness of \(Z\) relative to all possible summaries nor correctness of semantic annotations. If execution stops early, the best verified candidate remains a feasible incumbent; optimality and infeasibility are no longer established.

### Proposition 2. A restricted composition problem contains set cover

Consider unit-cost, independent packages, no transformations or dependencies, and the requirement to cover every obligation using at most \(k\) packages. Given a set-cover instance with universe \(U\) and subsets \(F_1,\ldots,F_n\), create one requirement per element of \(U\) and one package per \(F_i\), supporting exactly those requirements. The construction is polynomial, and selected packages cover all requirements exactly when their corresponding subsets cover \(U\).

This reduction transfers the known combinatorial difficulty of set cover [2] to this special case. It does not imply that every practical query is difficult, that extraction itself is formally solved, or that a heuristic has a particular approximation ratio.

### Proposition 3. The cardinality-greedy bound requires submodularity

Let \(f\) be a nonnegative, monotone, submodular set function with \(f(\varnothing)=0\). With at most \(k\geq1\) selected elements and no other constraints, greedy selection by greatest marginal gain achieves at least

\[
\left(1-\left(1-\frac1k\right)^k\right)\operatorname{OPT}
\geq (1-1/e)\operatorname{OPT}.
\]

**Argument.** Let \(O\) be an optimal set. At step \(i\), monotonicity gives \(\operatorname{OPT}=f(O)\leq f(A_i\cup O)\). Submodularity bounds the gain from \(A_i\) to \(A_i\cup O\) by the sum of at most \(k\) current single-element marginal gains. The best next gain is therefore at least \((\operatorname{OPT}-f(A_i))/k\). Each step reduces the remaining gap by a factor no greater than \(1-1/k\). Iterating from the empty set gives the bound. This is the classical result of Nemhauser, Wolsey, and Fisher [3], not a new theorem of the present model. ∎

The result does not cover arbitrary size-based greedy selection, nonadditive costs, or arbitrary mandatory closure. Those settings need their own justified algorithms and assumptions.

## 5. Counterexamples to convenient assumptions

Joint grounds need not be submodular. Suppose a requirement needs both a rule \(a\) and a condition \(b\). Let \(f(\varnothing)=f(\{a\})=f(\{b\})=0\), but \(f(\{a,b\})=1\). Adding \(b\) to the empty set yields no gain; adding it after \(a\) yields one. This violates diminishing returns. Individual ranking can therefore discard both members of the only useful pair.

Feasible root selections need not be downward-closed because coverage is mandatory. Consider one requirement whose only supporting group is \(\{a\}\), no dependencies, and a budget large enough for \(a\). The selection \(A=\{a\}\) is feasible, but its subset \(\varnothing\) does not cover the requirement. This counterexample uses the same closure-based support definition as §3.

Selected roots and delivered objects must not be confused. Removing a required condition from a root set can leave its closure unchanged because another selected root still requires it. Removing that condition from the actual delivered set is different: the resulting delivery may fail the closure obligation. A method justified for downward-closed feasible selections cannot be imported without checking which of these objects its guarantee concerns.

Budget pressure does not remove these obligations. If two mandatory grounds and an exception cost seven units in total and the budget is five, deleting the exception produces a smaller but inadmissible package. A feasible reformulation might exist, but it must be constructed and checked. Failure of one heuristic to find it is not proof of impossibility.

Finally, declared coverage can be invalidated by new information. Support is monotone only under explicitly fixed grounds, applicability judgments, and conflict rules. An added contradictory source or a changed requirement can require reassessment even when old passages remain available.

## 6. Stopping and measurement

A useful result reports its scope and stopping reason. Distinct outcomes include a verified complete package, an explicitly partial package, a need for clarification, insufficient resources, an exhausted search limit, and stale or conflicting evidence. Stopping after a limit does not establish absence. A useful partial answer is possible when the answer form permits it and its uncovered obligations remain visible.

Evaluation should compare methods under the same requirement snapshot, source scope, delivery constraints, and outcome rubric. Relevant baselines include ranked selection with dependency repair, selection of complete supporting groups, and exact enumeration on small instances. Removing dependencies or truncating delivery supplies ablations, not necessarily competitive baselines.

Measures should distinguish retrieval misses, invalid support groups, omitted dependencies, budget violations, and final-answer failures. Report denominators and uncertainty, including the number of cases that could not be adjudicated. Counting selected fragments or citing a larger source list does not measure sufficiency.

The mathematical results here hold for the declared finite model. They establish neither universal end-to-end answer correctness nor measured superiority on people, models, or production workloads. Recipient understanding and attention require separate observation, even when representation cost is measured exactly.

## 7. Connections to the published engineering work

The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) supplies exhaustive fixed-graph closure checks for all-required dependencies, plus historical layout and preliminary delivery checks. Its root-subset enumeration is not a budgeted composition optimizer. Alternative supporting groups, resource-constrained selection, and the counterexamples in §5 have no executable selection study in this corpus. The [projection study](../../engineering/studies/executable-projections-and-revision/STUDY.md) supplies the distinct counterexample to claim-level minimality. The [contract profile conformance study](../../engineering/studies/contract-profile-conformance/STUDY.md) concerns structural validation, which must remain distinct from semantic sufficiency.

The [glossary](../../reference/glossary/GLOSSARY.md) gives common terminology. [Evidence and falsification](../evidence-and-falsification/PAPER.md) specifies evaluation obligations; [knowledge utility](../knowledge-utility/PAPER.md) explains why a composition objective must state its baseline, horizon, and resource accounting.

## References

1. Lewis, P., et al. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *Advances in Neural Information Processing Systems* 33, 2020. <https://arxiv.org/abs/2005.11401>
2. Karp, R. M. “Reducibility Among Combinatorial Problems.” In *Complexity of Computer Computations*, 1972, 85–103. <https://doi.org/10.1007/978-1-4684-2001-2_9>
3. Nemhauser, G. L., Wolsey, L. A., and Fisher, M. L. “An Analysis of Approximations for Maximizing Submodular Set Functions—I.” *Mathematical Programming* 14, 1978, 265–294. <https://doi.org/10.1007/BF01588971>
