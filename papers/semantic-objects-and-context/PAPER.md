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

A knowledge system must distinguish what a source contains, how that content is interpreted, and whether an interpretation supports a particular use. This paper specifies a model that keeps those questions separate. Its basic unit is a versioned semantic object with an attributable interpretation, explicit context, and inspectable grounds. Applicability is a decision relative to declared requirements, rather than a permanent property of a passage. We establish five elementary conditional results: source fidelity does not establish truth; a finite dependency graph has a least required closure; mandatory strengthening narrows certified applicability; additional possible readings narrow common consequences; and complete backward slicing preserves selected deterministic outputs. Counterexamples show why omitted dependencies, ambiguous scope, and unexamined modal distinctions defeat stronger conclusions. These are properties of the stated model, not a proof that an interpreter extracts all relevant meaning. The contribution is an integrated, falsifiable account of the obligations between extraction and use. Reproducible transcription and dependency studies are published separately from the scientific argument.

**Keywords:** semantic object; provenance; context; applicability; interpretation; dependency closure.

## 1. Research question and contribution

An accurate quotation can be false. A true statement can be irrelevant to a task. Two identical sentences can concern different objects, dates, or obligations. A system that stores only text and a confidence score cannot express these differences without assigning several incompatible meanings to the same field.

Our question is: **what must remain explicit when source material becomes knowledge offered for a particular task?** We propose a separation between source representation, interpretation, grounding, applicability, and delivery. The contribution is the organization of these obligations and the identification of their failure conditions. The mathematical results below are elementary consequences of the definitions; we do not claim a new general theory of meaning.

The model complements established work. W3C PROV-DM describes provenance through entities, activities, and agents [1]. SKOS provides concepts, labels, and relations for knowledge organization [2]. Neither a provenance link nor a concept label is, by itself, evidence that a proposition is true or applicable. We use those distinctions while adding a task-relative admission question: what has to hold before this interpretation may support this use?

## 2. Objects, interpretations, and grounds

A **source representation** is a particular version of material: text, image, table, audio, or a combination. A locator identifies a region within that representation. A locator can make inspection repeatable; it does not certify the correctness of the region's interpretation.

A **semantic object** is a record

\[
o=(i,v,m,A,C,G),
\]

where \(i\) is identity, \(v\) is revision, \(m\) is the represented content, \(A\) is attribution, \(C\) is context, and \(G\) is a set of grounds and dependency relations. Content may represent a proposition, question, instruction, constraint, example, or another declared role. A role is not an epistemic verdict: recording an instruction does not establish its legitimacy, and recording an example does not establish a universal rule.

An **interpretation** maps a source region to such a record under declared reading assumptions. Interpretation can be uncertain or plural. If a diagram permits two readings, the record can retain both, with the observations needed to resolve them. Choosing one silently changes the knowledge claim.

**Grounding** identifies why a particular part of the interpretation is supported. A source may support that an author asserted \(P\), while an independent measurement supports \(P\) itself. These are different grounds. We therefore distinguish

\[
\operatorname{Says}(a,P) \quad\text{and}\quad P.
\]

There is no inference from the first to the second without additional premises about the source and the relevant domain. Co-occurrence is likewise not an implication: placing two statements in one paragraph does not establish a causal or logical relation between them.

Extraction must preserve logical structure when it matters. For a domain with two objects, one satisfying \(P\) and one not, “not every object satisfies \(P\)” is true while “every object fails \(P\)” is false. Similarly, absence of an obligation to act is different from an obligation not to act. A semantic representation that merges these distinctions changes the claim even if it preserves most words.

## 3. Context and applicability

We distinguish six context roles: source context, including terminology, referents, and local legends; extraction context, including the inspected representation and unresolved details; request context, including intent, completeness requirements, and budget; recipient context, including usable forms and modalities; situation context, including the target object, time, and reference frame; and intended-action context, specifying what is to be explained, compared, computed, or executed. These are functional roles, not a requirement to duplicate a value in six places. A single linked value can serve several roles, while source conditions and target conditions remain distinguishable.

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

There is no task-independent ideal size for a semantic object. A large unit may hide an exception; a tiny unit may detach a predicate from its scope. A useful decomposition exposes independent revision and inspection while retaining explicit mandatory connections. Granularity is therefore evaluated against reconstruction and use obligations, not by a preferred number of words.

Identity, equivalent content, and interchangeable use must also remain separate. Two records can contain equivalent claims but have different provenance. Two revisions of one record can differ on a critical condition. Two objects interchangeable for one question can be distinguishable for another. Deduplication should consolidate a verified content class without discarding the provenance that supports or qualifies its members.

Delivery creates a further obligation. A preserved image identifier does not guarantee that a recipient receives a readable image; alternative text does not necessarily preserve a visual relation needed by the task. The delivered package must include or expose the relevant material at a usable resolution and with the necessary legend or interpretation. These are inspectable engineering conditions, not consequences of naming a multimodal field.

## 6. Falsification and scope of evidence

The propositions establish properties of declared representations. The harder empirical question is whether an extraction process supplies the right representations and dependencies. That question requires independently prepared cases and adjudication rules. A useful evaluation distinguishes transcription error, attribution error, logical-scope error, omitted context, and unsupported inference. A single aggregate accuracy score hides these different failure mechanisms.

Counterexamples should include a changed referent with unchanged wording, an exception outside the extracted region, an ambiguous visual mark, and a correct quotation of a false assertion. An independent reference annotation should specify what counts as a permissible alternative reading. Agreement between two outputs is insufficient when both inherit the same omitted condition.

This article establishes the stated conditional properties and a falsifiable specification of extraction obligations. It reports no measured superiority of a particular model, annotation process, or user interface. Executable examples can test compliance on finite inputs; they cannot prove complete interpretation of unrestricted language or images.

## 7. Connections to the published engineering work

The [source transcription and uncertainty study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) demonstrates that a reproducible projection can omit recorded uncertainty, and reports a correction that preserves that field. It does not evaluate plural interpretations or the correctness of source locators. Those extraction obligations remain untested by the published studies. The [dependency closure and package delivery study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) separates fixed-graph closure from historical delivery checks; it does not establish that the graph contains every semantic dependency.

Definitions shared across the project are indexed in the [glossary](../../reference/glossary/GLOSSARY.md). The next scientific steps are [constrained transformations](../constrained-transformations/PAPER.md) and [retrieval and context composition](../retrieval-and-context-composition/PAPER.md), which use the applicability and dependency obligations defined here.

## References

1. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
2. W3C. *SKOS Simple Knowledge Organization System Reference*. W3C Recommendation, 2009. <https://www.w3.org/TR/skos-reference/>
3. Weiser, M. “Program Slicing.” *IEEE Transactions on Software Engineering* SE-10(4), 1984, 352–357. [Original article](https://faculty.cc.gatech.edu/~harrold/6340/cs6340_fall2009/Readings/Weiser.Slicing.TSE.pdf).
