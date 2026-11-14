---
title: Foundations-first manuscript package
sources: none
status: planned manuscript preparation; not a released corpus
updated: 2026-11-14
---

# Foundations-first manuscript package

> **Current source status (11 November 2026).** The F04 target `papers/geometry-of-semantic-representations/PAPER.md` now exists on source main `0892eeb1` with `research-draft` status. The 8 November preparation table and its `New` action are historical planning records, not today's missing-document inventory. A bounded mathematical review of a draft is not acceptance of the full F04 package, independent geometry evaluation or the six-unit foundations release.
>
> Editorial context (8 November 2026; execution direction updated 11 November): names replace opaque reader-facing labels; compatibility mappings are in [workstreams.json](workstreams.json). At the 8 November checkpoint the operator had paused engineering execution. The operator restored availability on 11 November; [Active Work](EXECUTION_STATUS.md) now governs current work. This document alone authorizes no deployment, costly experiment or unrestricted execution; task, review, access and budget gates still apply.

> **Priority update (14 November 2026).** The operator explicitly prioritizes knowledge algebra, meaning geometry, meaning algebra, meaning theory and agent state with proofs, executable engineering and tests. [The current five-direction plan](PRIORITIES_20261114.md) supersedes the historical one-manuscript-at-a-time preparation order below. The six-unit inventory and its acceptance dependencies remain; parallel preparation does not close them.

## 1. Updated decision and scope

The author's updated direction on 6 November 2026 is to prepare the missing foundations first, reconcile their links to the corpus, and only then resume its general editorial pass. This changes the immediate order in [ROADMAP.md](../ROADMAP.md) and the start boundary of Editorial Release in [TASKS.md](TASKS.md). It does not erase the 25 work packages, history or real execution bindings. The finite research boundary remains: completing every future experiment is not a condition for publishing an honest, bounded contribution.

The package has six document units: two new scientific papers, a substantial extension of one existing paper, two new engineering specifications and one new study of explicitly bounded worked cases. A shared integration map, vocabulary update and source ledger accompany them. The new paths below are proposed targets, not existing files.

6 November is the intended manuscript-preparation batch, not a promise that six independently reviewed publications, a deployment or a whole empirical programme will finish that day. Complete first manuscripts are saved in repository changes immediately; scientific acceptance, main-branch integration and live publication remain separately verified. An outline, planned experiment or unsupported theorem is not a completed result.

This turn establishes the plan. The next content operation is Meaning Bridge, not the old third-document copy-edit. Proceed one work at a time in the user-directed workflow; do not start the entire sequence from a mailbox timer. Existing authorized review and delivery of the first two edited papers may finish. Preserve their work and unrelated sessions.

## 2. Baseline and reuse

The inspected source baseline is `717c43deb514adc5b40f76837e7ee0fb2da37102`. Its [catalogue](../publication-catalog.json) contains 29 canonical documents. It already includes semantic objects, constrained transformations, evidence and falsification, semantic types, operation contracts, professional artifacts and actual studies. These are the starting point, not material to replace silently.

The [transformation paper](../papers/constrained-transformations/PAPER.md) already covers partial relations, composition, observation equivalence, projection, residuals and reconstruction. Transformation Algebra extends that path instead of creating a competing algebra manuscript. The [semantic-types specification](../engineering/specifications/semantic-types/SPECIFICATION.md) remains authoritative for its existing facets; Semantic Bridge supplies a bounded conversion process. The [evidence paper](../papers/evidence-and-falsification/PAPER.md) remains the scientific account; Semantic Verification specifies preparation and assessment of concrete verification packets. Historical I10/I12 material is a recovery lead under Claim Atlas, not automatically current authority.

No edition, protocol, API behavior or index state changes because this plan exists. Read [AGENTS.md](../AGENTS.md), [CONTRIBUTING.md](../CONTRIBUTING.md) and [PUBLISHING.md](../PUBLISHING.md) at the actual source revision before changes.

## 3. Preparation sequence

| Unit | Kind | Working title | Action | Roadmap coverage |
| --- | --- | --- | --- | --- |
| Meaning Bridge | Scientific paper | From Human Meaning to Contract-Governed Knowledge | New | Claim Atlas, Meaning Bridge, Source Audit |
| Semantic Bridge | Engineering specification | From Source Interpretation to Computable Knowledge: A Bounded Semantic Bridge | New; reuse semantic-types | Semantic Bridge, Extraction Fidelity |
| Transformation Algebra | Scientific paper | Constrained Transformations: Algebraic Profiles, Composition and Reconstruction | Extend existing constrained-transformations | Transformation Algebra, Meaning Cases, Falsification Register |
| Semantic Geometry | Scientific paper | Geometry of Semantic Representations: Similarity, Context and Limits | New | Semantic Geometry, Geometry Evaluation, Hybrid Retrieval |
| Semantic Verification | Engineering specification | Verification Contracts for Semantic Claims and Implementations | New; reuse evidence paper | Verification Records, Falsification Register, Scaled Checks, Theory Traceability |
| Meaning Controls | Engineering study | Worked Semantic Operations: Examples, Counterexamples and Bounded Checks | New, with actual analytic or executed results | Meaning Cases, Scaled Checks, Geometry Evaluation, Extraction Fidelity, Agent Application |

F identifiers name this sequence, not new Muneral tasks. Reconcile them to existing RM work and actual records. Writing a geometry paper does not complete its benchmark; writing a bridge specification does not implement an extractor.

<!-- markdownlint-disable-next-line MD033 -->
<a id="f01.-human-meaning-and-contract-governed-knowledge"></a>

### Meaning Bridge. Human meaning and contract-governed knowledge

**Proposed target:** `papers/human-meaning-and-computable-knowledge/PAPER.md`.

**Question:** What can be preserved and checked when a contextual human expression becomes knowledge an agent stores, transforms and uses?

Begin with an ordinary example before notation. Distinguish expression, intention, referent, proposition, context, interpretation, truth, justification, applicability and authorization. Separate human experience from a computational representation selected for a purpose. Trace source, possible interpretations, declared observations, knowledge artifacts, storage and a particular agent request. State what remains unresolved: tacit context, metaphor, ambiguity, changing goals and unsupported generalizations.

Include related work and a precise contribution statement. Verify primary literature before attribution or novelty claims. Conventional mathematical constructions retain their attribution. This is a bounded conceptual/formal framework, not a universal deterministic reduction of human meaning.

**Structure:** abstract; question/contribution; related work; distinctions and assumptions; framework; illustrative derivation; implications for KC; limitations; conclusion; references.

**Acceptance:** a new reader follows the entire chain without private project knowledge; symbols are defined; source assertion is not endorsement; a worked example preserves its exception, attribution and unresolved information. A theorem has a complete proof; an unproved proposal is identified as such.

<!-- markdownlint-disable-next-line MD033 -->
<a id="f02.-the-bounded-semantic-bridge"></a>

### Semantic Bridge. The bounded semantic bridge

**Proposed target:** `engineering/specifications/semantic-bridge/SPECIFICATION.md`.

**Question:** Which explicit steps connect an interpretation to a computable object and an artifact suitable for a stated task?

Specify source and representation identity, context, candidate interpretations, typed operators, units, quantifier/negation scope, attribution, evidence and losses. Separate candidate generation, which may use a language model, from deterministic checks in a declared formal fragment. State supported operations, undecided or unsupported cases, and termination/resource bounds only where justified. Do not call arbitrary language interpretation deterministic.

Describe accepted, partial, ambiguous, unsupported and rejected outcomes by reusing the existing status model. Explain the route to Role, Skill, Competency, Blueprint and Constraint artifacts without confusing descriptions, assessments and runtime authority. Reuse definitions and requirement IDs; new normative clauses receive identifiers through the normal register workflow.

**Acceptance:** inputs, outputs and failure behavior are explicit; multiple readings survive when warranted; losses distinguish omission from uncertainty; proposed fields are not described as deployed. References to semantic-types, core, artifact-registry and context-package replace duplicated definitions.

<!-- markdownlint-disable-next-line MD033 -->
<a id="f03.-algebraic-profiles-and-transformations"></a>

### Transformation Algebra. Algebraic profiles and transformations

**Canonical target:** `papers/constrained-transformations/PAPER.md`.

**Question:** Under which profiles can operations be composed, compared or reversed without exceeding their assumptions?

Retain and review the existing propositions and sources. Make carriers, observations, partial domains and profiles explicit. Develop entailment, observation equivalence, common consequence, conjunction/merge, projection, residual, reconstruction, composition and transfer. Explain representative independence and partial-domain congruence. State which laws hold, fail or remain unproved.

Use exact Boolean and typed-record/quantity profiles as declared examples. Logical common consequence is not automatically a useful common theme of books. Reconstruction and size savings are different claims. Distinguish nonempty/consistent interpretation from vacuous success. Incorporate historical material through a proposition-level map.

**Acceptance:** each operation has types, domain, semantics, conditions, a positive example and an adverse case. Changed scientific claims have a derivation or explicit unresolved status. Existing citations and dependent propositions remain traceable. This is substantive revision, not a typography-only change.

<!-- markdownlint-disable-next-line MD033 -->
<a id="f04.-geometry-of-semantic-representations"></a>

### Semantic Geometry. Geometry of semantic representations

**Proposed target:** `papers/geometry-of-semantic-representations/PAPER.md`.

**Question:** What can distance and similarity contribute to retrieval, and what cannot be inferred from them alone?

Define the representation map, represented object/context, space and chosen distance or similarity. Distinguish metric, pseudometric, similarity, semantic equivalence and directed entailment. Explain information loss, collisions, threshold nontransitivity and context-dependent neighborhoods. Every diagram must illustrate a defined relation, not imply that visual proximity proves meaning.

Develop exact countermodels and bounded deductions. Model-specific reliability, learned metric quality and benchmark superiority remain empirical questions until measured. Give geometry a constructive role as candidate generation followed by source, logical, applicability and authorization checks; do not claim vectors capture complete human meaning.

**Acceptance:** every geometric term has a carrier and operation; claimed axioms are justified for the selected measure; examples distinguish similarity from equivalence; the intended useful interface and untested claims are both explicit.

<!-- markdownlint-disable-next-line MD033 -->
<a id="f05.-verification-contracts"></a>

### Semantic Verification. Verification contracts

**Proposed target:** `engineering/specifications/semantic-verification/SPECIFICATION.md`.

**Question:** What exactly does a check establish, and how is a claim traced to supporting evidence?

Specify a record connecting claim, assumptions, profile, object under test, source/build revision, inputs, oracle, intervention, expected outcome, observation and limitation. Distinguish proof review, finite enumeration, implementation regression, source fidelity, task outcomes and controlled comparison. Reuse the evidence index and assessment semantics rather than creating another status authority.

Every finite count identifies its space, formula, bound and justification. Separate calculated cardinality from executed cases; expose vacuity and correlated or redundant configurations. A counterexample to a theorem satisfies its premises and violates its conclusion. Violating a premise tests a boundary or implementation instead. Positive controls prevent an always-rejecting system from appearing correct.

**Acceptance:** a reviewer can reconstruct the scope; the graph-root and Boolean-function uses of 4096 cannot be confused; actual code is distinguished from a separate reference model; self-review, rerun and independent reproduction remain different. The specification does not report unperformed tests.

<!-- markdownlint-disable-next-line MD033 -->
<a id="f06.-worked-operations-and-bounded-controls"></a>

### Meaning Controls. Worked operations and bounded controls

**Proposed target:** `engineering/studies/meaning-operations-controls/STUDY.md`, with its supporting files.

**Question:** Do the declared operations behave as stated on the cases actually evaluated?

Begin with three coherent traces: a rule with exception and attribution; a quantity with units and projection/residual; and retrieval/use under changed context or permission. Use the 18-family design in [EXPERIMENTS.md](EXPERIMENTS.md) and record actual coverage. For each selected distinction include a valid case, a materially changed adverse case and an irrelevant-change control where meaningful. Choose cases for semantic coverage, not a decorative total.

Perform and record feasible exact analytic or local checks. Preserve inputs, code, environment, outputs and failures. Attribute any service run to its actual build/executor. An expected answer is not an observed output; a worked mathematical example is not a production benchmark. Do not fabricate runs to satisfy the preparation date.

**Acceptance:** each result links to a derivation or actual run; controls exercise the intended distinction; missing coverage is visible. If execution is unavailable, keep its protocol in Semantic Verification or a preparation file and do not call the unexecuted study finished. Conclusions remain within the actual evaluated cases.

## 4. Dependencies and coherent corpus links

Before Meaning Bridge, complete a bounded slice of Claim Atlas/Source Audit: locate the definitions, historical inputs and primary sources needed here. This is not completion of the whole historical audit. Record omissions and use only material actually inspected.

Draft order is Meaning Bridge, Semantic Bridge, Transformation Algebra, Semantic Geometry, Semantic Verification, Meaning Controls. Semantic Bridge uses Meaning Bridge's distinctions. Transformation Algebra and Semantic Geometry share Semantic Bridge's representation vocabulary and the existing semantic-objects definitions. Semantic Verification connects their claims to verification obligations. Meaning Controls exercises selected operations under that methodology. Evidence preparation may proceed alongside writing, but dependent conclusions need actual reviewed prerequisites.

Create a section-level integration map using defines, uses-definition, proves-under, operationalizes, illustrates, tests, limits and supersedes links. A reading link is not a proof dependency. Cross-reading or bibliographic cycles may be legitimate; circular justification is not. Do not convert every link into an execution prerequisite.

For every affected current document record the exact revision, definition/claim to update, anchors and checks. Intended reading order: human-meaning introduction; semantic objects/context; bridge; algebra; geometry and retrieval; verification; worked studies; then reuse and other applications.

After full manuscripts exist, reconcile the glossary, bibliography, source map, section READMEs, source register and catalogue as one coherent integration change. Preserve old citation paths and redirects. Do not add placeholder papers to the catalogue, silently renumber all prior work, or assume every existing link is wrong. Reconcile the first two edited papers rather than discarding them.

## 5. Scientific writing and visual presentation

Repository manuscripts remain English under current contribution rules; progress reports and editorial explanations are Russian. A full Russian scientific version requires a separate semantically reviewed translation. Interface language is not manuscript language. Figure labels are English; duplicate translations do not become conflicting canonical sources.

Use applicable writing-editor methods: audience/task definition, precise wording, preservation of facts/conditions/numbers, coherent paragraphs, depth and whole-result review. Select relevant skills, not promotional or business-writing operations merely because they exist. Record actual revisions/dependencies read. The toolkit's original Russian applied-writing scope requires an explicit bounded adaptation for English science; neither general effectiveness nor native execution is assumed.

Connect a readable explanation to the formal statement. Motivate notation before introducing it, define terms before use, follow important formulas with their meaning, and preserve negation, modality, quantifiers, units, exceptions, uncertainty and attribution. Shortening is not the target.

For papers: descriptive title, concise abstract, keywords, question/contribution, related work, definitions/assumptions, model/method, results/proofs, examples/counterexamples, discussion, limitations, conclusion and references. Adapt headings to the contribution rather than inventing results to fill a template. For specifications: purpose/scope, terminology, interfaces, requirements, state/failure behavior, compatibility, conformance and sources. For studies: question, cases, procedure, observations, analysis, limits and reproducibility.

The house review layout is single-column, with one H1, consistent numbered sections, readable type and paragraph spacing, captioned tables/figures and displayed important equations. Keep headings with following text, avoid manual whitespace alignment, repeat table headers where appropriate, and prevent clipping or tiny footnotes. Use selectable text, clear symbols, meaningful links and accessible reading order. Visually inspect every PDF page and HTML/mobile rendering; a successful build alone is insufficient. These are project choices, not compliance with an unspecified journal. A later submission uses the chosen venue's current official template and disclosure rules.

## 6. Acceptance and release stages

| Stage | Required output | Not established by this stage |
| --- | --- | --- |
| Source-ready | Fixed inputs, source/claim inventory, required primary references and open questions | Exhaustive knowledge of every related field |
| Draft-complete | Whole manuscript, examples, protected claims and change/source trace | Independent acceptance or deployed implementation |
| Self-checked | Whole-text reasoning review, structural/link/formula checks and actual local results | Independent review or general proof by enumeration |
| Independently reviewed | Another reviewer reads the exact version and gives substantive findings | External academic acceptance merely because an agent reviewed it |
| Corpus-integrated | Reviewed definitions/links, valid catalogue/metadata/registers and normal release checks | Live site or indexed availability |
| Site-verified | Deployed source/build, actual text/link readback and visual checks | Agent execution or universal permission to reuse the content |

Scientific review begins alongside preparation and completes before accepted scientific release. A public research draft is labeled as such. An unsupported claim is proved, narrowed, removed or explicitly conjectural; typography cannot repair its evidence.

Each document packet contains full text, input/output identity, claim register, source attribution, examples, protocol/result distinction, mechanical checks, findings and unresolved conditions. Keep private mail and source-book payloads out of public changes.

Use current publication/source/requirement-register checks and relevant formal/unit tests. New clauses and evidence need reviewed register entries. Preserve raw historical evidence. A new title or metadata version does not upgrade a protocol or an old assessment. Reports distinguish drafted, committed, merged, released, deployed and indexed.

## 7. Ownership and immediate actions

KC-Brain authors the six units, source/claim/integration maps, examples and available checks, then addresses findings. Agent-Brain supplies separate mathematical/integration review and counterarguments; an analytical contribution is not called independent review of itself. Neither Brain delegates writing merely because the work is large.

KC-SWE reconciles task bindings and performs only necessary server/build/register/implementation/site operations with prepared inputs. Agent-SWE provides narrowly requested integration facts or runs. Neither is assigned a new broad benchmark, grant change or production mutation by the existence of this plan.

Immediate sequence: save and communicate the plan; prepare Meaning Bridge; inspect its whole result; continue the remaining units in order under the user-directed workflow. Resume the general cosmetic pass only after the missing foundation package and coherent link map are available. Existing publication defect fixes, roadmap-site work and first-two-paper review/delivery are not cancelled.

This bounded package does not complete the 25-item roadmap. Larger empirical studies, universal human semantics, production-wide conformance and model-specific superiority remain separate unless actually established. No unattended all-document run is authorized by the preparation plan.

## 8. GitHub communication transition

The author directs new coordination through GitHub rather than the Drive mailbox. At initial inspection, private workspace migration PR #1824 was still a draft; its Git mailbox README described a snapshot pending activation. Do not write into that snapshot, change another migration writer's branch, process old imported mail as new work, or declare delivery before canonical publication.

Use GitHub coordination to relay this decision and resolve the active canon/branch. After verified activation, follow the merged canon's per-role inbox/archive paths, delivery keys and handling rules. No new Drive correspondence is requested. A PR conversation may hold a transition notice but is not automatically four delivered mailbox copies. Posting it does not establish task acceptance or review approval.
