---
name: "constrained-transformations"
title: "Constrained Transformations and the Limits of Knowledge Transfer"
artifact: "scientific-paper"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Conditional preservation, composition and reconstruction of knowledge under explicit observations and losses."
---

# Constrained Transformations and the Limits of Knowledge Transfer

**Author:** Pavel Valentov · **Publication edition:** 1.0

## Abstract

Knowledge is repeatedly transformed: interpreted from a source, normalized, summarized, projected into a task, or instantiated for a new situation. A successful transformation need not preserve every property, but it must preserve the properties on which its permitted use depends. This paper models transformations as partial relations with explicit preconditions, protected observations, postconditions, and loss records. We prove conditional composition and preservation results, distinguish observation equivalence from identity, and show when a projection can or cannot be reversed. A separate result explains the limits of transferring a rule between domains. The claims concern declared transition models and successful executions; they do not imply that a transformation terminates, that its semantic annotations are complete, or that a language model follows the specified relation. The resulting obligations provide a precise basis for executable projections and for testing transformations with counterexamples.

**Keywords:** transformation contract; partial relation; semantic preservation; projection; transfer; reconstruction.

## 1. Research question and relation to prior work

An answer may retain the main words of a source while losing a condition that makes the answer usable. Conversely, a change of notation can preserve everything required for a particular task. The question is therefore not whether a transformation changes its input, but **which observations must remain valid, under which assumptions, for which use**.

We develop a task-relative account of transformation. It applies to changes of representation and to restricted inference, while keeping them distinct. Converting a value to another unit, summarizing an argument, and deriving a consequence require different premises. Naming all three “processing” does not supply a common correctness guarantee.

Hoare's account of program correctness separates preconditions, program execution, and postconditions [1]. Our formulation uses the same discipline at the boundary of knowledge operations. It does not claim that arbitrary natural-language transformations already have a mechanically verified semantics. The contribution is to expose the proof obligations and the cases in which a claim of preservation is too strong.

## 2. A transformation model

Let \(X\) and \(Y\) be declared spaces of input and output states. A transformation is a relation

\[
T\subseteq X\times Y.
\]

A relation, rather than a total function, permits multiple valid outputs and inputs on which the operation has no admitted result. A transformation contract specifies an input predicate \(P\), output predicate \(Q\), protected observations, and an account of allowed losses. Its partial-correctness condition is

\[
\forall x,y:\ P(x)\land T(x,y)\Rightarrow Q(y).
\]

This implication concerns successful transitions in \(T\). It neither promises an output for every admitted input nor bounds computation time. A practical implementation must separately distinguish successful output, refusal, ambiguity, insufficient budget, and execution failure.

A **protected observation** consists of interpretation functions \(p_X:X\to O\) and \(p_Y:Y\to O\) into a common observation space. Preservation means

\[
P(x)\land T(x,y)\Rightarrow p_X(x)=p_Y(y).
\]

The observations are selected for the task. They may include a numerical value, a referent, a condition, an attribution, or an unresolved uncertainty. Equality of two unknown observations preserves the recorded uncertainty; it does not establish the unknown proposition.

Not all transformations require equality. A projection may retain only a declared subset of observations; an inference may establish an output proposition from input premises under a rule. The contract must state which relation is required. Calling every relation “equivalence” would erase the distinction between preserving information and deriving a consequence.

## 3. Composition and preservation

### Proposition 1. Compatible partial-correctness contracts compose

Suppose \(T_1\subseteq X\times Y\) satisfies \(\{P\}T_1\{Q\}\), and \(T_2\subseteq Y\times Z\) satisfies \(\{R\}T_2\{S\}\). If \(Q(y)\Rightarrow R(y)\) for every intermediate state, then their relational composition satisfies \(\{P\}(T_2\circ T_1)\{S\}\).

**Proof.** For an admitted composed transition \((x,z)\), there is a state \(y\) such that \(T_1(x,y)\) and \(T_2(y,z)\). From \(P(x)\), the first contract yields \(Q(y)\). The compatibility assumption yields \(R(y)\), and the second contract yields \(S(z)\). ∎

This proposition does not prove total correctness. A second operation may have no successful transition for an intermediate state even when its partial-correctness implication holds. Existence of a result, termination, and resource sufficiency require additional assumptions.

### Proposition 2. A shared protected observation survives a finite chain

Let a finite chain of admitted transitions use observation functions into the same space \(O\). If every transition preserves the observation across its own interface, then the initial and final observations coincide.

**Proof.** Adjacent observations are equal by assumption. Equality is transitive, so repeated substitution gives equality between the first and last observations. ∎

The common-observation requirement is substantive. If one operation preserves a numerical value but drops its interpretation, and another preserves only the remaining text, the chain has not preserved a quantity with units. Local declarations about different properties do not combine into a stronger end-to-end claim.

A second counterexample concerns recipients. An operation may omit a condition because its current recipient already knows it. Passing the result to a different recipient changes that precondition. A technically intact record of the earlier check cannot restore a condition that the new recipient lacks.

## 4. Equivalence, projection, and residual information

For a fixed observation function \(p\), define

\[
x\sim_p x'\iff p(x)=p(x').
\]

This is an equivalence relation because equality is reflexive, symmetric, and transitive. It is an equivalence of declared observations, not of object identity or all meaning. Enlarging the observation set can split an equivalence class that was adequate for a narrower task.

A transformation descends to equivalence classes only if it respects the chosen relation. For a deterministic transformation \(f\), this requires that \(x\sim_p x'\) imply \(f(x)\sim_{p'}f(x')\). For a partial transformation, its domain must also contain every equivalent representative or none of them. Otherwise admission or output depends on which representative was selected, and replacing one representative by another is not justified.

A **projection** \(\pi_J\) retains observations indexed by \(J\). For coordinate projections, repeated application is idempotent and projection to a smaller set loses no further information about those retained coordinates. These properties follow from the defined operation; they must not be assumed for an arbitrary summarizer merely called a projection.

### Proposition 3. A noninjective transformation cannot have a left inverse

Let \(f:X\to Y\) map two distinct inputs \(x_1\ne x_2\) to the same output. There is no function \(g:Y\to X\) satisfying \(g(f(x))=x\) for all \(x\in X\).

**Proof.** Such a function would require the same value \(g(f(x_1))=g(f(x_2))\) to equal both distinct inputs. ∎

Reconstruction becomes possible if a retained residual \(\rho(x)\) makes the pair \((f(x),\rho(x))\) sufficiently informative and a reconstruction function is defined on that pair. For example, a projection of a two-component record can be reversed when the omitted component is stored as residual information. That restoration uses additional retained information. It is not evidence that compression creates information or that every summary is reversible.

Loss records must therefore distinguish intentionally omitted content, unresolved interpretation, and information retained elsewhere. A link to a residual helps only when the recipient can retrieve and interpret it within the permitted scope and resource budget.

A finite Boolean model gives an exact special case of shared content and residual information. Write \(M(F)\) for the models of formula \(F\). Entailment is inclusion of model sets. The formula \(C=F\lor G\) is a strongest common consequence of \(F\) and \(G\): both entail \(C\), and any consequence of both is true throughout \(M(F)\cup M(G)=M(C)\). Define \(R_F=\neg C\lor F\). Then

\[
C\land R_F=C\land(\neg C\lor F)\equiv C\land F\equiv F,
\]

because \(F\) entails \(C\). This proves reconstruction with that residual in the declared logic. It does not identify a useful common theme between arbitrary documents. The residual convention is also not unique outside \(C\). An inconsistent premise set has no models and classically entails every formula; operational admission must therefore separately require an appropriate consistent, nonempty interpretation rather than turn vacuous entailment into a recommendation.

## 5. Transfer between tasks and domains

Transfer is a directed operation. A rule applicable under conditions \(C\) can be used for a target only after those conditions have been mapped and checked. Similar vocabulary is a candidate-generation signal, not a proof that the required relation is preserved.

Consider a source rule

\[
C(x)\Rightarrow P(x).
\]

To infer \(P'(y)\) in a target representation, one needs a mapping between the relevant source and target objects, justification of the corresponding condition, and a bridge showing that the source conclusion supports \(P'\). Without such a bridge, the source rule remains a statement about its original interpretation.

An abstract counterexample is sufficient. Two systems can share a scalar variable called “size,” while one has output proportional to size and the other has output proportional to its square. Matching the variable name and one observed point does not justify transferring the linear rule. A usable transfer contract identifies the governing relation and its domain, rather than relying on surface similarity.

Units provide a limited positive case. If two units describe the same dimension and their relation is an exact rational factor, exact conversion preserves the represented quantity. The conclusion depends on dimension compatibility, the factor, and exact arithmetic. It does not validate an incorrectly extracted input value, an uncertain measurement, or an unrelated domain equation.

## 6. Records, implementation, and tests

A transformation record should identify the input and output revisions, declared operation, active preconditions, protected observations, verification result, and any loss or residual. Provenance is useful here because it makes dependencies inspectable [2]. Provenance alone does not establish that the operation satisfied its contract.

An implementation claiming compliance must connect its actual outputs to the relation used in the argument. A contract written next to a model does not constrain the model's behavior unless execution is checked or the implementation is independently justified. A finite checker can establish only properties in its supported language and bounded domain. Unsupported rules remain unsupported; they do not become valid because the system produces a plausible explanation.

Tests should include incompatible intermediate types, a dropped exception, changed recipients, a noninjective projection offered as reversible, an omitted residual, and a transfer with matching labels but incompatible relations. Positive tests should vary irrelevant features while keeping protected observations fixed. Negative tests should change one material assumption at a time and require refusal, qualified output, or a failed check.

The propositions in this paper are complete within their stated mathematical assumptions. No empirical claim is made that a particular extractor or generator reliably supplies those assumptions. The corresponding measurement question is the frequency and consequence of violations on independently constructed transformations, with separate reporting for interpretation, execution, and verification errors.

## 7. Connections to the published engineering work

The [executable projections and revision study](../../engineering/studies/executable-projections-and-revision/STUDY.md) is the location for finite transition implementations and their controls. The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) examines whether protected conditions survive actual delivery. Domain-specific conversions and transfers belong in those studies.

The shared [glossary](../../reference/glossary/GLOSSARY.md) defines project terminology. [Semantic objects and context](../semantic-objects-and-context/PAPER.md) supplies the interpretation boundary; [controlled knowledge reuse](../controlled-knowledge-reuse/PAPER.md) applies the preservation argument to previously prepared artifacts.

## References

1. Hoare, C. A. R. “An Axiomatic Basis for Computer Programming.” *Communications of the ACM* 12(10), 1969, 576–580, 583. <https://doi.org/10.1145/363235.363259>
2. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
