---
name: "interaction-and-memory"
title: "Interaction, Documents, and Memory with Explicit Revision Boundaries"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Versioned requirements, dialogue branches, memory and evidence of learning in agent interaction."
---

# Interaction, Documents, and Memory with Explicit Revision Boundaries

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

An assistant's conversation, work state, documents, and durable memory evolve at different rates and under different rules. Treating them as one expanding transcript makes corrections, delayed results, and changes of purpose difficult to interpret. This paper defines a state model that separates messages from communicative acts, Work Items from execution attempts, and current task context from admitted memory. Documents are versioned outputs whose correctness must be checked after rendering or revision. We establish conditional properties for generation boundaries, idempotent event handling, and narrow update scope, and apply the corpus's general dependency-directed reassessment result. Counterexamples identify where correct state handling still permits semantic error. The model also distinguishes observed task success from learning and user acceptance from evidence. Its contribution is a coherent set of transition obligations for dialogue and memory, with falsifiable implementation consequences. It does not establish that any current interpreter reliably recognizes every intention, referent, or learning outcome.

**Keywords:** dialogue; Work Item; document revision; memory; requirements; learning assessment.

## 1. Research question

A conversation can contain instructions, quotations, corrections, tentative ideas, and reports of previous actions. It can also receive a delayed result after the user has changed the goal. If every new message simply overwrites one mutable state, the system cannot reliably explain which requirements a result satisfies or why a memory applies.

We ask: **how should interaction state change so that the scope of a statement, correction, or result remains inspectable?** The proposed answer separates interpretation from authorized transition, and separates immediate dialogue context from persistent knowledge.

The model builds on ordinary distinctions between activities, entities, and agents represented in PROV-DM [1]. It adds explicit obligations for dialogue generations, document outputs, and admission into memory. These obligations are a design model. Their practical adequacy must be assessed against independently interpreted conversations, not inferred from the existence of a structured event log.

## 2. Messages, acts, and work

A **message** is a received or generated representation with sender attribution, time, and content. A **communicative act** is an interpreted function of some content: a request, correction, question, proposal, acknowledgment, or report. One message can contain several acts. An act record should identify its target, scope, and uncertainty.

Quoted content is not automatically an instruction from the present speaker. Likewise, a statement that an action occurred is evidence of that report, not proof of execution. Interpretation assigns a candidate role; authorization determines whether the resulting transition is permitted.

A **Work Item** is a bounded objective with requirements, constraints, expected outputs, and acceptance conditions. `WorkItem` is a serialization spelling of that same entity, not a second concept. An **attempt** is one execution toward the objective. A document or other **output** is a result of an attempt. A message can create or modify a Work Item without itself constituting an execution attempt.

Let the active work state be

\[
W=(i,g,R,C,O,A),
\]

where \(i\) is identity, \(g\) is a requirement generation, \(R\) requirements, \(C\) constraints, \(O\) output expectations, and \(A\) acceptance conditions. A material change creates a new generation whose identifier is never reissued within that Work Item, including after rollback or restoration of earlier requirements. A strictly increasing counter is one implementation. A requirements-content hash alone does not distinguish a later return to earlier content. This discipline does not require abandoning all previous work: an earlier output can be re-evaluated for the new generation, with its original provenance preserved.

Understanding, agreement, evidence, and authority remain separate. A user can understand an answer and reject its conclusion. An authorized owner can accept a document despite an acknowledged evidential limitation. Neither act changes the truth of its factual propositions by definition.

## 3. Context and memory layers

We distinguish immediate conversation context, the current Work Item state, durable user or project memory, and externally sourced knowledge. The distinction is operational: each layer has different admission, revision, scope, and retrieval rules. Storing everything in one database does not eliminate these differences.

A memory record contains content, provenance, applicability scope, assessment state, and a revision or revocation relation. A statement intended for one task does not become a permanent preference merely because it is repeated. Widening its scope requires a justified transition, such as an explicit instruction or a separately supported generalization.

Memory admission is therefore a decision with conditions. Relevant conditions can include attribution, intended persistence, consistency with current instructions, permission to retain, and a defined use scope. Unknown mandatory conditions do not count as satisfied. Retrieval later must check whether the record remains applicable to the present task and recipient.

Memory has dependencies. A derived preference, summary, or plan may rely on earlier records whose revision changes its basis. Revocation does not always imply physical deletion: a historical record may remain necessary for an audit while being inadmissible for current guidance. Current use, archival availability, and storage retention must be modeled separately.

## 4. Documents as evaluated outputs

A document is a versioned representation, not merely a string emitted during conversation. Its assessment has several axes: source fidelity, factual support, satisfaction of requirements, internal consistency, readability, accessibility, and acceptance for a specific use. A fluent document can fail a mandatory requirement; a faithful transcription can be poorly organized.

Generation and editing therefore have a final-output obligation. The actual document must be inspected after assembly, including headings, references, tables, images, and any constraints that can be lost during rendering. Checking only the retrieved sources or an intermediate outline leaves the delivered output unevaluated.

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

This is a measurement obligation rather than a theory of human learning. Different studies may examine transfer, delayed retention, error correction, or independent task completion. Their outcomes should not be collapsed into one unqualified “learned” flag.

Counterexamples test the boundaries of dialogue interpretation. A correction to one branch must not silently rewrite another branch. An ambiguous “use that version” should not become a verified referent without resolution. A delayed answer must not reinstate a withdrawn requirement. A quoted instruction must not acquire the authority of its surrounding message merely because it uses imperative wording.

Further counterexamples concern memory and documents. A task-specific choice should not become an unrestricted preference; a revoked premise should not remain an unnoticed basis for a recommendation; and a successful local edit should not waive whole-document consistency checks. These cases can be specified without assuming any particular domain or model.

## 7. Evidence and limits

The model supports finite transition tests and independently annotated dialogue cases. A useful evaluation reports interpretation mistakes separately from transition-handling mistakes. Otherwise a correct event processor can hide a poor interpreter, or an accurate interpreter can be blamed for an unrelated state-management defect.

This paper establishes only its conditional state properties. It reports no measured improvement in learning, long-term recall, or agent reliability. Structural validation cannot authenticate a speaker by itself, and a requirements map cannot prove that the final document satisfies its intended meaning. Those dependencies require their own evidence and must remain visible in a claim of end-to-end performance.

The [executable projections and revision study](../../engineering/studies/executable-projections-and-revision/STUDY.md) evaluates reader boundaries, selection of records for addressed revision, and finite partial projections. It does not test Work Item generation admission or concurrent event idempotence; no engineering study in this corpus supplies implementation evidence for Propositions 1–2. The [editorial skill pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) compares two produced versions of one text under disclosed editorial requirements. The shared [glossary](../../reference/glossary/GLOSSARY.md), [revision and governance](../revision-and-governance/PAPER.md), and [evidence and falsification](../evidence-and-falsification/PAPER.md) supply related definitions and assessment boundaries.

## References

1. W3C. *PROV-DM: The PROV Data Model*. W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
