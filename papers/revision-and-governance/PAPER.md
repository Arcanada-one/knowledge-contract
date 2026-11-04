---
name: "revision-and-governance"
title: "Knowledge Revision, Version Identity, and the Adoption of Norms"
artifact: "scientific-paper"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Separate identities for content, assessment and normative adoption, with explicit revision and publication decisions."
---

# Knowledge Revision, Version Identity, and the Adoption of Norms

**Author:** Pavel Valentov · **Publication edition:** 1.0

## Abstract

Knowledge can change because its content is corrected, its evidence is reassessed, its use conditions change, or a community adopts a different rule. These changes should not be represented by one undifferentiated status. This paper separates object identity, content revision, representation, assessment, and normative adoption. It defines revision and admission operations, establishes conditional properties of pinned references and dependency-based reassessment, and explains why the adoption of a norm does not establish the truth of the claims it contains. A central distinction is between reproducing a historical state and authorizing a present use. The contribution is an explicit account of what changes, what remains attributable, and which previous checks can legitimately transfer. The account is suitable for finite implementation and counterexample testing, but does not establish complete dependency discovery, authenticated authority, or a universally correct governance policy.

**Keywords:** knowledge revision; provenance; versioning; governance; normative adoption; historical reproducibility.

## 1. Research question

A knowledge repository often uses “current,” “approved,” or “valid” as if each described one property. In practice, a record can be the latest revision while being disputed, an approved policy can contain a factual error, and a historical version can remain necessary for reproducing an old result.

Our question is: **how can a system revise knowledge and adopt norms without confusing content, evidence, and authority?** We propose distinct objects and transition rules for each. The purpose is not to freeze knowledge, but to preserve a clear explanation of why a particular revision or assessment was used at a particular time.

PROV-DM offers the general distinction between entities, activities, and responsible agents [1]. We use that structure to connect revisions and decisions. The additional contribution is a set of obligations for transferring checks, following current versions, retaining historical grounds, and admitting normative decisions.

## 2. Five different objects of change

An **identity** groups revisions treated as versions of one object under a declared identity policy. The policy matters: a correction, a translation, a derived summary, and a competing interpretation need not all be revisions of the same object.

A **content revision** is a pinned content state. Material content changes create a new revision with a relation to its predecessor. Immutability here is a property of the repository's version discipline, not a guarantee supplied by writing a revision label.

A **representation** is a delivery or serialization of content: a document rendering, machine format, or other declared form. Two representations may preserve selected content while differing in accessibility or layout. Equivalence requires an appropriate preservation check; a shared title is insufficient.

An **assessment** concerns a proposition about a revision: whether it is supported, applicable, conflicted, current for a purpose, or compliant with a rule. New evidence can change an assessment without changing the assessed text. Overwriting the text to reflect every assessment change would confuse the object with judgments about it.

A **normative adoption** is a decision to use a rule within a named community, process, or jurisdiction. It identifies the decision maker, authority basis, scope, effective period, adopted revision, and review or withdrawal conditions. Adoption makes the rule operative under that policy; it does not make every factual premise of the rule true.

These distinctions permit a corrected revision and a withdrawn assessment to coexist with an earlier historical record. They also prevent unrelated properties—such as popularity, technical availability, or a successful build—from acting as substitutes for adoption or evidential support.

## 3. Revision operations and their grounds

A revision operation records the affected object, motivating evidence or request, proposed change, relevant dependencies, decision, and resulting revisions or assessments. A useful operation can correct a transcription, replace a false premise, narrow an applicability condition, add a competing interpretation, or change a normative decision.

Not every conflict should be resolved by replacing one statement. The conflict may concern different dates, referents, scopes, or interpretations. Preserving those distinctions can dissolve an apparent contradiction without declaring either source universally correct. If the conflict remains unresolved, the system should retain that assessment and avoid presenting one branch as established merely because it is newer.

Checks attach to a revision and an assessment scope. A successful check of an old text is not automatically a successful check of a materially changed text. Transfer requires a reason: the checked property is unaffected by the change, the transformation preserves it, or the check has been repeated. The reason should be inspectable rather than inferred from a similar filename.

Duplicate detection is likewise scoped. Equivalent content can be consolidated while retaining multiple provenance relations. Merging identities without a justified identity policy can destroy distinctions between independent sources, conflicting readings, or separate normative authorities.

## 4. Conditional properties

### Proposition 1. Pinned references preserve historical selection

Suppose a reference names an immutable revision, and retrieval either returns that exact revision or reports failure. Changing the repository's current-revision pointer does not change the content selected by that reference.

**Proof.** Selection depends on the named revision, not on the current pointer. The pointer change therefore cannot alter the selected identifier or its immutable content. ∎

This property requires storage integrity and exact reference resolution. A readable label or hash field alone does not ensure either. It also guarantees selection, not perpetual availability, current applicability, or permission to disclose the historical content.

### Proposition 2. Checks transfer through preserved complete inputs

Let a deterministic check \(f\) depend on a complete input tuple \(d\). If two revisions and their evaluation contexts induce the same tuple, then the check returns the same result for both.

**Proof.** Determinism gives equal outputs for equal complete inputs. ∎

The word “complete” is decisive. A check that depends on a policy version, current authorization, or a source interpretation cannot be transferred using only equality of visible text. If the evaluator itself changes, the equality-of-function assumption must also be reconsidered.

### Proposition 3. Material changes require reassessment along complete dependencies

If every dependency relevant to an assessment is represented in a finite graph, complete reverse reachability from a changed dependency identifies all assessments potentially affected by that change.

**Proof.** A relevant dependency gives a finite path from the assessment to the changed object. Reversal makes the assessment reachable from the change. Complete traversal includes every such path. ∎

This result identifies candidates for reassessment, not automatic failures. An assessment may remain valid because an alternative ground still suffices. Conversely, a missing edge can hide an affected assessment despite a correct traversal algorithm.

### Proposition 4. Adoption is not a truth-preserving inference rule

Without an additional premise connecting an adoption procedure to truth, the fact that a rule is adopted does not logically entail the truth of its factual content.

**Argument.** Consider two interpretations with the same recorded adoption event, one in which the factual content is true and another in which it is false. Both satisfy the adoption record. The content therefore is not a consequence of that record alone. ∎

This does not deny the practical force of adopted rules. It locates that force in the declared governance policy rather than in an unsupported epistemic inference.

## 5. Authority and normative admission

A governance policy defines who may propose, review, adopt, amend, or withdraw a norm, under which conditions. Those are different permissions. A role description can explain responsibility without granting every operation associated with the role.

Admission should evaluate current authority, the applicable procedure, the exact proposed revision, required reviews, unresolved conflicts, and any effective-date conditions. When a condition is mandatory, unknown is not pass. A record that says a reviewer approved something must be connected to the correct subject and a trustworthy attribution mechanism; a field named “reviewer” cannot authenticate itself.

The model does not prescribe one decision rule for every community. A maintainer decision, a quorum, or an external mandate can each be represented, provided the rule and its scope are explicit. The research obligation is to state what the procedure establishes and what it leaves unproven.

An appeal or correction creates a new event rather than erasing the earlier decision. This permits analysis of why an earlier output was produced and how the current basis differs. Accountability requires that history remain inspectable under the applicable retention and access rules; it does not require unrestricted public disclosure of every underlying record.

## 6. Historical reproduction and current use

Historical reproduction asks what followed from a pinned state and policy. Current use asks whether the result is admissible now. These can have different answers. A historical computation may remain reproducible even when its source has been superseded. A current recommendation may require reassessment despite exact reproduction of the earlier computation.

Time therefore has several meanings: when an event occurred, when it was recorded, when a rule became effective, and when a use is being admitted. Collapsing them into one timestamp makes delayed information and retrospective correction difficult to represent correctly.

Likewise, storage retention, publication status, and use eligibility are distinct. An artifact can remain archived while current use is withdrawn. Removing it from search results does not erase all copies. Retaining an original for reproducibility does not grant permission to use it in a new context. Each transition should identify its intended effect.

Migration between representations introduces another preservation question. A migration report should state what is mapped, what is transformed with checked preservation, what is intentionally omitted, and what cannot be represented. A successful import is not evidence of semantic equivalence if critical distinctions were collapsed.

## 7. Falsification and evidence boundary

The model can be tested with cases that change one material feature: a source revision, authority grant, effective date, interpretation rule, or mandatory dependency. It should also include unchanged content with a changed assessment, and changed layout with preserved content but impaired delivery.

Counterexamples are particularly useful where identifiers conceal assumptions. Reusing a prior receipt after a policy change tests whether the receipt is wrongly treated as permanent permission. Updating a current pointer while resolving a pinned reference tests historical selection. Merging two textually equal records with different provenance tests whether deduplication destroys relevant history.

These controls can establish behavior on finite represented cases. They do not prove complete dependency discovery, correct interpretation of all governance rules, or trustworthy authentication in an unexamined deployment. The formal propositions remain conditional on those boundaries.

The contribution is a complete account of the distinctions needed to reason about revision and adoption, together with checkable consequences and counterexamples. It makes no empirical claim that one governance procedure is universally superior or that the model resolves substantive disagreement automatically.

## 8. Connections to the published engineering work

The [executable projections and revision study](../../engineering/studies/executable-projections-and-revision/STUDY.md) concerns pinned revisions and bounded update behavior. The [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) examines current eligibility of previously prepared artifacts.

The shared [glossary](../../reference/glossary/GLOSSARY.md), [interaction and memory](../interaction-and-memory/PAPER.md), and [controlled knowledge reuse](../controlled-knowledge-reuse/PAPER.md) define the connected work-state and admission obligations.

## References

1. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
