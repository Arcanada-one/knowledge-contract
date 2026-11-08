---
name: "interaction-and-memory"
title: "Interaction and Memory: Interaction, Documents, and Memory with Explicit Revision Boundaries"
short_title: "Interaction and Memory"
subtitle: "Interaction, Documents, and Memory with Explicit Revision Boundaries"
previous_title: "Interaction, Documents, and Memory with Explicit Revision Boundaries"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Versioned requirements, dialogue branches, memory and evidence of learning in agent interaction."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="interaction-documents-and-memory-with-explicit-revision-boundaries"></a>

# Interaction and Memory: Interaction, Documents, and Memory with Explicit Revision Boundaries

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

A conversation record does not by itself identify which requirements a result satisfies, authorize a correction, or justify persistent memory. This paper asks how an assistant can keep those boundaries inspectable while messages, tasks, documents, and memory change. We separate message content from interpreted communicative acts, Work Items from attempts, and temporary context from admitted memory. A versioned work state records requirements and their generation; a delivered document is assessed as a particular output rather than inferred correct from its sources. Three conditional propositions address stale-result admission, duplicate internal effects, and observations preserved by a narrow update. Their premises include non-reissued generations, an acceptance-time comparison, atomic event records, and correctly scoped state components. Constructed boundary cases show why matching requirement bytes, a prior check, or a plausible event log is insufficient. We also distinguish memory retention from current applicability and observed performance from learning. The method is deductive and scope-limited. It neither supplies a complete interpreter of human intent nor demonstrates concurrent production enforcement, improved recall, or learning. Its contribution is an explicit account of what must be interpreted, authorized, versioned, and checked before a conversational result can become current guidance.

**Keywords:** dialogue; Work Item; document revision; memory; requirements; learning assessment.

## 1. Research question

A conversation can contain instructions, quotations, corrections, tentative ideas, and reports of previous actions. It can also receive a delayed result after the user has changed the goal. If every new message simply overwrites one mutable state, the system cannot reliably explain which requirements a result satisfies or why a memory applies.

We ask: **how should interaction state change so that the scope of a statement, correction, or result remains inspectable?** The proposed answer separates interpretation from authorized transition, and separates immediate dialogue context from persistent knowledge.

The model builds on the distinctions among entities, activities, and agents in PROV-DM [1]. That source supplies a provenance vocabulary, not a guarantee that an assistant correctly interpreted an instruction or executed a permitted transition. This paper applies explicit identity, scope, and assessment boundaries to interaction. It does not claim that versioning or transaction atomicity originate here.

The contribution has three parts: a separation of the objects that change during interaction; conditional arguments about three state transitions; and boundary cases that identify what those arguments leave open. The method is deductive: define the state, state the premises, derive the bounded consequence, and test the effect of omitting a premise. Practical adequacy still requires independently interpreted conversations and checks on the actual implementation. A structured event log alone establishes neither.

## 2. Messages, acts, and work

A **message** is a received or generated representation with sender attribution, time, and content. A **communicative act** is an interpreted function of some content: a request, correction, question, proposal, acknowledgment, or report. One message can contain several acts. An act record should identify its target, scope, and uncertainty.

Quoted content is not automatically an instruction from the present speaker. Likewise, a statement that an action occurred is evidence of that report, not proof of execution. Interpretation assigns a candidate role; authorization determines whether the resulting transition is permitted.

A **Work Item** is a bounded objective with requirements, constraints, expected outputs, and acceptance conditions. `WorkItem` is a serialization spelling of that same entity, not a second concept. An **attempt** is one execution toward the objective. A document or other **output** is a result of an attempt. A message can create or modify a Work Item without itself constituting an execution attempt.

Let the active work state be

\[
W=(i,g,R,C,O,A),
\]

where \(i\) is identity, \(g\) is a requirement generation, \(R\) requirements, \(C\) constraints, \(O\) output expectations, and \(A\) acceptance conditions. A material change creates a new generation whose identifier is never reissued within that Work Item, including after rollback or restoration of earlier requirements. A strictly increasing counter is one implementation. A requirements-content hash alone does not distinguish a later return to earlier content.

The identity is part of the comparison. Equal generation numbers in different Work Items do not identify the same assignment. A branch or restored task must preserve a distinguishable task-and-generation scope rather than silently reuse an old identity pair. This is an identity obligation, not a requirement that every implementation use one global counter.

Earlier work need not be discarded. An earlier output can be re-evaluated for the active generation while its original provenance remains intact. The new assessment must concern that exact output, target generation, and intended use; a passing assessment for another output is not transferable merely because their labels match. The active generation must still be checked at acceptance. Matching a generation also does not decide which of several attempts for that same generation should become current. That requires a separately stated selection rule and any applicable output checks.

Understanding, agreement, evidence, and authority remain separate. A user can understand an answer and reject its conclusion. An authorized owner can accept a document despite an acknowledged evidential limitation. Neither act changes the truth of its factual propositions by definition.

## 3. Context and memory layers

We distinguish four layers by their use and admission rules, not by their physical storage location.

**Table 1. Interaction layers and the distinction each must preserve.**

| Layer | What it records | What its presence does not establish |
| --- | --- | --- |
| Immediate conversation context | Messages and candidate interpretations needed for the current exchange | A standing instruction or persistent preference |
| Current Work Item state | The active objective, generation, requirements, and constraints | Completion of an attempt or correctness of an output |
| Durable user or project memory | Retained content with provenance, scope, and assessment | Applicability to every later task or recipient |
| Externally sourced knowledge | Attributed material and its interpretation | Truth, present authority, or permission to retain and reuse it |

Each layer therefore needs its own admission, revision, and retrieval rules. Keeping all four in one database does not remove their logical differences.

A memory record contains content, provenance, applicability scope, assessment state, and a revision or revocation relation. A statement intended for one task does not become a permanent preference merely because it is repeated. Widening its scope requires a justified transition, such as an explicit instruction or a separately supported generalization.

Memory admission is therefore a decision with conditions. Relevant conditions can include attribution, intended persistence, consistency with current instructions, permission to retain, and a defined use scope. Unknown mandatory conditions do not count as satisfied. Retrieval later must check whether the record remains applicable to the present task and recipient.

Memory has dependencies. A derived preference, summary, or plan may rely on earlier records whose revision changes its basis. Current use, archival availability, and storage retention are separate decisions. A historical record may be retained for a permitted audit purpose while being excluded from current guidance. This distinction does not itself authorize retention, override an erasure obligation, or give a later recipient access. Those conditions remain subject to the applicable policy.

Repeated retrieval is not a new assessment. A record can be returned faithfully yet be unsuitable for the present task because its scope changed, its basis was revoked, or its intended persistence was never established. When a mandatory condition is unknown, neither repetition nor storage duration changes that condition into a pass.

## 4. Documents as evaluated outputs

A document is a versioned representation, not merely a string emitted during conversation. Its assessment has several axes: source fidelity, factual support, satisfaction of requirements, internal consistency, readability, accessibility, and acceptance for a specific use. A fluent document can fail a mandatory requirement; a faithful transcription can be poorly organized.

Generation and editing therefore have a final-output obligation. The actual document must be inspected after assembly, including headings, references, tables, images, and conditions that rendering can omit or detach from their scope. Checking only the retrieved sources or an intermediate outline leaves the delivered output unevaluated.

An assessment should name the exact document revision and representation it inspected. A Markdown-source check is not automatically a PDF-layout check; a valid intermediate file is not evidence that the recipient received that file. The required checks depend on the intended use, but their subject cannot silently change between assessment and delivery. A content identifier can bind a check to bytes; it does not by itself establish the document's meaning or accessibility.

A local edit also has both local and global effects. Replacing one section can change cross-references, definitions, totals, or the force of a conclusion elsewhere. The edit record should state its intended scope, while dependency information identifies the additional checks needed. A claim that “only one paragraph changed” is not evidence that every unaffected-looking paragraph remains valid.

Document summaries become a separate memory object when reused. A summary may omit details acceptable for its original audience but necessary for a later task. Reuse should apply the same applicability and dependency discipline as any other prepared knowledge.

## 5. Conditional transition properties

### Proposition 1. Generation admission prevents a specified stale update

Suppose a result carries the Work Item identity and generation for which it was produced, and generation identifiers are unique and never reissued within that Work Item. Suppose the acceptance transition checks those identifiers against the active state at the same serialization point at which it makes the result current. Direct acceptance requires an exact match; otherwise a separate successful re-evaluation bound to the active generation is required. Then a result from an earlier generation cannot be accepted as current solely through its original completion event.

**Proof.** Non-reuse of generation identifiers makes an earlier generation different from the active one, even if the requirements later return to earlier content. Its completion event therefore fails the direct-admission comparison at acceptance. The only remaining path requires a new evaluation, so original completion alone is insufficient. ∎

This property depends on correct identifiers and enforcement at the transition boundary. It does not guarantee that the interpreter recognized a material requirement change or that the re-evaluation is semantically correct.

### Proposition 2. Recorded duplicate events need not duplicate effects

Let an event handler serialize the check and creation of a stable event identifier so that at most one first commit for that identifier can succeed. The identifier, payload fingerprint, result or stable result reference, and internal effect commit in one atomic state change. A concurrent contender that loses the first-commit race performs no committed effect and reads the winning record. Subsequent handling of the same identifier and payload returns the stored result without applying the effect again; a different payload is rejected as a conflict.

**Proof.** Serialization permits at most one successful first commit. Atomicity binds that commit's effect to its identifier, fingerprint, and result, and prevents an aborted contender from retaining an internal effect. Every later successful lookup takes the duplicate or conflict branch, neither of which applies a new effect. The duplicate branch can return the result because that result or its stable reference was committed with the identifier. ∎

A unique identifier constraint can enforce the first-commit rule only when a conflicting transaction rolls back its whole internal effect and then reads the committed record. Independent atomic transactions without that uniqueness or serialization condition are insufficient: two first deliveries can both observe absence. The result establishes idempotent handling within the stated state boundary, not exactly-once execution of an external action whose system lies outside it. Fingerprint equality also presupposes the declared canonical payload comparison and collision assumptions.

### Dependency-directed reassessment

The general reachability result is stated once in [Revision and governance, Proposition 3](../revision-and-governance/PAPER.md#proposition-3-complete-dependencies-identify-candidates-for-reassessment). Applied to memory and documents, it identifies output assessments that may need reconsideration after a represented dependency changes. The premise is a complete finite dependency graph; the conclusion is candidate identification, not a verdict that the affected output is now false. An omitted dependency defeats that premise even if traversal is correct.

### Proposition 3. A narrow update preserves independent state components

Let a transition write only a declared component set \(J\) of a product state and leave all other components unchanged. Then every observation depending solely on components outside \(J\) is preserved.

**Proof.** Such an observation receives identical component values before and after the transition. ∎

This syntactic preservation result requires correct scope. If two components are semantically coupled but that coupling is omitted, unchanged bytes do not guarantee an unchanged valid interpretation.

## 6. Learning, correction, and counterexamples

A useful tutoring conversation distinguishes the learner's own attempt, supplied assistance, observed performance, and the assessment being made. Repeating an explanation or accepting an answer does not establish learning. A learning claim requires a declared skill, assessment conditions, a time horizon, and evidence that discriminates retained ability from immediate assistance or memorized responses.

This is a measurement obligation rather than a theory of human learning. Different studies may examine transfer, delayed retention, error correction, or independent task completion. Their outcomes should not be collapsed into one unqualified “learned” flag. The same separation applies when assessing an agent: a successful assisted attempt, a newly stored record, and improved performance on an independently specified task are different observations. This paper reports none of those as a measured improvement.

Counterexamples test the boundaries of dialogue interpretation. A correction to one branch must not silently rewrite another branch. An ambiguous “use that version” should not become a verified referent without resolution. A delayed answer must not reinstate a withdrawn requirement. A quoted instruction must not acquire the authority of its surrounding message merely because it uses imperative wording.

Further counterexamples concern memory and documents. A task-specific choice should not become an unrestricted preference; a revoked premise should not remain an unnoticed basis for a recommendation; and a successful local edit should not waive whole-document consistency checks. These cases can be specified without assuming any particular domain or model.

### Constructed transition-boundary cases

Consider requirements that change from A to B and later return to A. An old output and the active requirements can have matching content fingerprints while belonging to different generations. The direct-admission comparison still rejects the old generation. A new assessment may justify reuse, but changing the output label to the active generation is not such an assessment. Likewise, checking a matching generation and then accepting after an intervening change violates the shared-serialization-point premise of Proposition 1. Neither case refutes the proposition: each removes a stated premise or substitutes a weaker rule.

For Proposition 2, the event identifier must be interpreted in its declared namespace and the recorded outcome must remain available throughout the claimed deduplication scope. Deleting that record and treating a replay as unseen can apply the effect again. A retention period can bound a claim; it cannot support unqualified deduplication of later replays after the identifying state is gone. Distinct identifiers for the same business action are another case: this proposition deduplicates identifiers and matching payloads, not all semantically equivalent intentions.

A further boundary is an external action. Suppose an external service applies an action, but the local handler fails before recording the outcome. Retrying without a shared atomic boundary or an effective external idempotency mechanism can repeat the action. Recording local intent first does not alone prove that the action occurred. The two systems' evidence and recovery protocol require their own argument; the internal atomicity proposition supplies no exactly-once guarantee for them.

Finally, an observation in Proposition 3 must really depend only on unchanged components under the same interpretation. Updating a shared referent, an aliased object, or an external basis can defeat a claim of independence even if a nearby field's bytes did not change. A declared write set is not proof of the actual write set. These are constructed boundary cases, not reported defects or measured frequencies in a deployed assistant.

## 7. Evidence and limits

The model supports finite transition tests and independently annotated dialogue cases. A useful evaluation reports interpretation mistakes separately from transition-handling mistakes. Otherwise a correct event processor can hide a poor interpreter, or an accurate interpreter can be blamed for an unrelated state-management defect.

This paper establishes only its conditional state properties. It reports no measured improvement in learning, long-term recall, or agent reliability. Structural validation cannot authenticate a speaker by itself, and a requirements map cannot prove that the final document satisfies its intended meaning. Those dependencies require their own evidence and must remain visible in a claim of end-to-end performance.

The [executable projections and revision study](../../engineering/studies/executable-projections-and-revision/STUDY.md) evaluates reader boundaries, selection of records for addressed revision, and finite partial projections. It does not test Work Item generation admission or concurrent event idempotence; no engineering study in this corpus supplies implementation evidence for Propositions 1–2. The [editorial skill pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) compares two produced versions of one text under disclosed editorial requirements. The shared [glossary](../../reference/glossary/GLOSSARY.md), [revision and governance](../revision-and-governance/PAPER.md), and [evidence and falsification](../evidence-and-falsification/PAPER.md) supply related definitions and assessment boundaries.

## 8. Conclusion

Interaction requires more than retaining the transcript. A system must distinguish what was said, how it was interpreted, which transition was authorized, which requirement generation an output addresses, and whether retained information applies now. These distinctions make disagreement and uncertainty inspectable rather than silently converting them into accepted state.

The three propositions establish conditional safeguards, not a complete theory of dialogue. Non-reissued generations and an acceptance-time comparison prevent the specified stale update. A serialized, atomic event record prevents duplicate internal effects within its stated identity and retention boundary. A narrow write preserves only observations that genuinely depend on unchanged components. None of these results establishes semantic interpretation, external exactly-once execution, or an automatic learning outcome.

The practical consequence is to bind each assessment to its actual subject and scope, preserve historical provenance without treating it as current authority, and test the delivered representation rather than infer its quality from intermediate success. Independent semantic evaluation and implementation evidence remain separate requirements. When those observations are missing, the limitation must remain visible instead of being hidden behind a fluent answer, an event identifier, or a positive receipt.

## References

1. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
