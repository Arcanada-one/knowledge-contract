---
name: "evidence-and-falsification"
title: "Evidence and Falsification: Evidence, Reasoning, and Falsification in Knowledge Systems"
short_title: "Evidence and Falsification"
subtitle: "Evidence, Reasoning, and Falsification in Knowledge Systems"
previous_title: "Evidence, Reasoning, and Falsification in Knowledge Systems"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "How claims, proofs, finite tests, counterexamples and comparative evaluations support different conclusions."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="evidence-reasoning-and-falsification-in-knowledge-systems"></a>

# Evidence and Falsification: Evidence, Reasoning, and Falsification in Knowledge Systems

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

A validation report, formal proof, review, and deployment log support different claims. Treating them as interchangeable can turn a correct structural check into an unsupported assertion about meaning or practical benefit. This paper asks how a knowledge system can keep a claim accountable to the subject, scope, and limitations of its actual grounds. We distinguish five assessment axes and represent offered justifications as finite graphs of premises and inference applications. Two conditional propositions state when sound rules preserve true premises and when an in-scope countermodel refutes a universal claim. We then specify a falsification protocol that separates failures of the model, implementation, interpretation, and evaluation. The protocol binds observations to exact subjects, retains unresolved outcomes, distinguishes boundary tests from theorem refutations, and requires appropriate comparators and stopping rules. Constructed cases expose shared-oracle errors, vacuous exclusion tests, and changes of scope after a failure. The method is deductive and methodological, not a new empirical benchmark or an automatic semantic verifier. Its contribution is a precise account of what may be concluded from a result, including what remains unmeasured or unsupported.

**Keywords:** evidence; inference; falsification; claim scope; evaluation; counterexample.

## 1. Research question and evidential distinctions

Knowledge systems produce citations, validation reports, explanations, benchmark scores, approvals, and execution logs. These objects can be relevant evidence without answering the same question. A citation can identify a source without establishing the truth of its content. Approval can establish permission without establishing correctness. A passing test can establish an observed behavior without covering every possible behavior.

We ask: **how can a scientific and engineering claim remain accountable to the kind, scope, and limitations of its actual grounds?** The proposed method connects each assertion to its subject, premises, assessment procedure, potential refuters, and revision conditions. It does not replace those grounds with one overall success label.

Program-logic reasoning already makes correctness conditional on stated preconditions and semantics [1]. PROV-DM provides a vocabulary for the origins and production of entities [2]. We use these established distinctions without claiming that conditional proof or provenance originate here. The additional operational concern is that evidence about a source, model, checker, implementation, and deployment must not silently migrate between those subjects.

The contribution has three parts: a separation of assessment questions; explicit boundaries for deductive and finite-test claims; and a falsification procedure that preserves both failures and uncertainty. The method is deductive and methodological. Section 3 proves two elementary conditional results, while the remaining sections specify obligations and constructed failure cases. The paper introduces neither a general algorithm for deciding natural-language truth nor measured evidence that the proposed organization improves agent performance.

## 2. Claims and independent assessment axes

A **claim** is a proposition or quantified assertion with an identified subject, scope, and interpretation. A useful record specifies its content, revision, claim kind, assumptions, supporting grounds, potential refuters, assessment method, and unresolved dependencies. Relevant versions, task distribution, population, time interval, and operating conditions belong to its scope when they can affect the conclusion.

Claim kinds include definitional, deductive, empirical, comparative, causal, and normative. They are not mutually exclusive labels for an entire document. A paper can define a model, prove a conditional property, and propose an empirical hypothesis; each assertion still needs the appropriate grounds. A definition fixes terminology within the model. Naming a desired property in that definition does not show that a real system has it.

**Table 1. Assessment axes that must not be silently substituted for one another.**

| Axis | Question | Insufficient substitute |
| --- | --- | --- |
| Authenticity and attribution | Is the source or record authentic and correctly attributed? | A plausible author label alone |
| Source fidelity | Is the represented content faithful to that source? | Valid fields or fluent wording alone |
| Evidential support | Do the grounds support the proposition under its stated interpretation? | A citation or positive receipt alone |
| Applicability | Does the proposition apply to the present use? | Correctness under a different date, task, or scope |
| Authorization | Is the proposed use permitted? | Truth, usefulness, or technical capability alone |

These assessments need not agree. An accurately attributed false statement can be useful as an object of refutation. A true proposition can be inapplicable to a different date. An authorized decision can be poorly supported. A single confidence score preserves these distinctions only if its interpretation and aggregation rule actually represent them; the presence of a number is not such an explanation.

Unknown is not false, and absence of a recorded refutation is not confirmation. An assessment can remain unresolved while a restricted informational output is permitted. A mandatory action precondition, however, is not satisfied merely because the system failed to find contrary evidence.

An assessment also needs a precise subject. Identify the claim revision, assessed artifact or implementation revision, relevant configuration, input, representation, and assessment method as needed by that claim. A check of one file cannot silently become a check of another rendering or deployed build. A digest helps bind a record to bytes under a declared serialization and hash assumption; it does not authenticate the author, establish semantic equivalence, or show that those bytes were delivered to a recipient. Evidence may be reused only when its relationship to the new subject and scope is justified.

## 3. Justification graphs and conditional soundness

A **justification graph** contains claim nodes, premise nodes, and explicit inference applications. An inference application identifies its rule, input claims, output claim, and relevant side conditions. It may also carry a computation or verification witness. The graph is an explanation of the offered justification, not a complete record of every internal mental or computational event.

For the following result, take a finite directed acyclic derivation graph. Each leaf is a premise, and every other claim is obtained by a supported inference rule whose inputs appear earlier in a topological order. Interpret truth in one fixed domain model.

### Proposition 1. Sound rules preserve true premises in a finite derivation

If every premise is true in the model, every used rule is sound for that model when its side conditions hold, and every side condition of every inference application is satisfied in the model, every derived claim is true in that model.

**Proof.** Order the graph topologically. The initial premise nodes are true by assumption. At each subsequent node, all input claims are true by the induction hypothesis and all side conditions hold by assumption. Soundness of that rule under those conditions makes the output true. Induction covers every node. ∎

The result is conditional on premises, rule semantics, and discharged side conditions. For example, a rule that cancels a divisor cannot be used when its nonzero-divisor condition is false. The proposition does not show that the premises were correctly extracted, that the domain model is adequate, or that the implementation actually followed the rule. A computation with correctly applied arithmetic and an incorrectly read input remains an incorrect domain result.

Circular support is outside this proof. A cycle that repeats a conclusion as its own premise supplies no independent foundation. Some systems admit explicitly defined fixed-point reasoning, but they require a separate semantics and correctness argument. Finite serialization of a cycle is not that argument.

### Proposition 2. A countermodel refutes a universal claim within its scope

For a claim \(\forall x\in D, P(x)\), an admissible \(x_0\in D\) with \(\neg P(x_0)\) refutes the claim.

**Proof.** Universal quantification requires \(P\) for every element of \(D\), including \(x_0\). ∎

The domain condition matters. A failure outside the claimed domain can motivate a broader study but does not refute the narrower theorem. Conversely, narrowing the domain after seeing a failure produces a revised claim; it does not retroactively turn the original claim into a successful one.

## 4. What different checks establish

**Table 2. Evidence types and the boundary of their immediate conclusions.**

| Evidence type | What it can support within its stated conditions | What does not follow from it alone |
| --- | --- | --- |
| Structural validation | Compliance with the representation rules implemented by a correct validator | Correct interpretation of natural-language fields |
| Formal proof | A consequence of stated assumptions under specified semantics | Satisfaction of those assumptions by an implementation |
| Executable test | An observed outcome for the tested input, configuration, and oracle | Correctness on untested cases or other revisions |
| Exhaustive finite check | The checked property on a completely enumerated finite model | Coverage of an unbounded domain or a different deployment |
| Substantive review | A scoped assessment under the reviewer's sources, expertise, and rubric | Automatic independence, external peer review, or runtime conformance |
| Production observation | An actual observed behavior, failure, or cost at the recorded boundary | Causal superiority over an unmeasured alternative |

For a finite check, the carrier, enumerated values, supported operations, and tested predicate must be stated. Complete enumeration is a substantive premise, not a synonym for a large iteration count. Coverage may fail because a generator omits an input, an execution outcome, or a configuration. A correct checker applied to an incomplete enumeration cannot establish the advertised larger universal claim.

An empty domain makes a universal formula true vacuously. A test set containing no relevant negative case can likewise fail to challenge an exclusion rule. Neither observation demonstrates successful useful behavior. Record the vacuous or unexercised case separately, and include applicable positive controls when usefulness is part of the claim. Repeated copies of one test do not enlarge the distinct tested domain.

Evidence types are complementary, not a ladder on which more records always mean stronger support. Ten tests sharing an incorrect oracle can repeat one mistake. A second reading by the producer is self-review. A separate reviewer who sees the proposed answer or earlier verdict performs a non-blind review; this is not automatically the independent assessment intended by a blinded design. Describe the actual separation of information, source access, rubric, and adjudication rather than infer independence from different agent names.

For example, suppose an extracted value is wrong and both a calculation and its reference answer use that same extracted value. Their agreement can validate the calculation relative to its input while missing the source-reading error. A reference independently established from the source can expose the discrepancy. This is a constructed example of shared dependence, not a measured extraction-failure rate.

## 5. A falsification protocol

An evaluation begins by freezing the claim and requirements before examining the decisive cases. Record subject versions, admissible inputs, expected behavior, failure criteria, scope of generalization, and the treatment of uncertain cases. Also identify the reference procedure and the evidence needed to decide that a proposed counterexample belongs to the claimed domain. A later change creates a new claim or evaluation revision; it does not overwrite the earlier result.

Adversarial cases should probe both the required conditions and the system's enforcement of them. For extraction, change a referent, logical scope, or source revision. For composition, omit a jointly required ground or add a conflicting condition. For reuse, change a material dependency or current permission. For resource accounting, repeat a telemetry event or expose a shared cost counted twice. The objective is to distinguish enforcement from success on familiar positive examples.

Two uses of such cases must remain separate. A case outside a theorem's premises can show why those premises matter, but does not refute that conditional theorem. An admissible case in which an implementation wrongly asserts that a condition has passed can refute the implementation's enforcement claim. To refute the theorem itself, the case must satisfy all its premises and falsify its conclusion under the same interpretation. Failure of a premise does not prove that every result outside the premise is wrong either; it removes that particular justification.

An independent impact oracle is especially important for dependency completeness. Traversing an annotated graph can verify traversal; it cannot expose an omitted dependency when the reference answer comes from that same graph. A useful test changes a relevant source feature and separately establishes whether the output should change. Shared errors in annotation and evaluation must not be counted as independent confirmation.

Separate at least four failure classes: the model's claim is false; the implementation violates the model; the input interpretation or annotation is wrong; or the evaluation lacks enough information to decide. These classes identify different repairs. One incident can involve several defects, so assigning a single convenient label must not erase the other supported findings. Uncertain domain membership or an unverified oracle leaves the alleged refutation unresolved rather than making it a confirmed failure or success.

A refutation record should retain the exact claim revision, in-scope witness, conditions, actual output, expected relation, and enough execution or derivation information to inspect the contradiction. For a stochastic or nondeterministic implementation, state whether the claim quantifies over all permitted executions or over a distribution. One verified prohibited success contradicts a claim that such success never occurs. It does not by itself refute a different claim that permits a specified nonzero failure probability. Testing only one convenient outcome does not cover an all-executions claim.

## 6. Comparators, analysis, and stopping

A comparative claim needs a relevant baseline with matched tasks, resource accounting, and acceptance conditions. A method that produces more complete outputs at higher cost must not be described as unconditionally cheaper. Skipping required checks cannot yield an apparent speed advantage without disclosing the lost assurance. Report whether comparisons share source material, evaluator information, execution budgets, and the same meaning of an acceptable output.

The analysis plan should state the primary outcome, denominators, missing and unresolved cases, uncertainty estimates, and stopping conditions. A report must distinguish planned cases, attempted cases, interpretable outcomes, and accepted outputs. An infrastructure failure is not automatically a semantic error; excluding it without explanation can nevertheless change the practical-success denominator.

As an arithmetic illustration, two passes, one failure, and one unresolved outcome yield two passes among three resolved outcomes, but only two confirmed passes among four planned cases. If the unresolved outcome may eventually pass or fail, the final fraction on those four cases lies between one half and three quarters. This is an identification bound for that fixed ledger, not a confidence interval or an estimate for a population. Reporting the resolved-only fraction as the overall success rate changes the denominator and conceals the unresolved case.

If evaluation stops at a budget limit, identify the covered and uncovered cases and whether the planned stopping policy was followed. Selecting only successful attempts or revising the success rule after inspection creates a different evidential object from the planned evaluation. Exploratory analysis can be useful, but should be identified as exploratory rather than relabeled as a predeclared test.

Data separation also matters. Cases used to design a rule, tune a threshold, or repair an implementation are development evidence. They may later be reused as regression tests, but not called unseen evaluation. Shared sources, near-duplicates, and leaked reference annotations can make nominally separate cases dependent. Count distinct inputs, execution attempts, graph configurations, and assertions separately; their totals are not interchangeable units of evidence.

For causal or practical-effect claims, the required design is stronger than a catalog of passing controls. The [knowledge utility paper](../knowledge-utility/PAPER.md) states the intervention and attribution conditions. Observed use, user approval, or a plausible demonstration alone does not establish improved outcomes relative to a meaningful alternative.

## 7. The evidential status of this research program

The scientific results presented here are definitions, explicit conditional arguments, and countermodels. They specify what a compliant knowledge process would have to preserve. Published engineering studies provide the separate place for reproducible executions, actual observations, and their limits. A link to a study is not a declaration that every proposed experiment has been performed; the study's own methods and evidence record determine its scope.

This distinction allows a formal or methodological paper to have a complete argument while practical hypotheses remain open. Completion means that the paper states and supports its actual contribution, not that every imaginable deployment question has been settled. Conversely, removing a provisional label cannot substitute for missing evidence.

A falsifiable engineering claim must identify an implementation \(I\), its revision \(v\), a well-formed input domain \(D\), and a mandatory condition \(C\). The claim to test is

\[
\forall x\in D:\quad \neg C(x)
\Rightarrow \operatorname{Admit}(I_v,x)\ne\mathsf{success}.
\]

Here \(D\) includes validly formed negative cases; it is not prefiltered to inputs already satisfying \(C\). A single input in \(D\) that violates \(C\) and nevertheless receives successful admission refutes the claim about that implementation revision. No premise assumes that the implementation already enforces the condition. Positive controls separately test whether permitted cases can succeed, because refusal of every case would satisfy this exclusion property without showing usefulness. Semantic and practical predictions require independently interpreted or measured outcomes in addition to structural controls.

The [contract profile conformance study](../../engineering/studies/contract-profile-conformance/STUDY.md), [source transcription and uncertainty study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md), and [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) address distinct subjects. The [editorial skill pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) addresses document production. Their results should remain separate until a justified analysis explains how they combine.

## 8. Scope and shared definitions

The model does not automate the discovery of every relevant premise, guarantee the trustworthiness of a reviewer, or establish universal usefulness of structured knowledge. It makes these dependencies inspectable and supplies conditions under which a particular claim can be rejected, retained, or narrowed.

The shared [glossary](../../reference/glossary/GLOSSARY.md) defines evidence, verification, authority, and related terms. [Revision and governance](../revision-and-governance/PAPER.md) specifies how new evidence changes assessments without erasing their history.

## 9. Conclusion

A result supports a claim only through an explicit relationship among its subject, interpretation, assumptions, assessment procedure, and scope. Provenance, fidelity, support, applicability, and authority are distinct questions. A positive structural receipt cannot stand in for all of them.

The two propositions give conditional deductive boundaries. A finite acyclic derivation preserves truth when its premises, rules, and side conditions satisfy the stated assumptions. An admissible countermodel refutes a universal claim within its domain. Neither result discovers missing premises, authenticates observations, or establishes that a deployed system follows the model. Finite checks, substantive reviews, and practical comparisons therefore require their own precisely bounded records.

The practical method is to preserve exact subjects and adverse results, separate missing evidence from negative evidence, test the relevant boundary with a defensible oracle, and retain revisions when a claim changes. Completion of a bounded argument does not require every future experiment to finish. It does require that unmeasured benefits, unchecked implementations, and unresolved cases remain visible rather than being converted into an overall success label.

## References

1. Hoare, C. A. R. “An Axiomatic Basis for Computer Programming.” *Communications of the ACM* 12(10), 1969, 576–580, 583. <https://doi.org/10.1145/363235.363259>
2. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
