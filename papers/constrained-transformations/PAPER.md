---
name: "constrained-transformations"
title: "Knowledge Transformations: Constrained Transformations and the Limits of Knowledge Transfer"
short_title: "Knowledge Transformations"
subtitle: "Constrained Transformations and the Limits of Knowledge Transfer"
previous_title: "Constrained Transformations and the Limits of Knowledge Transfer"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Conditional preservation, composition and reconstruction of knowledge under explicit observations and losses."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="constrained-transformations-and-the-limits-of-knowledge-transfer"></a>

# Knowledge Transformations: Constrained Transformations and the Limits of Knowledge Transfer

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

A transformation can retain a source's words while losing a condition needed for their use. Conversely, a change of representation can preserve every observation required by a particular task. This paper asks when such preservation survives a sequence of operations, which distinctions a projection may discard, and what is needed for reconstruction or transfer. We model transformations as partial relations with explicit preconditions, postconditions, protected observations, and loss records. Two conditional propositions establish partial-correctness composition and endpoint preservation when adjacent steps have compatible preconditions and agree on the observation passed between them. A third proposition rules out a left inverse for a noninjective transformation. We distinguish observation equivalence from identity, state coordinate-projection laws with their domains and codomains, and make the retained-information condition for reconstruction explicit. A Boolean construction illustrates shared consequences and residuals without claiming compression or general document similarity. Cross-domain examples explain why matching labels do not justify transferring a rule. The method is deductive: these results do not establish termination, complete semantic annotation, or compliance by a deployed model. Their role is to make the assumptions and limits of a preservation claim inspectable and refutable.

**Keywords:** transformation contract; partial relation; semantic preservation; projection; transfer; reconstruction.

## 1. Research question and relation to prior work

An answer may retain the main words of a source while losing a condition that makes the answer usable. A change of notation, by contrast, can preserve everything required for a particular task. The research question is therefore **which observations must remain valid, under which assumptions, for which use**. Byte identity, similar wording, and semantic preservation answer different questions.

The account is task-relative. It covers representation changes and restricted inference but does not equate them. Converting a value to another unit, summarizing an argument, and deriving a consequence require different premises. A common label such as “processing” supplies no common correctness guarantee.

Hoare's account of program correctness separates preconditions, execution, and postconditions [1]. We use that discipline to state obligations at the boundary of knowledge operations. The composition argument is an application of established partial-correctness reasoning, not a claim to have invented sequential composition. Similarly, observation equivalence and the obstruction to inverting a noninjective function use elementary mathematics. The contribution is their explicit, bounded application to knowledge artifacts: a chain must preserve the same task-relevant observation, reconstruction must account for discarded information, and transfer needs a justified bridge between interpretations.

The method is deductive. We define a transition model, derive consequences from stated premises, and construct cases in which omitting a premise defeats the proposed justification. The proofs concern the declared model. They do not establish that arbitrary natural-language transformations have a complete formal semantics or that a particular implementation follows that model. Section 7 separates the existing engineering evidence from the mathematical argument.

## 2. A transformation model

Let \(X\) and \(Y\) be declared spaces of input and output states. A transformation is a relation

\[
T\subseteq X\times Y.
\]

A relation permits more than one admitted output for an input, and it need not supply an output for every input. A transformation contract specifies an input predicate \(P\), an output predicate \(Q\), protected observations, and allowed losses. Its partial-correctness condition is

\[
\forall x,y:\ P(x)\land T(x,y)\Rightarrow Q(y).
\]

This implication concerns successful transitions in \(T\). It neither promises an output for every admitted input nor bounds computation time. In particular, a relation with no transition can satisfy the implication without producing a useful result. A practical implementation must separately distinguish successful output, refusal, ambiguity, insufficient budget, and execution failure.

A **protected observation** consists of interpretation functions \(p_X:X\to O\) and \(p_Y:Y\to O\) into a common observation space. Preservation means

\[
P(x)\land T(x,y)\Rightarrow p_X(x)=p_Y(y).
\]

The preservation condition is universal over the admitted transitions: when an input has several possible outputs, each output in the relation must satisfy it. One successful sampled output does not establish preservation for the other possible outputs.

The observations are selected for the task. They may include a numerical value, referent, condition, attribution, or unresolved uncertainty. Equality of two unknown observations preserves the recorded uncertainty; it does not establish the unknown proposition. Selecting and justifying the observation functions is itself an obligation: the equations do not discover which semantic features the task requires.

Not all transformations require equality. A projection may retain only a declared subset of observations; an inference may establish an output proposition from input premises under a rule. The contract must state which relation is required. Calling every relation “equivalence” would erase the distinction between preserving information and deriving a consequence.

## 3. Composition and preservation

### Proposition 1. Compatible partial-correctness contracts compose

Suppose \(T_1\subseteq X\times Y\) satisfies \(\{P\}T_1\{Q\}\), and \(T_2\subseteq Y\times Z\) satisfies \(\{R\}T_2\{S\}\). If \(Q(y)\Rightarrow R(y)\) for every intermediate state, then their relational composition satisfies \(\{P\}(T_2\circ T_1)\{S\}\).

**Proof.** For an admitted composed transition \((x,z)\), there is a state \(y\) such that \(T_1(x,y)\) and \(T_2(y,z)\). From \(P(x)\), the first contract yields \(Q(y)\). The compatibility assumption yields \(R(y)\), and the second contract yields \(S(z)\). ∎

This proposition does not prove total correctness. A second operation may have no successful transition for an intermediate state even when its partial-correctness implication holds. Existence of a result, termination, and resource sufficiency require additional assumptions.

### Proposition 2. A shared protected observation survives a finite chain

Let \(n\geq1\) and \(T_i\subseteq X_{i-1}\times X_i\) for \(1\leq i\leq n\). Each step satisfies \(\{P_i\}T_i\{Q_i\}\) and preserves observations \(p_i^-:X_{i-1}\to O\), \(p_i^+:X_i\to O\) whenever \(P_i\) holds. At every junction require

\[
Q_i(x)\Rightarrow P_{i+1}(x),
\qquad
Q_i(x)\Rightarrow p_i^+(x)=p_{i+1}^-(x),
\quad 1\leq i<n.
\]

For any successful chain \(T_i(x_{i-1},x_i)\) beginning with \(P_1(x_0)\), these conditions imply

\[
p_1^-(x_0)=p_n^+(x_n).
\]

**Proof.** Partial correctness of the first step yields \(Q_1(x_1)\). The first junction implication supplies \(P_2(x_1)\); induction gives every subsequent precondition and postcondition. Each step therefore preserves its observation on the actual transition. The second junction implication equates the preceding output observation with the following input observation on each intermediate state. Substituting those within-step and between-step equalities gives the displayed endpoint equality. ∎

Both junction requirements are necessary to this argument. On \(\{0,1\}\), take two identity transitions, with identity observations at both interfaces of the first step and Boolean negation at both interfaces of the second. Each step preserves its own observations, and the state chain is \(x\to x\to x\). Nevertheless, the initial observation is \(x\) and the final observation is \(1-x\): the observation functions disagree at the intermediate interface. Separately, let the first transition be identity with an unrestricted precondition and the second map both inputs to \(1\), with precondition \(x=1\). With identity observations throughout, both local contracts preserve observations on their admitted inputs. Nevertheless the composed path \(0\to0\to1\) changes the observation because the second precondition is not met.

The common-observation requirement is substantive. If one operation preserves a numerical value but drops its interpretation, and another preserves only the remaining text, the chain has not preserved a quantity with units. Local declarations about different properties do not combine into a stronger end-to-end claim.

A second counterexample concerns recipients. An operation may omit a condition because its current recipient already knows it. Passing the result to a different recipient changes that precondition. A technically intact record of the earlier check cannot restore a condition that the new recipient lacks.

The two propositions provide sufficient compositional conditions. Failure of a stated premise prevents using that argument; it does not imply that every particular run violating the premise must lose its endpoint observation. A counterexample to a conditional proposition would have to satisfy all its premises while falsifying its conclusion.

## 4. Equivalence, projection, and residual information

For a fixed observation function \(p\), define

\[
x\sim_p x'\iff p(x)=p(x').
\]

This is an equivalence relation because equality is reflexive, symmetric, and transitive. It is an equivalence of declared observations, not of object identity or all meaning. Enlarging the observation set can split an equivalence class that was adequate for a narrower task.

A transformation descends to equivalence classes only if it respects the chosen relation. For a deterministic transformation \(f\), this requires that \(x\sim_p x'\) imply \(f(x)\sim_{p'}f(x')\). For a deterministic partial transformation, its domain must also contain every equivalent representative or none of them. Otherwise admission or output depends on which representative was selected, and replacing one representative by another is not justified. For a nondeterministic relation, a quotient construction requires its own stated criterion for the reachable output classes; the deterministic-function condition alone does not specify that construction.

A **projection** \(\pi_J\) retains observations indexed by \(J\). The coordinate-projection law must respect the input and output types. Let \(X_K\) be the space of records indexed by \(K\), and let \(\pi_J^K:X_K\to X_J\) be restriction to \(J\subseteq K\). For \(I\subseteq J\subseteq K\),

\[
\pi_I^J\circ\pi_J^K=\pi_I^K,
\qquad \pi_J^J=\operatorname{id}_{X_J}.
\]

Thus, restricting first to the intermediate coordinates and then to the retained coordinates has the same result as restricting directly to the retained coordinates. Applying the identity restriction on the resulting space makes no further change. This is the typed form of repeated coordinate selection. The expression \(\pi_J^K\circ\pi_J^K\) need not even be defined when the domain and codomain differ. An idempotence equation for a projection on one state space requires a separately defined endomorphism of that space. None of these laws follows merely from calling an arbitrary summarizer a projection.

### Proposition 3. A noninjective transformation cannot have a left inverse

Let \(f:X\to Y\) map two distinct inputs \(x_1\ne x_2\) to the same output. There is no function \(g:Y\to X\) satisfying \(g(f(x))=x\) for all \(x\in X\).

**Proof.** Such a function would require the same value \(g(f(x_1))=g(f(x_2))\) to equal both distinct inputs. ∎

A retained residual \(\rho(x)\) can distinguish inputs that the transformation alone merges. The pair \((f(x),\rho(x))\) is an augmented encoding:

\[
h(x)=(f(x),\rho(x)).
\]

A reconstruction function on the image of this encoding recovers every input exactly if and only if the augmented encoding is injective on the declared source domain. Necessity follows by the same collision argument as Proposition 3. For sufficiency, assign each attained pair its unique preimage. This is a set-theoretic statement about reconstruction on the image; it supplies neither an algorithm nor a bound on time or storage. An actual consumer also needs a decoder it can execute and access to the correct residual.

For example, a projection of a two-component record can be reversed when the omitted component is stored as residual information. That restoration uses additional retained information. A residual that repeats only the retained component does not separate the lost alternatives. Neither example shows that compression creates information or that every summary is reversible.

Bancilhon and Spyratos use a view together with a complement to determine the database state and constrain view-update translation [3]. That established construction motivates the distinction between a projection and the information needed to reconstruct its source. The present model states a reconstruction obligation for knowledge artifacts; it does not establish the view-update laws or a general bidirectional transformation for natural-language summaries.

Loss records must therefore distinguish intentionally omitted content, unresolved interpretation, and information retained elsewhere. A link to a residual helps only when the recipient can retrieve and interpret it within the permitted scope and resource budget.

A finite Boolean model gives an exact special case of shared content and residual information. Fix a common finite propositional signature and classical truth-assignment semantics for all formulas in this construction. Write \(M(F)\) for the models of formula \(F\). Entailment is inclusion of model sets. The formula \(C=F\lor G\) is a strongest common consequence of \(F\) and \(G\): both entail \(C\), and any consequence of both is true throughout \(M(F)\cup M(G)=M(C)\). Define \(R_F=\neg C\lor F\). Then

\[
C\land R_F=C\land(\neg C\lor F)\equiv C\land F\equiv F,
\]

because \(F\) entails \(C\). The reconstruction is logical equivalence in this fixed language, not recovery of the original spelling, syntax tree, or source document. It does not establish economy: \(R_F=F\) also reconstructs \(F\), and a claim that another residual is smaller requires a separate size measure and comparison. The strongest common consequence is defined by entailment, not by textual similarity or a useful theme between arbitrary documents.

The residual convention is not unique outside \(C\): changing a residual's truth values there does not change its conjunction with the common consequence. An inconsistent premise set has no models and classically entails every formula. Operational admission must therefore separately require an appropriate consistent, nonempty interpretation rather than turn vacuous entailment into a recommendation.

## 5. Transfer between tasks and domains

Transfer is a directed operation. A rule applicable under conditions \(C\) can be used for a target only after those conditions have been mapped and checked. Similar vocabulary is a candidate-generation signal, not a proof that the required relation is preserved.

Consider a source rule

\[
C(x)\Rightarrow P(x).
\]

To infer \(P'(y)\) in a target representation, one needs a mapping between the relevant source and target objects, justification of the corresponding condition, and a bridge showing that the source conclusion supports \(P'\). Without such a bridge, the source rule remains a statement about its original interpretation.

An abstract counterexample is sufficient. Two systems can share a scalar variable called “size,” while one has output proportional to size and the other has output proportional to its square. With both proportionality constants set to one, they agree at size one but differ at size two: the outputs are two and four. This is a constructed mathematical example, not an observed experiment. Matching the variable name and one point does not justify transferring the linear rule. A usable transfer contract identifies the governing relation and its domain, rather than relying on surface similarity.

Units provide a limited positive case. If two units describe the same dimension and their relation is an exact rational factor, exact conversion preserves the represented quantity. The conclusion depends on dimension compatibility, the factor, and exact arithmetic. Same-dimension labels alone do not establish that multiplicative relation. Nor does conversion validate an incorrectly extracted input value, remove measurement uncertainty, or justify an unrelated domain equation.

## 6. Records, implementation, and tests

A transformation record should identify the input and output revisions, declared operation, active preconditions, protected observations, verification result, and any loss or residual. Provenance is useful here because it makes dependencies inspectable [2]. Provenance alone does not establish that the operation satisfied its contract.

An implementation claiming compliance must connect its actual outputs to the relation used in the argument. A contract written next to a model does not constrain the model's behavior unless execution is checked or the implementation is independently justified. A finite checker can establish only properties in its supported language and bounded domain. Unsupported rules remain unsupported; they do not become valid because the system produces a plausible explanation.

Tests should include incompatible intermediate types, a dropped exception, changed recipients, a noninjective projection offered as reversible, an omitted residual, and a transfer with matching labels but incompatible relations. Positive tests should vary irrelevant features while keeping protected observations fixed. Negative tests should change one material assumption at a time and check the declared refusal, qualification, or failure behavior.

A test report must identify what it exercised: the abstract relation, a finite checker, or the actual implementation. It must also state the carrier, parameter ranges, assumptions, and unit counted. Enumerating a finite model checks that model within those bounds. It neither constitutes an empirical trial on human meanings nor shows that a deployed model enforces the same conditions. A premise-violating example tests the boundary of the justification; a genuine refutation of a proposition requires all its premises and a false conclusion.

The propositions establish the selected composition, preservation, and reconstruction properties under their explicit assumptions. They are not a completeness claim about all knowledge transformations. No empirical claim is made that a particular extractor or generator reliably supplies those assumptions. The corresponding measurement question is the frequency and consequence of violations on independently constructed transformations, with separate reporting for interpretation, execution, and verification errors.

## 7. Connections to the published engineering work

The [executable projections and revision study](../../engineering/studies/executable-projections-and-revision/STUDY.md) reports finite consumer checks for partial extraction and addressed revision. The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) reports a fixed dependency graph, preserved artifact payloads, and a historical preliminary delivery decision. These controls concern the stated packages and projections; neither study evaluates every transformation relation or cross-domain transfer proposed here.

The shared [glossary](../../reference/glossary/GLOSSARY.md) defines project terminology. [Semantic objects and context](../semantic-objects-and-context/PAPER.md) supplies the interpretation boundary; [controlled knowledge reuse](../controlled-knowledge-reuse/PAPER.md) applies the preservation argument to previously prepared artifacts.

## 8. Conclusion

Preservation is a claim about declared observations under explicit conditions, not about unchanged words alone. Partial-correctness contracts compose when the first operation's postcondition supplies the next operation's precondition. Endpoint preservation additionally requires adjacent operations to agree on the observation they exchange. These conditions justify successful chains; they do not guarantee a result, termination, or compliance by a language model.

Projection and reconstruction require equally explicit boundaries. Coordinate restriction obeys a typed composition law. A noninjective transformation cannot recover every original input without distinguishing residual information, and an injective augmented encoding establishes only set-theoretic reconstructability until an executable decoder and accessible residual are supplied. In the Boolean illustration, reconstruction means logical equivalence, not restoration of source bytes or a demonstrated reduction in size.

The resulting method is to identify the property a task needs, state the permitted transformation and its assumptions, and check the actual result at the relevant boundary. Where a condition is unsupported, the preservation claim must be limited rather than inferred from a plausible output or a provenance record. Whether particular extractors and agents reliably meet these obligations remains an empirical question for separately specified studies.

## References

1. Hoare, C. A. R. “An Axiomatic Basis for Computer Programming.” *Communications of the ACM* 12(10), 1969, 576–580, 583. <https://doi.org/10.1145/363235.363259>
2. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
3. Bancilhon, F., and Spyratos, N. “Update Semantics of Relational Views.” *ACM Transactions on Database Systems* 6(4), 1981, 557–575. [Original article](https://cs.uwaterloo.ca/~david/cs848s18/constant-complement.pdf).
