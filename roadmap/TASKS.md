---
title: Knowledge Contract research and engineering work packages
sources: none
status: definitions-with-artifact-observations
updated: 2026-11-08
---

# Research and engineering work packages

These are executable task definitions, not completed research. Public RM identifiers are stable roadmap references, not Muneral IDs. Execution ownership, acceptance and state remain in the existing work graph; Workgraph Reconciliation reconciles the bindings. No deadline or completion is invented. Proposed priorities: Immediate = immediate transparency/release enablement; Next = next substantive research/verification; Expansion = subsequent expansion and integration. The original planning baseline was 6 November 2026. The dated artifact observations below supersede any impression that an existing document is still absent; execution states remain unverified in Muneral. Engineering availability was restored by the operator on 11 November 2026; see [Active Work](EXECUTION_STATUS.md).

KC-Brain and Agent-Brain retain analytical authorship, examples, scientific tests, interpretation and acceptance. SWE roles perform only the necessary server, task-registry, implementation or deployment operations with prepared inputs. A task naming SWE does not delegate scientific authorship. Each dependent task needs the named reviewed output, not closure of an entire research programme. Every task also uses the common evidence rules in [EXPERIMENTS.md](EXPERIMENTS.md).

The [dependency definition](dependencies.json) is the machine-readable companion. [ROADMAP.md](../ROADMAP.md) gives release boundaries, sequence and baseline sources. Task acceptance means the promised deliverable is complete; its scientific result may be negative or inconclusive.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-01"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="recover-the-claim-level-mathematical-crosswalk"></a>

## Claim Atlas: Recover the claim-level mathematical crosswalk

**Artifact observation (8 November 2026).** A selected corpus map exists; it is not an exhaustive accounting of historical claims.

**Priority:** Immediate · **Owner:** KC-Brain · **Required outputs:** none.

**Original gap (6 November 2026).** The source map is topical, not a complete accounting of historical definitions, laws and geometry proposals.

**Work.** Inventory all documents in the pinned current catalogue (31 at `0892eeb1`; historical baseline 30) by section and the historical I10/I12 leads. Map each relevant definition, proposition, counterexample and limitation to a current location or an explicit disposition. Separate absent exposition, unsupported claims, missing evidence and absent implementation; do not equate these gaps.

**Deliverables.** A version-pinned claim inventory, old-to-current crosswalk and gap ledger with source anchors.

**Acceptance.** Every inspected historical item has retained, revised, superseded, deferred or rejected disposition and rationale; unknown coverage remains explicit; a second architect checks omissions.

**Adversarial check.** Try to find a historical premise, exception or result not accounted for by the map; an omitted item reopens only the affected row.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-02"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="explain-and-publish-the-scope-of-each-verification-result"></a>

## Verification Records: Explain and publish the scope of each verification result

**Artifact observation (8 November 2026).** Bounded checker reports exist; a complete reviewed passport set is not established.

**Priority:** Immediate · **Owner:** KC-Brain · **Required outputs:** none.

**Original gap (6 November 2026).** Raw case totals can conceal the carrier, duplicated behaviors, arbitrary bounds and the distinction between a model and production code.

**Work.** Prepare a verification passport for each cited checker: exact program/hash, tested object, parameter space, enumeration formula, iteration bound, oracle, vacuous cases, observed verdicts and exclusions. Reconcile the graph-root 4096 cases with the different historical 16-cubed Boolean-function triples. Publish only original or cleared reproducible inputs.

**Deliverables.** Public reproducibility packets and per-claim verification passports; preserved historical reports.

**Acceptance.** A reviewer can derive each case count and rerun the named program; an arbitrary small bound is explained, not advertised as sufficient; all production imports or their absence are disclosed.

**Adversarial check.** Remove a necessary assumption and inject an implementation defect. A checker unable to detect the intended defect cannot support that assertion; same-code reruns are not independent validation.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-03"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="publish-the-research-roadmap-on-contract-place"></a>

## Roadmap Publication: Publish the research roadmap on Contract Place

**Artifact observation (8 November 2026).** Repository roadmap exists; this naming/status revision has not been deployed to the website.

**Current delivery observation (11 November 2026).** Knowledge Contract source `161a01afb1b756adf059ea2e1cbdd0dca29d83a2` was rebuilt and deployed through contract-place-site `1d29084ad34f42f4f5279acd9b4836eec9ee5565` (PR #34, deploy run 42985309321). KC-SWE reported byte-equivalent EN/RU/zh-Hans served roadmap pages after stripping the Cloudflare beacon; DEUS-Arcana reported its scoped check 5 PASS. These are attributed delivery observations, not new scientific admission, fresh Muneral reconciliation, or a proof that a later source edit is already served.

**Next revision boundary.** For a new source commit, rebuild the site from that exact pin, carry the changed source status into every localized roadmap, and inspect the new served readback after review/CI/deployment. Preserve the historical 8 November observation above.

**Priority:** Immediate · **Owner:** KC-SWE · **Required outputs:** none.

**Original gap (6 November 2026).** Readers need a visible separation between current results, known limits and planned research.

**Work.** Implement the prepared roadmap reading surface using the canonical repository files, the existing site build and its pinned source revision. Provide localized navigation, task anchors, priorities, dependencies and truthful delivery state. Follow SITE_DELIVERY.md; do not create a second independent task database.

**Deliverables.** A site PR, generated roadmap pages, navigation entry, deployment and readback receipt.

**Acceptance.** The deployed page identifies the exact source commit, shows all roadmap items and their definitions, preserves current paper routes, works on desktop/mobile and exposes no private execution data. The report includes real URLs, build/deploy identity and substantive content checks.

**Adversarial check.** Test a stale source pin, broken task anchor, missing task and blocked/no-evidence status. None may render as completed research.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-04"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="bind-roadmap-definitions-to-the-execution-work-graph"></a>

## Workgraph Reconciliation: Bind roadmap definitions to the execution work graph

**Artifact observation (8 November 2026).** Previously reported bindings are not a fresh Muneral reconciliation.

**Priority:** Immediate · **Owner:** KC-SWE · **Required outputs:** none.

**Original gap (6 November 2026).** Public roadmap IDs describe planned work; they are not verified task identities or execution status.

**Work.** Reconcile each item against existing Muneral work, including the existing editorial, validation and consumer tasks. Reuse or split existing scope without losing history; create only genuinely missing work items. Return actual IDs, owners and typed dependencies privately. Publish only a sanitized, timestamped status projection where supported.

**Deliverables.** A complete private RM-ID to real-work-item map and evidence-backed public status policy.

**Acceptance.** All 25 definitions resolve to existing or newly created real tasks, or an exact unresolved binding is named. No invented UUIDs, duplicate engineering dispatch or status inferred from mail delivery; dependencies match the roadmap graph.

**Adversarial check.** Attempt duplicate registration and conflicting status updates. Reconciliation preserves one execution authority and reports disagreement.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-05"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="write-the-foundations-from-human-meaning-to-usable-knowledge"></a>

## Meaning Bridge: Write the foundations: from human meaning to usable knowledge

**Artifact observation (8 November 2026).** The complete foundations introduction is in the catalogue with research-draft status.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Claim Atlas, Source Audit.

**Original gap (6 November 2026).** The corpus has semantic objects and conditional results but lacks a single accessible foundations treatment spanning human meaning and agent use.

**Work.** Draft a standalone introduction with scope, research questions and a terminology map. Separate expression, referent, proposition, intended meaning, context, interpretation, truth, justification, applicability and authorization. Trace human abstraction to explicit representation, formal interpretation, checked operation, knowledge storage and bounded agent use. State where ambiguity or judgment cannot be made deterministic by declaration.

**Deliverables.** A proposed foundations PAPER.md, examples, glossary changes and a map to existing papers; no automatic publication-catalogue promotion.

**Acceptance.** A new reader can follow one example end to end and locate all assumptions. Existing work and external ideas are credited. The text distinguishes definitions, conjectures, established arguments and implementation proposals.

**Adversarial check.** Use ambiguous intent, metaphor, context-dependent reference and conflicting norms to test whether the proposed account overclaims a universal reduction of human meaning.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-06"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="establish-related-work-and-the-boundary-of-novelty"></a>

## Source Audit: Establish related work and the boundary of novelty

**Artifact observation (8 November 2026).** PR67 contains historical bibliography triage; triage is not full reading of all primary sources.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Claim Atlas.

**Original gap (6 November 2026).** Standard mathematical constructions and project-specific integration need a transparent comparison with prior work.

**Work.** Review primary sources in semantics/pragmatics, model theory and logic, program correctness, abstraction, database views/provenance, conceptual or vector representations and knowledge graphs. Compare assumptions, operations and guarantees rather than matching names. Treat unavailable or unpublished material as unavailable, not a reconstructed authoritative theory.

**Deliverables.** A primary-source matrix, bibliography additions and a novelty/non-novelty statement for each proposed contribution.

**Acceptance.** Every borrowed definition or result has a specific attribution; unsupported priority or novelty claims are removed; external theories are not silently identified with KC.

**Adversarial check.** Seek earlier work that already supplies the claimed contribution; narrowing or abandoning a novelty claim is an acceptable result.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-07"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="specify-the-human-to-formal-semantic-bridge"></a>

## Semantic Bridge: Specify the human-to-formal semantic bridge

**Artifact observation (8 November 2026).** A separate bounded conversion specification remains planned.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Meaning Bridge.

**Original gap (6 November 2026).** The structure of a semantic object does not itself define a correct conversion of arbitrary language into computable content.

**Work.** Define a bounded typed representation with scoped negation, quantifiers, conditions, units, time, referents, attribution, alternatives, provenance and uncertainty. Specify candidate extraction separately from deterministic validation. Define abstract/concrete mappings, supported language fragments, loss accounting, computability limits and refusal or unresolved outcomes. Connect it to professional artifacts without treating a skill file as capability.

**Deliverables.** A representation/adapter specification, conversion contract and worked human-text to formal-object to artifact examples.

**Acceptance.** Each mapping has a declared domain/codomain, assumptions, loss record and executable checks where feasible; competing readings survive until justified resolution; unsupported constructs are not coerced into false precision.

**Adversarial check.** Find a text pair collapsed into the same representation despite different required actions, or a round trip that drops a mandatory qualifier.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-08"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="complete-the-profile-algebra-of-meaning-operations"></a>

## Transformation Algebra: Complete the profile algebra of meaning operations

**Artifact observation (8 November 2026).** The transformation paper has conditional results; the planned algebra extension is not thereby complete.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Claim Atlas, Source Audit, Semantic Bridge.

**Original gap (6 November 2026).** Operations exist, but a coherent family of carriers, partial domains and laws is not fully traced to all intended uses.

**Work.** Specify equivalence, entailment, conjunction/merge, common consequence, projection, residual, reconstruction, composition and transfer for named profiles. State partial domains, nonempty/consistent interpretations, representative independence, supported decision procedures and resource limits. Distinguish observation equivalence from identity and similarity; list laws that do not hold.

**Deliverables.** An algebra profile document, law register, proof obligations and bounded executable reference semantics.

**Acceptance.** Every operation has types, domain, semantics, at least one positive and adverse example, and an explicit proof/test status. A standard Boolean result is not relabeled as a new theory or a universal document operation.

**Adversarial check.** Attack domain congruence, noninjective reconstruction, incompatible observation interfaces, inconsistent premises, and claims of minimal residual size.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-09"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="build-practical-algebra-examples-and-adversarial-controls"></a>

## Meaning Cases: Build practical algebra examples and adversarial controls

**Artifact observation (8 November 2026).** Analytic and synthetic examples exist; a new independent benchmark is not established.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Semantic Bridge, Transformation Algebra, Falsification Register.

**Original gap (6 November 2026).** Small synthetic spaces do not provide a diverse test set of practically meaningful transformations.

**Work.** Instantiate the algebra families in EXPERIMENTS.md using original or licensed sources. Cover units, exceptions, roles, scoped negation, attributions, changing recipients, residuals, conflicting sources and cross-domain transfer. Preserve source anchors and both positive and minimally changed negative cases. Separate visible development cases from withheld evaluation cases.

**Deliverables.** A versioned algebra benchmark, independent annotations/oracles and a case-to-law coverage matrix.

**Acceptance.** Every required semantic phenomenon has an expected observation and a counterexample control; ambiguous cases have sets of permissible answers rather than fabricated single labels; coverage is reported by family, not just count.

**Adversarial check.** Have the independent architect construct unseen cases that defeat the proposed rule; retain failures, annotation disagreement and dataset leakage findings.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-10"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="maintain-proof-obligations-and-a-falsification-docket"></a>

## Falsification Register: Maintain proof obligations and a falsification docket

**Artifact observation (8 November 2026).** Scoped reviews and counterexamples exist; no complete project-wide falsification register is claimed.

**Priority:** Next · **Owner:** Agent-Brain · **Required outputs:** Claim Atlas.

**Original gap (6 November 2026).** A failed premise, failed implementation and counterexample to a theorem are different diagnoses.

**Work.** For every selected claim record quantifiers, assumptions, carrier, intended observation, proof route and attempted refutation. Classify evidence as deductive argument, bounded model, implementation regression or empirical comparison. A theorem counterexample satisfies all premises and violates the conclusion; premise-breaking cases test boundaries or conformance instead.

**Deliverables.** A claim/falsification register with adversarial cases, proof gaps and disposition rules.

**Acceptance.** Each major claim has a concrete attack and criterion for supported-within-scope, refuted, inconclusive or not measured. A verified counterexample forces correction/retraction of the affected claim, not a cosmetic roadmap note.

**Adversarial check.** Search for vacuous success, hidden policy vetoes, inconsistent carriers, circular oracles and quantifier changes. Report unsuccessful searches with their actual bounds.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-11"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="scale-bounded-checks-and-connect-them-to-implementation"></a>

## Scaled Checks: Scale bounded checks and connect them to implementation

**Artifact observation (8 November 2026).** Existing finite checks do not establish production or arbitrary-scale correctness; subsequent scoped runs need observed evidence.

**Priority:** Next · **Owner:** KC-SWE · **Required outputs:** Verification Records, Meaning Cases, Falsification Register.

**Original gap (6 November 2026).** Three-vertex enumeration and the fixed iteration limit do not establish large-graph or production correctness.

**Work.** Run the Brain-prepared plan with parameterized graph sizes, independent closure oracle, long chains/cycles, generated and mutation cases, and explicit deterministic budgets. Start with complete n=1..4 scope when feasible and use justified generated cases beyond it. Replace size-specific loop bounds only through reviewed implementation; separate model-only runs from tests importing actual code.

**Deliverables.** Versioned runner/results, mutation report, seed and environment manifest, time/resource measurements.

**Acceptance.** Counts are derived and regenerated; original 4096 cases remain reproducible; long-chain defects are detected; model-only, production and unexecuted scopes remain separate. Exhaustive n=5 is not an arbitrary release requirement.

**Adversarial check.** Inject missing-edge, early-stop, wrong-root, inconsistent-oracle and vacuous-case mutations; surviving mutants are reported and explained.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-12"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="develop-the-geometry-of-meaning-profile"></a>

## Semantic Geometry: Develop the geometry-of-meaning profile

**Artifact observation (8 November 2026).** A standalone current geometry manuscript remains planned.

**Current source observation (11 November 2026).** The [Meaning Geometry manuscript](../papers/geometry-of-semantic-representations/PAPER.md) is now present in source `main` at `0892eeb1` with `research-draft` status (paper blob `077c13ad7e8d47646cd04ed2bdbeadceef48f9e3`). The 8 November statement above is retained as dated history, not a current missing-file claim. Completion of the F04 draft does not establish independent full-package review, held-out geometry results or release acceptance.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Claim Atlas, Source Audit, Semantic Bridge.

**Original gap (6 November 2026).** Historical geometry arguments exist, but a current explicit and validated geometry profile is not established.

**Work.** Specify what points/regions represent, the embedding map and version, dimensions, context conditioning, similarity or distance, topology if used, and claimed invariants. State metric axioms only when proved or verified for the chosen definition; separate pseudometric, similarity and directed entailment. Define information loss and the limits of inverse interpretation.

**Deliverables.** A geometry research document with precise definitions, candidate claims, countermodels and an evaluation plan.

**Acceptance.** No geometric term is decorative: each has a carrier, operation and intended use. Similarity never grants truth, equivalence or authority by itself; no embedding is advertised as complete human meaning.

**Adversarial check.** Construct threshold nontransitivity, collisions, norm changes and context-dependent nearest-neighbor reversals; a contradiction narrows or rejects the affected claim.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-13"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="test-geometry-against-semantic-distinctions"></a>

## Geometry Evaluation: Test geometry against semantic distinctions

**Artifact observation (8 November 2026).** No new held-out geometry result is claimed.

**Priority:** Next · **Owner:** Agent-Brain · **Required outputs:** Meaning Cases, Falsification Register, Semantic Geometry.

**Original gap (6 November 2026).** Geometric similarity has not been validated against the distinctions required by concrete KC tasks.

**Work.** Prepare a frozen comparison of high-similarity contradictions and low-similarity equivalent expressions. Include negation, quantifier scope, units, numbers, actor swaps and context. Compare lexical, vector and formal/profile-aware routes. Calibrate thresholds only on development data; keep separate unseen evaluation and explicit coverage/refusal outcomes.

**Deliverables.** A geometry benchmark/protocol and a server-ready run packet; actual results supplied by the engineering executor.

**Acceptance.** Report unsafe equivalence/merge decisions, retrieval coverage, calibration and variability by phenomenon. Fix sample size, primary measures and confidence/uncertainty method before the held-out run; one favorable example is not a measured advantage.

**Adversarial check.** Search for a system that looks precise only because it refuses everything, learns test labels, or uses similarity as an unexamined correctness oracle.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-14"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="specify-hybrid-retrieval-without-semantic-overreach"></a>

## Hybrid Retrieval: Specify hybrid retrieval without semantic overreach

**Artifact observation (8 November 2026).** Architecture candidates do not establish a completed integrated consumer.

**Priority:** Next · **Owner:** Agent-Brain · **Required outputs:** Semantic Bridge, Semantic Geometry, Geometry Evaluation.

**Original gap (6 November 2026).** Candidate ranking and contract-based admissibility need a documented interface between the geometric and logical layers.

**Work.** Specify geometry/lexical retrieval as candidate generation, followed by source, scope, dependency, policy and semantic checks. Record ranking exclusions versus mandatory rejections. Define adapters to Scrutator without inventing new grants or namespaces. Retain an uncertainty/refusal route and a useful positive path.

**Deliverables.** A consumer interface/decision record and positive/adversarial fixtures with explicit handoff conditions.

**Acceptance.** A similar but incompatible record is not delivered as accepted knowledge; a valid record can complete the path; cost and recall losses of checks are measured separately.

**Adversarial check.** Attempt metadata-hash substitution, omitted dependency, misleading similarity, wrong reader and context-budget truncation.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-15"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="trace-theory-to-requirements-code-and-observations"></a>

## Theory Traceability: Trace theory to requirements, code and observations

**Artifact observation (8 November 2026).** The published claim-evidence index is bounded; a complete theory-to-live-code matrix remains open.

**Priority:** Next · **Owner:** Agent-Brain · **Required outputs:** Claim Atlas, Falsification Register.

**Original gap (6 November 2026).** Existing propositions, specifications, standalone checks and services are not connected by a complete verified map.

**Work.** For each selected property identify the exact definition/proposition, requirement ID, implementation function/build, tests, raw evidence and limits. Distinguish code read, component tested and live behavior observed. Mark specified-but-unimplemented operations explicitly; reuse existing consumer/readiness tasks rather than dispatch duplicates.

**Deliverables.** A versioned traceability matrix with missing links and bounded implementation requests.

**Acceptance.** Every claimed implemented guarantee has a resolvable source and appropriately scoped observation; a document next to a model does not count as enforcement.

**Adversarial check.** Follow an allegedly supported guarantee to an unrelated test, stale build, stub or unsupported representation; downgrade that row instead of treating the matrix as proof.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-16"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="run-production-representative-conformance-and-fault-tests"></a>

## Runtime Conformance: Run production-representative conformance and fault tests

**Artifact observation (8 November 2026).** No all-system production conformance verdict; subsequent scoped runs need actual evidence.

**Priority:** Next · **Owner:** Agent-SWE · **Required outputs:** Scaled Checks, Theory Traceability.

**Original gap (6 November 2026).** Finite reference checks do not establish that the deployed implementation enforces the same contract.

**Work.** Execute prepared fixtures against named actual builds in authorized environments. Exercise malformed data, unsupported profiles, missing dependencies, wrong subject/recipient, stale evidence and altered outputs; include positive controls and independent observable counters. Preserve secrets and unrelated environments.

**Deliverables.** Build-pinned execution reports, raw logs, input manifests, coverage and unresolved defects.

**Acceptance.** Every result names the exercised boundary and exact implementation; failures before a boundary do not verify later checks. No global conformance verdict from a subset.

**Adversarial check.** Mutate or bypass an actual gate and show the test observes the intended violation; zero downstream calls require a positive-path control.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-17"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="evaluate-extraction-ambiguity-and-source-fidelity"></a>

## Extraction Fidelity: Evaluate extraction, ambiguity and source fidelity

**Artifact observation (8 November 2026).** The transcription study does not measure unrestricted semantic extraction accuracy.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Semantic Bridge, Meaning Cases, Falsification Register.

**Original gap (6 November 2026).** Well-formed records do not show that all material semantic conditions were extracted from a source.

**Work.** Prepare independently annotated, rights-cleared tasks for extraction and transformation, with source coordinates, preserved alternatives and damage/uncertainty labels. Define omission, hallucination, attribution and operator-scope errors separately. Freeze the evaluation protocol before any model run and preserve human/agent reviewer roles honestly.

**Deliverables.** Annotation guide, evaluation split, source-bound reference answers and exact run plan.

**Acceptance.** Disagreement and inaccessible source regions remain visible; no producer-only judgment is called independent ground truth; deterministic validation is not confused with semantic completeness.

**Adversarial check.** Insert a crucial exception in a table, footnote, image or different chapter and test whether a structurally valid artifact silently loses it.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-18"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="demonstrate-accepted-knowledge-in-a-bounded-agent-task"></a>

## Agent Application: Demonstrate accepted knowledge in a bounded agent task

**Artifact observation (14 November 2026).** Agent Situation and Context Controls are research-draft artifacts in an Agent Application subprogramme. Finite checks, the draft engineering design, the planned LLM trial and production use have separate evidence boundaries. Advanced retrieval work remains separate from the baseline exact-consumer pilot.

**Priority:** Next · **Owner:** Agent-Brain · **Required outputs:** Hybrid Retrieval, Theory Traceability, Extraction Fidelity.

**Original gap (6 November 2026).** Prepared artifacts, indexed entries, exact retrieval and successful task use are separate stages.

**Work.** Prepare an advanced research demonstration of one accepted semantic artifact and its finite required closure, including the Hybrid Retrieval hybrid-retrieval interface, then reuse a suitable existing private consumer route for exact readback, complete context delivery and bounded task use. Bind source, representation, revision, purpose and assessment. Engineer executes only the required ingestion/service operations. Within this workstream, develop the [Agent Situation](../papers/agent-situation/PAPER.md) research draft on initialization, revision-sensitive changes and bounded context projection; keep the [nonnormative engineering design](agent-situation/ENGINEERING.md) separate from adopted specifications.

**Scope separation.** Agent Application is an advanced research extension whose own acceptance depends on Hybrid Retrieval, Theory Traceability and Extraction Fidelity. The existing Live Lab exact-consumer baseline has its own approved KCLIVE prerequisites and can supply earlier evidence without satisfying Agent Application. Do not alias the whole Agent Application task to that baseline or import geometry / hybrid-retrieval dependencies into an otherwise ready KCLIVE task. Link only an actually matching, reviewed output; keep both task identities and their distinct acceptance conditions. Agent Situation is a bounded research subprogramme here, not an additional roadmap task or a substitute for the parent workstream's prerequisites. Its finite controls and planned LLM trial have separate methods, denominators and evidence; neither a draft protocol nor an author-produced finite pass establishes production behavior.

**Deliverables.** An exact-byte handoff manifest, task output, assessment and trace across storage/retrieval/use. The Agent Situation subprogramme contributes a research-draft paper, the [Context Controls](../engineering/studies/agent-situation-controls/STUDY.md) finite-check study with actual run records, a draft engineering design and a separately labelled [LLM experiment plan](agent-situation/EXPERIMENT.md).

**Acceptance.** Whole-document returned bytes match accepted hashes; all mandatory dependencies are present; the actual output is evaluated. Native task-run authority is not inferred from ordinary-session use. For the Agent Situation subprogramme, source distinctions and limits are explicit; finite observations are reproducible from exact code and inputs; missing or changed state is not silently relabelled current; planned LLM measurements remain unexecuted until observed. Acceptance of these bounded artifacts does not declare the whole Agent Application workstream complete.

**Adversarial check.** Change one source, request, reader grant or dependency while retaining the old artifact; stale acceptance must not silently survive. The Agent Situation controls also examine omitted observations, contradictory or stale state and loss of a task-relevant distinction during context projection, with useful positive controls so blanket refusal is not counted as successful task performance.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-19"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="verify-current-use-authority-and-revision-races"></a>

## Current Authority: Verify current-use authority and revision races

**Artifact observation (8 November 2026).** Policies and candidate controls are not proof of a live authorization boundary.

**Priority:** Next · **Owner:** Agent-Brain · **Required outputs:** Falsification Register, Theory Traceability.

**Original gap (6 November 2026).** A recent check or TTL does not establish authorization at the protected operation or safe publication ordering.

**Work.** Specify a concrete admission point, supported snapshot/lease/lock assumptions, generation identity and revocation behavior. Prepare races involving check-then-revoke, slow-old-writer, lost/reordered invalidation and changed recipients. Reuse existing authority/readiness/install work and request only missing bounded observations.

**Deliverables.** A concurrency/failure model, test fixtures and a requirements-to-observation review.

**Acceptance.** The coordination mechanism is named and tested at its actual boundary; no native success from CONTRACT_MISSING; event deduplication is not presented as recovery of lost events.

**Adversarial check.** Force the interleaving that violates the claimed current-state property and check whether the implementation detects or prevents it.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-20"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="measure-practical-benefit-against-strong-alternatives"></a>

## Practical Utility: Measure practical benefit against strong alternatives

**Artifact observation (8 November 2026).** Six bounded studies are published; no general superiority or universal savings follows.

**Priority:** Expansion · **Owner:** KC-Brain · **Required outputs:** Runtime Conformance, Agent Application, Current Authority.

**Original gap (6 November 2026).** The corpus does not establish universal quality, latency or economic superiority.

**Work.** Design task-matched comparisons among no reuse, simple strong reuse, lexical/vector retrieval and contract-aware routes where applicable. Equalize required quality and authority. Account for preparation, storage, validation, retries, review and coordination without double counting. Choose sample size and uncertainty reporting before evaluation.

**Deliverables.** A preregistered comparison protocol and, after execution, complete results including ties and adverse outcomes.

**Acceptance.** Separate causal claims from observations, retain all declared outcomes and report when overhead exceeds benefit. No selection of only successful cached tasks.

**Adversarial check.** Test conditions where a simple baseline ties or wins and where safe rejection creates apparent speed improvements at the expense of usefulness.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-21"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="test-multilingual-multimodal-and-shifted-context-limits"></a>

## Cross-Language Meaning: Test multilingual, multimodal and shifted-context limits

**Artifact observation (8 November 2026).** Body translation drafts and a semantic cross-language benchmark are distinct deliverables.

**Priority:** Expansion · **Owner:** Agent-Brain · **Required outputs:** Semantic Geometry, Extraction Fidelity.

**Original gap (6 November 2026).** Language/genre and modality transfer cannot be inferred from one textual profile.

**Work.** Prepare paired cross-language and multimodal cases with independently checked references, including numeric notation, image legends, OCR damage, missing assets and changed professional context. Keep interface translation separate from manuscript translation. Bound intended use instead of promising universal transfer.

**Deliverables.** A robustness suite, profile applicability table and per-family report.

**Acceptance.** Failures and unresolved readings remain distinct; correlations across translated cases do not inflate independent sample counts; model/data versions and rights are recorded.

**Adversarial check.** Find a translation or visual normalization that leaves topical similarity unchanged but reverses a scoped condition or numerical interpretation.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-22"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="recover-historical-evidence-without-rewriting-history"></a>

## Evidence Recovery: Recover historical evidence without rewriting history

**Artifact observation (8 November 2026).** Retained evidence and documented historical recovery gaps coexist.

**Priority:** Next · **Owner:** KC-Brain · **Required outputs:** Claim Atlas.

**Original gap (6 November 2026).** Some historical programs/fixtures remain unavailable and source-rights constraints limit reproducibility.

**Work.** Audit the existing recovery inventory and cited reports; request only exact missing exports/logs from their owners. Preserve originals and hashes; distinguish recovered original, reconstructed view and new synthetic reproduction. Prepare public substitutes only when clearly labeled and appropriately licensed.

**Deliverables.** An updated recovery inventory, evidence provenance and permitted reproduction bundles.

**Acceptance.** Every gap has recovered, unavailable or superseded-by-new-study disposition; no invented past execution or retrospective alteration of raw data.

**Adversarial check.** Try to reproduce a historical conclusion from only available inputs; an inability is reported, not repaired by substituting a new result without disclosure.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-23"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="validate-editorial-skills-and-reader-comprehension"></a>

## Editorial Evaluation: Validate editorial skills and reader comprehension

**Artifact observation (8 November 2026).** The published single-section pilot reports a tie, not a measured general benefit.

**Priority:** Expansion · **Owner:** KC-Brain · **Required outputs:** Claim Atlas, Verification Records.

**Original gap (6 November 2026).** Russian applied-writing skills and a single-section tie do not establish English scientific-editing effectiveness.

**Work.** Define a bounded genre/language adaptation and protected-claim contract. Evaluate complete documents with separate scientific review and comprehension questions, and compare with a well-specified ordinary editing baseline where a benefit claim is intended. Preserve measured ties and unknown reader results.

**Deliverables.** An adaptation profile, edit trace, independent review and appropriately scoped comprehension study.

**Acceptance.** Critical conditions, negations, equations and citations are retained or explicitly corrected; readable does not mean shorter; author self-review is not called external peer review.

**Adversarial check.** Seek a clearer-sounding edit that turns sufficient conditions into necessary ones, deletes a qualifier or increases confidence without evidence.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-24"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="integrate-new-findings-through-versioned-research-updates"></a>

## Corpus Integration: Integrate new findings through versioned research updates

**Artifact observation (8 November 2026).** Typed reading maps exist; links are not proof and proposal pins are not a coherent release.

**Priority:** Expansion · **Owner:** KC-Brain · **Required outputs:** Claim Atlas, Falsification Register.

**Original gap (6 November 2026).** New theory and negative results need a controlled route back into papers, specifications, studies and appendices.

**Work.** For each completed work package prepare its claim-level impact set, corrected manuscript/specification/study, evidence links and historical compatibility mapping. Add new foundations or geometry papers to the catalogue only when actual reviewed documents exist. Preserve task outcome separately from scientific support.

**Deliverables.** Reviewed versioned changes, impact/review records and repository/site/index readback where applicable.

**Acceptance.** A positive, negative or inconclusive research outcome is accurately reflected in every affected claim; planned work is never cited as completed evidence. Integrate incrementally, not after the entire backlog.

**Adversarial check.** Check for stale downstream theorems, unsupported catalogue entries, rewritten old evidence or a site serving a different source commit.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.

<!-- markdownlint-disable-next-line MD033 -->
<a id="rm-25"></a>

<!-- markdownlint-disable-next-line MD033 -->
<a id="finish-the-bounded-editorial-publication-pass"></a>

## Editorial Release: Finish the bounded editorial publication pass

**Artifact observation (8 November 2026).** The current ten-paper reading catalogue has eight baseline papers and two foundations research drafts; historical editorial-pass counts remain distinct.

**Priority:** Immediate · **Owner:** KC-Brain · **Required outputs:** none.

**Original gap (6 November 2026).** Unlimited research expansion must not prevent a readable, scientifically honest release of the existing corpus.

**Work.** Freeze the current editorial inventory at the 31 documents of source main `0892eeb1` (retaining the historic 29-record snapshot as evidence), then review sections one document at a time with protected scientific content, genre-specific structure and exact repository changes. Include specifications, studies, glossary, bibliography and appendices. Repair material false claims locally; defer enrichment to this roadmap. Existing approved first/second-document publication work is preserved.

**Deliverables.** A finite per-document editorial checklist, reviewed changes and verified publication handoffs.

**Acceptance.** Each document has readable structure, correct attribution, intact or explicitly corrected claims, visible limitations, working references and actual site confirmation after release. No requirement to solve all meaning research first.

**Adversarial check.** Reject a pass that only looks scholarly, hides an unsupported result, lacks source traceability or treats successful typography/CI as scientific validation.

**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Authorized bounded engineering may proceed under current Muneral ownership and applicable review/CI/access gates; a task description does not itself grant release authority.
