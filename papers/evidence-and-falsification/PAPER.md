---
name: "evidence-and-falsification"
title: "Evidence, Reasoning, and Falsification in Knowledge Systems"
artifact: "scientific-paper"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "How claims, proofs, finite tests, counterexamples and comparative evaluations support different conclusions."
---

# Evidence, Reasoning, and Falsification in Knowledge Systems

**Author:** Pavel Valentov · **Publication edition:** 1.0

## Abstract

A knowledge system can pass structural checks while offering an unsupported conclusion. It can also possess a sound formal argument whose assumptions are not satisfied by an implementation. This paper specifies how to connect claims, grounds, inference rules, checks, and decisions without confusing their evidential roles. We define a claim record and a finite justification graph, prove a conditional soundness property for supported acyclic derivations, and characterize the scope of finite testing. We then give a falsification protocol that separates counterexamples to a model, implementation defects, annotation failures, and limits of empirical transfer. Evaluation must use pinned requirements, explicit comparators, independent reference judgments where needed, and a predeclared analysis and stopping policy. The contribution is a method for determining exactly what a result supports, including negative findings and unresolved claims. No number of structural checks is treated as proof of unrestricted semantic correctness or practical superiority.

**Keywords:** evidence; inference; falsification; claim scope; evaluation; counterexample.

## 1. Research question and evidential distinctions

Knowledge systems produce many objects that resemble evidence: citations, validation reports, explanations, benchmark scores, approvals, and execution logs. Their resemblance does not make them interchangeable. A citation can establish provenance without establishing truth. Approval can establish permission without establishing correctness. A passing test can establish one observed behavior without establishing all possible behaviors.

We ask: **how can a scientific and engineering claim remain accountable to the kind, scope, and limitations of its actual grounds?** Our answer is a claim-centered method connecting each assertion to its premises, evaluators, counterexamples, and revision conditions.

Program-logic reasoning already makes correctness conditional on stated preconditions and semantics [1]. PROV-DM provides a vocabulary for the origins and production of entities [2]. We use those distinctions while addressing a further operational problem: evidence about a source, model, checker, implementation, and deployment must not silently migrate between those subjects.

## 2. Claims and independent assessment axes

A **claim** is a proposition or quantified assertion with an identified subject, scope, and interpretation. A useful record specifies its content, revision, claim kind, assumptions, supporting grounds, potential refuters, assessment method, and unresolved dependencies. The scope includes relevant versions, task distribution, population, time interval, and operating conditions when those matter.

Claim kinds include definitional, deductive, empirical, comparative, causal, and normative. These are not mutually exclusive labels for an entire document: a paper can define a model, prove a property of it, and propose an empirical hypothesis. Each assertion needs the appropriate grounds.

We distinguish at least five questions:

- Is the source or record authentic and correctly attributed?
- Is its represented content faithful to that source?
- Does the evidence support the proposition under the stated interpretation?
- Is the proposition applicable to the current use?
- Is the proposed use authorized?

These assessments need not agree. An accurately attributed false statement can be useful as an object of refutation. A true proposition can be inapplicable to a different date. An authorized decision can be poorly supported. A single confidence score cannot preserve these distinctions unless its meaning and aggregation rule explicitly encode them.

Unknown is not false, and absence of a recorded refutation is not confirmation. An assessment can remain unresolved while a restricted informational output is permitted. A mandatory action precondition, however, is not satisfied merely because the system failed to find contrary evidence.

## 3. Justification graphs and conditional soundness

A **justification graph** contains claim nodes, premise nodes, and explicit inference applications. An inference application identifies its rule, input claims, output claim, and relevant side conditions. It may also carry a computation or verification witness. The graph is an explanation of the offered justification, not a complete record of every internal mental or computational event.

For the following result, take a finite directed acyclic derivation graph. Each leaf is a premise, and every other claim is obtained by a supported inference rule whose inputs appear earlier in a topological order. Interpret truth in one fixed domain model.

### Proposition 1. Sound rules preserve true premises in a finite derivation

If every premise is true in the model and every used rule is sound for that model, every derived claim is true in that model.

**Proof.** Order the graph topologically. The initial premise nodes are true by assumption. At each subsequent node, all input claims are true by the induction hypothesis. Soundness of the applied rule makes the output true. Induction covers every node. ∎

The result is conditional on both premises and rule semantics. It does not show that the premises were correctly extracted, that the domain model is adequate, or that the implementation actually followed the rule. A computation with correctly applied arithmetic and an incorrectly read input remains an incorrect domain result.

Circular support is outside this proof. A cycle that repeats a conclusion as its own premise supplies no independent foundation. Some systems admit explicitly defined fixed-point reasoning, but they require a separate semantics and correctness argument. Finite serialization of a cycle is not that argument.

### Proposition 2. A countermodel refutes a universal claim within its scope

For a claim \(\forall x\in D, P(x)\), an admissible \(x_0\in D\) with \(\neg P(x_0)\) refutes the claim.

**Proof.** Universal quantification requires \(P\) for every element of \(D\), including \(x_0\). ∎

The domain condition matters. A failure outside the claimed domain can motivate a broader study but does not refute the narrower theorem. Conversely, narrowing the domain after seeing a failure produces a revised claim; it does not retroactively turn the original claim into a successful one.

## 4. What different checks establish

Structural validation establishes compliance with a declared representation rule when the validator is correct. It may verify mandatory fields, references, enumerations, or finite relational conditions. It does not establish that a field's natural-language content is correctly interpreted.

A formal proof establishes a consequence under its assumptions and formal semantics. Executable tests establish observed behavior for the tested cases, subject to their oracle and execution conditions. An exhaustive finite test can support a universal statement about its enumerated finite model; it does not automatically cover unbounded inputs or a deployed environment with different behavior.

Human review can assess interpretation, relevance, and argument quality within a defined rubric. Its strength depends on expertise, access to sources, independence, and adjudication. Production observations can reveal actual failures and costs, but selected observations alone do not identify a causal benefit.

These evidence types are complementary, not a single ladder on which more items always mean stronger support. Ten tests sharing the same incorrect oracle can repeat one mistake. Two reviewers with access to each other's answer may not provide the intended independent judgment. Independence should be described as a concrete procedure, not inferred from different agent names.

## 5. A falsification protocol

An evaluation begins by freezing the claim and requirements before examining the decisive cases. The record should specify the subject versions, admissible inputs, expected behavior, failure criteria, scope of generalization, and how uncertain cases will be handled. Changes create a new evaluation record rather than overwriting the earlier one.

Counterexamples should target assumptions. For extraction, change a referent, logical scope, or source revision. For composition, omit a jointly required ground or add a conflicting condition. For reuse, change a material dependency or current permission. For resource accounting, repeat a telemetry event or expose a shared cost counted twice. The purpose is to distinguish a system that enforces the condition from one that merely passes familiar positive examples.

An independent impact oracle is especially important for dependency completeness. Traversing an annotated graph can verify traversal; it cannot reveal an omitted dependency if the reference answer is generated from that same graph. A useful test mutates a relevant source feature and independently specifies whether the output should change.

The protocol should separate at least four failure classes: the model's claim is false; the implementation violates the model; the input interpretation or annotation is wrong; or the evaluation lacks enough information to decide. Combining them into a single failure total can obscure the repair required.

## 6. Comparators, analysis, and stopping

A comparative claim needs a relevant baseline with matched tasks, resource accounting, and acceptance conditions. A method that produces more complete outputs at a higher cost must not be described as unconditionally cheaper. A method that skips required checks must not gain an apparent speed advantage without reporting the lost assurance.

The analysis plan should state the primary outcome, denominators, treatment of missing and unresolved cases, uncertainty estimates, and stopping conditions. If evaluation stops after a budget limit, the report should identify the covered and uncovered cases. Selecting only successful attempts or changing the success rule after inspection creates a different evidential object from the planned study.

Data separation also matters. Cases used to design a rule, tune a threshold, or repair an implementation are development evidence. A later evaluation can reuse them for regression testing, but should not label that reuse an unseen assessment. Shared sources, repeated near-duplicates, and leaked reference annotations can make nominally separate cases dependent.

For causal or practical-effect claims, the required design is stronger than a catalog of passing controls. The [knowledge utility paper](../knowledge-utility/PAPER.md) states the intervention and attribution conditions. Observed use, user approval, or a plausible demonstration alone does not establish that the system improved outcomes relative to a meaningful alternative.

## 7. The evidential status of this research program

The scientific results presented here are definitions, explicit conditional arguments, and countermodels. They specify what a compliant knowledge process would have to preserve. Published engineering studies provide the separate place for reproducible executions, actual observations, and their limits. A link to a study is not a declaration that every proposed experiment has been performed; the study's own methods and evidence record determine its scope.

This distinction allows a formal or methodological paper to have a complete argument while practical hypotheses remain open. Completion means that the paper states and supports its actual contribution, not that every imaginable deployment question has been settled. Conversely, removing a provisional label cannot substitute for missing evidence.

The central falsifiable engineering prediction is conditional: if an implementation enforces a declared mandatory condition, cases that violate that condition should not receive the corresponding successful admission. Semantic and practical predictions require independently interpreted or measured outcomes in addition to structural controls.

The [contract profile conformance study](../../engineering/studies/contract-profile-conformance/STUDY.md), [source transcription and uncertainty study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md), and [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) address distinct subjects. The [editorial skill pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) addresses document production. Their results should remain separate until a justified analysis explains how they combine.

## 8. Scope and shared definitions

The model does not automate the discovery of every relevant premise, guarantee the trustworthiness of a reviewer, or establish universal usefulness of structured knowledge. It makes these dependencies inspectable and supplies conditions under which a particular claim can be rejected, retained, or narrowed.

The shared [glossary](../../reference/glossary/GLOSSARY.md) defines evidence, verification, authority, and related terms. [Revision and governance](../revision-and-governance/PAPER.md) specifies how new evidence changes assessments without erasing their history.

## References

1. Hoare, C. A. R. “An Axiomatic Basis for Computer Programming.” *Communications of the ACM* 12(10), 1969, 576–580, 583. <https://doi.org/10.1145/363235.363259>
2. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
