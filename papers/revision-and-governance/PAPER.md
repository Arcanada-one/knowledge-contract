---
name: "revision-and-governance"
title: "Knowledge Revision: Version Identity, and the Adoption of Norms"
short_title: "Knowledge Revision"
subtitle: "Version Identity, and the Adoption of Norms"
previous_title: "Knowledge Revision, Version Identity, and the Adoption of Norms"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Separate identities for content, assessment and normative adoption, with explicit revision and publication decisions."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="knowledge-revision-version-identity-and-the-adoption-of-norms"></a>

# Knowledge Revision: Version Identity, and the Adoption of Norms

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

A knowledge record can be corrected, reassessed, rendered differently, or adopted as a rule. Treating these events as one change of status obscures which claims and permissions remain justified. This paper asks how knowledge revision can preserve that distinction. We separate object identity, content revision, representation, assessment, and normative adoption. Four conditional propositions concern exact historical selection, equal results from deterministic checks with equal complete inputs, dependency-based identification of reassessment candidates, and the non-entailment of contingent factual claims by adoption alone. The method is deductive, supplemented by constructed boundary cases rather than deployment measurements. The contribution is a bounded account of the obligations for transferring checks and admitting current use, not a new truth-maintenance algorithm or a realization of AGM belief revision. In particular, reproducing a check result does not establish the check's soundness, and identifying an affected assessment does not establish its failure. Complete dependency discovery, reliable authentication, retention in a deployed system, and the comparative effectiveness of a governance policy remain separate obligations.

**Keywords:** knowledge revision; provenance; versioning; governance; normative adoption; historical reproducibility.

## 1. Research question

A knowledge repository often uses “current,” “approved,” or “valid” as if each described one property. In practice, a record can be the latest revision while being disputed, an approved policy can contain a factual error, and a historical version can remain necessary for reproducing an old result.

Our question is: **how can a system revise knowledge and adopt norms without confusing content, evidence, and authority?** We propose distinct objects and transition rules for each. The purpose is not to freeze knowledge, but to preserve a clear explanation of why a particular revision or assessment was used at a particular time.

PROV-DM offers the general distinction between entities, activities, and responsible agents [1]. We use that structure to connect revisions and decisions. The additional contribution is a set of obligations for transferring checks, following current versions, retaining historical grounds, and admitting normative decisions.

Dependency-directed revision has an established basis in Doyle's truth-maintenance work, which records reasons for beliefs and revises them when assumptions change [2]. The reachability result below isolates an elementary prerequisite for identifying affected assessments; it does not implement a truth-maintenance system. Alchourrón, Gärdenfors, and Makinson study contraction and revision of logical theories under explicit postulates [3]. Our use of “revision” concerns versioned records, assessments, and authority decisions, and claims neither an AGM revision operator nor satisfaction of those postulates.

### 1.1 Method and contribution boundary

The argument proceeds by definitions, explicit premises, and their consequences. The four propositions isolate elementary obligations; their short proofs should not be read as novel results about arbitrary belief systems. Constructed cases expose what stops following when a premise is removed. Neither those cases nor a mechanically checked document establish an implemented governance mechanism.

The references perform different jobs. PROV-DM specifies provenance relations; its revision relation is a specialized derivation, not a proof that a revision is correct [1, Section 5.2.2]. Doyle supplies the prior problem of maintaining reasons for beliefs [2]. AGM supplies formal contraction and revision of theories with a consequence operation and stated postulates [3, Sections 1–2]. A versioned collection of documents is not, merely by being versioned, a deductively closed theory equipped with those operations. Connecting this account to an AGM operator would require an explicit representation, operation correspondence, and proof of the relevant postulates. None is assumed here.

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

### 3.1 A scoped transfer obligation

A transfer record should identify the old and new subjects, the selected property, the evaluator and its interpretation, the relevant context, and the grounds for treating the inputs as complete. This is an explanatory obligation, not a new machine schema. Content equality can discharge only those comparisons for which content is the entire relevant input. Changes of policy, recipient, time interpretation, or evaluator can leave the text unchanged while invalidating that justification.

Proposition 2 concerns equality of check results. A deterministic checker that always returns success also repeats its answer on equal inputs. That fact does not make the answer sound. Using the result as evidence for a property requires a separate justification of the checker for that property and scope. Permission to use or disclose the result requires its own current decision.

## 4. Conditional properties

### Proposition 1. Pinned references preserve historical selection

Suppose a reference names an immutable revision, and retrieval either returns that exact revision or reports failure. Changing the repository's current-revision pointer does not change the content selected by that reference.

**Proof.** Selection depends on the named revision, not on the current pointer. The pointer change therefore cannot alter the selected identifier or its immutable content. ∎

This property requires storage integrity and exact reference resolution. A readable label or hash field alone does not ensure either. It also guarantees selection, not perpetual availability, current applicability, or permission to disclose the historical content.

### Proposition 2. Checks transfer through preserved complete inputs

Let a deterministic check \(f\) depend on a complete input tuple \(d\). If two revisions and their evaluation contexts induce the same tuple, then the check returns the same result for both.

**Proof.** Determinism gives equal outputs for equal complete inputs. ∎

The word “complete” is decisive. A check that depends on a policy version, current authorization, or a source interpretation cannot be transferred using only equality of visible text. If the evaluator itself changes, the equality-of-function assumption must also be reconsidered.

### Proposition 3. Complete dependencies identify candidates for reassessment

If every dependency relevant to an assessment is represented in a finite graph, complete reverse reachability from a changed dependency identifies all assessments potentially affected by that change.

**Proof.** A relevant dependency gives a finite path from the assessment to the changed object. Reversal makes the assessment reachable from the change. Complete traversal includes every such path. ∎

This result identifies candidates for reassessment, not automatic failures. An assessment may remain valid because an alternative ground still suffices. Conversely, a missing edge can hide an affected assessment despite a correct traversal algorithm.

### Proposition 4. Adoption is not a truth-preserving inference rule

Let \(A\) be an adoption record and \(F\) a factual proposition in the adopted rule. Suppose \(A\land F\) and \(A\land\neg F\) are both satisfiable under the admitted interpretation. Then the adoption record alone does not entail \(F\).

**Argument.** The satisfying interpretation of \(A\land\neg F\) is a countermodel to \(A\Rightarrow F\). The other interpretation shows that the same adoption record is also compatible with \(F\). Thus adoption alone leaves this contingent factual content undecided. ∎

The independence premise excludes logical validities and facts already entailed by the adoption record, such as a correctly represented fact about the adoption event itself. An additional reliable procedure could supply evidence for \(F\), but its reliability would be a separate premise. This does not deny the practical force of adopted rules; it locates that force in the declared governance policy.

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

### 6.1 Constructed revision sequence

Consider a fictional procedure whose first revision permits automated processing only for validated inputs. An assessment records that this revision preserves the condition, and an authorized decision adopts that exact revision for a named process. The following changes have different effects; the example asserts no observed deployment result.

**Table 1. Changes that must not collapse into a single status.**

| Change | What changes | What does not follow |
| --- | --- | --- |
| A new counterexample shows that the input checker accepts an invalid case. | The assessment of that checker and dependent assurances needs revision. | The stored procedure text has changed, or every dependent conclusion is false. |
| A proposed second revision removes the validation condition. | The procedure has new content requiring its own assessment. | An adoption of the first revision also adopts the second. |
| An authorized withdrawal ends current use of the first revision. | Its present normative status changes. | Its historical content or the earlier adoption event disappears. |
| A rendered copy omits the condition while retaining the title. | The delivered representation fails the stated preservation obligation. | Matching titles establish equivalent instructions. |
| The earlier revision is unavailable from storage. | Exact retrieval must report failure under Proposition 1's premise. | A current replacement can be silently returned as the pinned historical revision. |

Suppose two permitted grounds independently suffice for one assessment. Losing one ground makes that assessment a reassessment candidate, but the other may still justify it. Conversely, an omitted dependency can prevent a traversal from finding an assessment that has actually lost its only ground. These cases separate dependency completeness, candidate identification, and the subsequent support judgment.

## 7. Falsification and evidence boundary

The model can be tested with cases that change one material feature: a source revision, authority grant, effective date, interpretation rule, or mandatory dependency. It should also include unchanged content with a changed assessment, and changed layout with preserved content but impaired delivery.

Counterexamples are particularly useful where identifiers conceal assumptions. Reusing a prior receipt after a policy change tests whether the receipt is wrongly treated as permanent permission. Updating a current pointer while resolving a pinned reference tests historical selection. Merging two textually equal records with different provenance tests whether deduplication destroys relevant history.

These controls can establish behavior on finite represented cases. They do not prove complete dependency discovery, correct interpretation of all governance rules, or trustworthy authentication in an unexamined deployment. The formal propositions remain conditional on those boundaries.

The contribution is an explicit account of the stated distinctions between content, assessment, historical selection, and normative adoption, together with checkable consequences and counterexamples. It does not claim that this list exhausts every governance model. Nor does it make an empirical claim that one governance procedure is universally superior or that the model resolves substantive disagreement automatically.

### 7.1 What a useful test must distinguish

A finite test suite should pair each intended behavior with a deliberately weaker alternative: resolve a pin versus silently follow the current pointer; compare complete inputs versus compare text alone; reassess reachable dependents versus mark them all false; and inspect present authority versus reuse an earlier approval. Failure to distinguish those alternatives is a limitation of the test, not evidence that the extra obligation is unnecessary.

The independence premise of Proposition 4 also needs a control. When the factual proposition is already entailed by the adoption record, the stated non-entailment conclusion is not licensed by that proposition. An adoption event can establish a correctly recorded fact about that event while leaving another empirical claim unsupported. No general rejection of institutional facts follows.

## 8. Connections to the published engineering work

The [executable projections and revision study](../../engineering/studies/executable-projections-and-revision/STUDY.md) concerns pinned revisions and bounded update behavior. The [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) examines current eligibility of previously prepared artifacts.

The shared [glossary](../../reference/glossary/GLOSSARY.md), [interaction and memory](../interaction-and-memory/PAPER.md), and [controlled knowledge reuse](../controlled-knowledge-reuse/PAPER.md) define the connected work-state and admission obligations.

## 9. Conclusion

Knowledge revision requires an account of which object changed and which justification remains applicable. Under the stated premises, a pin fixes historical selection, equal complete inputs preserve a deterministic check's result, and complete represented dependencies permit identification of reassessment candidates. Adoption alone does not settle a contingent factual claim when the same adoption record is compatible with both its truth and falsity.

These results are deliberately limited. A repeated result is not a soundness proof; a dependency path is not a finding of invalidity; and a historical adoption is not permanent current authority. The account specifies distinctions and conditional obligations that an implementation can be tested against. It does not establish a universal revision policy, an automatic method for discovering all semantic dependencies, or measured advantages over other systems. Each stronger claim requires its own model, evidence, and review.

## References

1. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
2. Doyle, J. “A Truth Maintenance System.” *Artificial Intelligence* 12(3), 1979, 231–272. [Publisher record](https://www.sciencedirect.com/science/article/pii/0004370279900080). [MIT report version, AI Memo 521](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a).
3. Alchourrón, C. E., Gärdenfors, P., and Makinson, D. “On the Logic of Theory Change: Partial Meet Contraction and Revision Functions.” *The Journal of Symbolic Logic* 50(2), 1985, 510–530. <https://doi.org/10.2307/2274239>
