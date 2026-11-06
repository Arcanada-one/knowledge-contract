---
name: "semantic-objects-and-context"
title: "Semantic Objects, Context, and Conditions of Applicability"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "A formal account of source interpretations, context, mandatory dependencies and conditions of applicability."
---

# Semantic Objects, Context, and Conditions of Applicability

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

Faithful extraction does not by itself establish that source content is true or suitable for a task. This paper asks which distinctions a knowledge system must preserve between source material and its use. We define a versioned semantic object with attributable content, explicit context, and inspectable grounds, and define certified applicability relative to declared requirements and assessments. Five elementary conditional results characterize the model: fidelity alone cannot distinguish truth across observationally identical worlds; a finite dependency graph has a least required closure; mandatory strengthening narrows certified applicability; additional readings narrow common consequences; and complete backward slicing preserves selected deterministic outputs. Counterexamples delimit those results: a computed closure may omit an unrecorded exception, a retained quotation may be false, and a representation may lose the scope of a negation or obligation. The contribution is an integrated account of the obligations between extraction and use, not a new general theory of meaning. The method is deductive; the empirical question of whether an interpreter supplies complete and correct representations remains separate. Published engineering studies provide bounded transcription and dependency evidence, not a demonstration of complete semantic extraction.

**Keywords:** semantic object; provenance; context; applicability; interpretation; dependency closure.

## 1. Research question and contribution

An accurately reproduced quotation can contain a false assertion. A true statement can be irrelevant to a task. Identical sentences can concern different objects, dates, or obligations. Text and a single confidence score do not distinguish these cases unless the system assigns incompatible meanings to the same field.

Our question is: **what must remain explicit when source material becomes knowledge offered for a particular task?** We separate five questions. What representation was inspected? How was it interpreted? What grounds support that interpretation? Which requirements govern its proposed use? What material actually reaches the recipient? A favorable answer to one question does not settle the others.

The contribution is the organization of these obligations and their failure conditions. The semantic-object record connects attribution and context to inspectable grounds. The applicability definition makes mandatory conditions and justified exemptions explicit. The conditional results identify what follows from those definitions and what still requires independent evidence. They are elementary results, not a claim to a new general theory of meaning or a new extraction algorithm.

The method is deductive. Sections 2 and 3 define the objects and certification rule. Section 4 states five propositions with their assumptions, proofs, and limits. Sections 5 and 6 examine granularity, delivery, and empirical evaluation; Section 7 identifies the narrower questions addressed by the published engineering studies. The proofs do not establish that an extraction process meets their premises.

The model complements established work. W3C PROV-DM describes provenance through entities, activities, and agents [1]. SKOS provides concepts, labels, and relations for knowledge organization [2]. A provenance link or concept label does not, by itself, establish a proposition's truth or suitability for a task. The question addressed here is what additional conditions must hold before an interpretation may support a particular use.

## 2. Objects, interpretations, and grounds

A **source representation** is a particular version of material: text, image, table, audio, or a combination. A locator identifies a region within that representation. A locator can make inspection repeatable; it does not certify the correctness of the region's interpretation.

A **semantic object** is a record

\[
o=(i,v,m,A,C,G),
\]

where \(i\) is identity, \(v\) is revision, \(m\) is the represented content, \(A\) is attribution, \(C\) is context, and \(G\) is a set of grounds and dependency relations.

The represented content may be a proposition, question, instruction, constraint, example, or another declared content role. That role describes what the record represents; it is not an epistemic verdict. Recording an instruction does not establish its legitimacy. Recording an example does not establish a universal rule.

An **interpretation** maps a source region to a semantic-object record under declared reading assumptions. It may remain uncertain or admit several readings. When a diagram permits two readings, the record can retain both and identify the observations needed to resolve them. Silently choosing one changes the knowledge claim rather than merely simplifying its presentation.

**Grounding** identifies why a particular part of the interpretation is supported. A source may support that an author asserted \(P\), while an independent measurement supports \(P\) itself. These are different grounds. We therefore distinguish

\[
\operatorname{Says}(a,P) \quad\text{and}\quad P.
\]

The first does not entail the second without additional premises about the source and the relevant domain. Faithful attribution and truth therefore require different justifications.

Co-occurrence is not an implication either. Two statements appearing in the same paragraph do not acquire a causal or logical relation merely through their proximity.

Extraction must preserve logical structure when it matters. For a domain with two objects, one satisfying \(P\) and one not, “not every object satisfies \(P\)” is true while “every object fails \(P\)” is false. Similarly, absence of an obligation to act is different from an obligation not to act. A semantic representation that merges these distinctions changes the claim even if it preserves most words.

## 3. Context and applicability

Context serves six distinct functions in this model.

**Table 1. Context roles and the information they identify.**

| Context role | Relevant information |
| --- | --- |
| Source | Terminology, referents, and local legends in the source. |
| Extraction | The inspected representation and unresolved details. |
| Request | Intent, completeness requirements, and budget. |
| Recipient | Usable forms and modalities. |
| Situation | Target object, time, and reference frame. |
| Intended action | What is to be explained, compared, computed, or executed. |

These are functional roles, not six required copies of the same value. One linked value may serve several roles. The representation must nevertheless distinguish conditions attached to the source from conditions governing the intended target use.

Let a use request be \(q\), a relevant state be \(s\), and the finite declared mandatory conditions be \(R(q)\). Each condition has an assessment

\[
e_r(o,q,s)\in\{\mathsf{pass},\mathsf{fail},\mathsf{unknown},\mathsf{not\_applicable}\}.
\]

A condition is **discharged** when it passes, or when a justified applicability rule establishes that it imposes no obligation in the exact assessed scope. Write \(w_r(o,q,s)\) for the validity of that rule application and its supporting witness. Then

\[
\operatorname{Discharged}_r(o,q,s)
\iff e_r(o,q,s)=\mathsf{pass}
\ \lor\ \bigl(e_r(o,q,s)=\mathsf{not\_applicable}\land w_r(o,q,s)\bigr).
\]

The witness identifies the rule, its grounds, and the subject and scope to which it applies. A bare `not_applicable` label is insufficient. Certified applicability is

\[
\operatorname{Applicable}(o,q,s)
\iff \forall r\in R(q),\ \operatorname{Discharged}_r(o,q,s).
\]

This definition uses the same four assessment values as the [status model](../../engineering/specifications/status-model/SPECIFICATION.md). It does not treat unknown as pass or allow an unsupported exemption. It also does not equate failure to certify with proof that the content is false. An unanswered question about a relevant date may block a current recommendation while leaving the underlying statement unresolved.

Certification is only as strong as the completeness and correctness of the declared conditions, assessments, and exemption rules. If \(R(q)=\varnothing\), the displayed quantification is vacuously true; it does not establish that the request had no material obligations. Using certification to justify a consequential use therefore requires a separate justification that the requirement set covers that use.

Conditions can be inherited only through a declared rule. A section-level exception may apply to its paragraphs, but arbitrary proximity does not establish inheritance. Conflicting conditions require an explicit conflict decision or a restricted answer. A system must not select whichever condition produces a convenient result.

The request determines the necessary depth. A short identification question may require fewer dependencies than an instruction to execute a consequential action. Increasing depth can create new obligations; it is not merely a demand for a longer response. Applicability must also be checked for the actual recipient and delivered representation. A condition available to the system but absent from the delivered instructions may not protect the recipient.

## 4. Conditional results

### Proposition 1. Fidelity cannot discriminate indistinguishable worlds

Suppose two possible worlds produce the same observed source representation, while \(P\) is true in one and false in the other. Any deterministic procedure using only that representation produces the same decision in both worlds. It therefore cannot correctly decide the truth of \(P\) in both.

**Proof.** The procedure receives identical inputs, so its outputs coincide. The correct truth verdicts differ. Hence at least one verdict is incorrect if the procedure returns a definite truth value. A randomized procedure has the same output distribution in both worlds and likewise receives no discriminating evidence. ∎

This result does not make sources useless. It identifies the extra premise needed to move from faithful attribution to a truth claim: a reliable domain model, independent observation, or another justified discriminating ground.

### Proposition 2. Least required closure exists on a finite graph

Let \(V\) be a finite set of pinned object revisions, \(\mathit{Roots}\subseteq V\) selected roots, and \(D_q\subseteq V\times V\) the active mandatory dependencies for a fixed request. Define

\[
C_0=\mathit{Roots},\qquad
C_{n+1}=C_n\cup\{v:\exists u\in C_n,(u,v)\in D_q\}.
\]

Then the sequence reaches a fixed point \(C^*\), which is the least \(D_q\)-closed set containing \(\mathit{Roots}\).

**Proof.** The sequence is increasing and contained in finite \(V\), so only finitely many strict additions are possible. Its fixed point is closed by construction. For any closed set \(S\) containing \(\mathit{Roots}\), induction gives \(C_n\subseteq S\) for every \(n\). Thus \(C^*\subseteq S\). ∎

Cycles do not invalidate this set-theoretic result. The [tested engineering profile](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) rejects cycles; its executable evidence therefore covers the acyclic profile, while the cyclic case here is supported by the proof. Missing edges invalidate an interpretation of computed closure as semantic completeness: a perfectly computed closure can still omit an unrecorded exception.

“Least” is relative to the declared vertices and edges. The [projection study's counterexample](../../engineering/studies/executable-projections-and-revision/STUDY.md#counterexample-to-claim-level-minimality) shows that a least entity closure can still carry unnecessary claims inside a shared qualification. The proposition establishes neither claim-level minimality nor a smallest token budget.

### Proposition 3. Mandatory strengthening narrows certified applicability

Let \(R\subseteq R'\), and keep the assessments, exemption witnesses, and discharge semantics of shared conditions unchanged. Every object certified under \(R'\) is certified under \(R\).

**Proof.** Discharging every condition in \(R'\) entails discharging every condition in its subset \(R\). ∎

The fixed-semantics condition matters. If adding a requirement also changes the meaning of an earlier one, the comparison is no longer a simple strengthening.

### Proposition 4. Additional readings narrow common consequences

For a nonempty set of possible readings \(I\), let \(K(I)=\bigcap_{i\in I}\operatorname{Conseq}(i)\), with a fixed consequence relation. If \(I\subseteq I'\), then \(K(I')\subseteq K(I)\).

**Proof.** Membership in the intersection over \(I'\) requires membership in every set indexed by \(I\), as well as any additional sets. ∎

This supports conservative reporting under ambiguity. It does not establish that the recorded readings include the correct one, or that the consequence relation is sound for the domain.

### Proposition 5. A complete backward slice preserves selected deterministic outputs

Let a finite acyclic computation graph have fixed deterministic node functions and fixed input values. Retain the selected output nodes and every node on which they depend. Evaluating that retained graph gives the same selected outputs as evaluating the full graph.

**Proof.** Order the retained graph topologically. Retained input nodes have unchanged values. Every later retained node has all its predecessors retained and, by induction, receives their unchanged values. Its fixed function therefore returns the same value. This includes the selected outputs. ∎

The result concerns complete computational dependencies. Hidden inputs, changing functions, omitted edges, or an inadequate model of the original task defeat its premises. It is a restricted acyclic instance of the behavior-preservation obligation studied in program slicing [3], not a new slicing algorithm. Applying that obligation to knowledge additionally requires a justified interpretation and task scope; the result does not prove that an arbitrary textual summary preserves meaning.

## 5. Granularity, identity, and delivery

A semantic object has no task-independent ideal size. A large unit may hide an exception; a tiny unit may detach a predicate from its scope. Decomposition is useful when it permits independent revision and inspection without losing mandatory connections. Its adequacy depends on reconstruction and use obligations, not on a preferred word count.

Identity, equivalent content, and interchangeable use answer different questions. Records with equivalent claims may have different provenance. Revisions of one record may differ on a critical condition. Objects interchangeable for one question may be distinguishable for another. Deduplication should therefore preserve the provenance that supports or qualifies members of a verified content class.

Delivery must be checked separately. Keeping an image identifier does not establish that the recipient received a readable image. Alternative text may omit a visual relation needed by the task. The delivered package must include or expose the relevant material at a usable resolution, together with the necessary legend or interpretation. Naming a multimodal field does not establish that these engineering conditions were met.

## 6. Falsification and scope of evidence

The propositions concern declared representations under stated premises. A separate empirical question is whether an extraction process supplies the correct representations and dependencies. Testing that process requires independently prepared cases and adjudication rules. The evaluation should distinguish transcription error, attribution error, logical-scope error, omitted context, and unsupported inference. A single aggregate accuracy score can conceal these different failure mechanisms.

Test cases should include unchanged wording with a changed referent, an exception outside the extracted region, an ambiguous visual mark, and a correct quotation of a false assertion. Independent reference annotations should specify permissible alternative readings. Agreement between two outputs is insufficient when both inherit the same omitted condition.

An omitted dependency can invalidate a system's claim to semantic completeness even when its closure computation is correct. Such a case challenges the completeness of the represented dependencies; it does not refute the conditional closure result for the graph actually declared. The same distinction applies when an implementation fails another proposition's premises. A counterexample to a conditional proposition must satisfy its premises and contradict its conclusion.

This article establishes the stated conditional properties and makes extraction obligations explicit enough to assess. It reports no measured superiority of a model, annotation process, or user interface. Executable examples can test compliance on finite inputs, but cannot establish complete interpretation of unrestricted language or images. The published observations and their untested boundaries are identified next.

## 7. Connections to the published engineering work

The [source transcription and uncertainty study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) demonstrates that a reproducible projection can omit recorded uncertainty, and reports a correction that preserves that field. It does not evaluate plural interpretations or the correctness of source locators. Those extraction obligations remain untested by the published studies. The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) separates fixed-graph closure from historical delivery checks; it does not establish that the graph contains every semantic dependency.

Definitions shared across the project are indexed in the [glossary](../../reference/glossary/GLOSSARY.md). The next scientific steps are [constrained transformations](../constrained-transformations/PAPER.md) and [retrieval and context composition](../retrieval-and-context-composition/PAPER.md), which use the applicability and dependency obligations defined here.

## 8. Conclusion

Source fidelity, supported interpretation, certified applicability, and successful delivery are distinct obligations. The semantic-object record makes attribution, context, and grounds inspectable; the applicability rule asks whether each declared mandatory condition has passed or has a justified exemption in the assessed scope. Neither a locator nor a confidence label settles those questions on its own.

The five propositions describe conditional guarantees, not automatic extraction capabilities. Least closure is relative to a declared graph. Strengthening requires unchanged assessments and discharge semantics. Common consequences depend on the recorded readings and consequence relation. Backward slicing requires complete dependencies, fixed inputs, and deterministic functions on an acyclic graph. Fidelity alone cannot discriminate worlds that present the same source evidence but differ in truth.

The remaining empirical obligation is to justify the representations, dependencies, assessments, and delivery on which a proposed use relies. Unknown conditions must not be reported as satisfied, and an empty requirement set must not be mistaken for evidence that no obligation exists. The model supplies a disciplined account of those obligations; it does not certify unrestricted interpretation or establish a performance advantage.

## References

1. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
2. W3C. *SKOS Simple Knowledge Organization System Reference*. W3C Recommendation, 2009. <https://www.w3.org/TR/skos-reference/>
3. Weiser, M. “Program Slicing.” *IEEE Transactions on Software Engineering* SE-10(4), 1984, 352–357. [Original article](https://faculty.cc.gatech.edu/~harrold/6340/cs6340_fall2009/Readings/Weiser.Slicing.TSE.pdf).
