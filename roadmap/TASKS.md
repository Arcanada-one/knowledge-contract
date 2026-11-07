---
title: Knowledge Contract research and engineering work packages
sources: none
status: planned
updated: 2026-11-06
---

# Research and engineering work packages

These are executable task definitions, not completed research. Public RM identifiers are stable roadmap references, not Muneral IDs. Execution ownership, acceptance and state remain in the existing work graph; RM-04 reconciles the bindings. No deadline or completion is invented. Proposed priorities: P0 = immediate transparency/release enablement; P1 = next substantive research/verification; P2 = subsequent expansion and integration. All tasks begin as **planned, execution unverified**.

KC-Brain and Agent-Brain retain analytical authorship, examples, scientific tests, interpretation and acceptance. SWE roles perform only the necessary server, task-registry, implementation or deployment operations with prepared inputs. A task naming SWE does not delegate scientific authorship. Each dependent task needs the named reviewed output, not closure of an entire research programme. Every task also uses the common evidence rules in [EXPERIMENTS.md](EXPERIMENTS.md).

The [dependency definition](dependencies.json) is the machine-readable companion. [ROADMAP.md](../ROADMAP.md) gives release boundaries, sequence and baseline sources. Task acceptance means the promised deliverable is complete; its scientific result may be negative or inconclusive.

## RM-01

### Recover the claim-level mathematical crosswalk

**Priority:** P0 · **Owner:** KC-Brain · **Required outputs:** none.

**Gap.** The source map is topical, not a complete accounting of historical definitions, laws and geometry proposals.

**Work.** Inventory all 29 catalogue documents by section and the historical I10/I12 leads. Map each relevant definition, proposition, counterexample and limitation to a current location or an explicit disposition. Separate absent exposition, unsupported claims, missing evidence and absent implementation; do not equate these gaps.

**Deliverables.** A version-pinned claim inventory, old-to-current crosswalk and gap ledger with source anchors.

**Acceptance.** Every inspected historical item has retained, revised, superseded, deferred or rejected disposition and rationale; unknown coverage remains explicit; a second architect checks omissions.

**Adversarial check.** Try to find a historical premise, exception or result not accounted for by the map; an omitted item reopens only the affected row.

**Start boundary.** Ready for Brain analysis now; no server or full-corpus experiment is required.

## RM-02

### Explain and publish the scope of each verification result

**Priority:** P0 · **Owner:** KC-Brain · **Required outputs:** none.

**Gap.** Raw case totals can conceal the carrier, duplicated behaviors, arbitrary bounds and the distinction between a model and production code.

**Work.** Prepare a verification passport for each cited checker: exact program/hash, tested object, parameter space, enumeration formula, iteration bound, oracle, vacuous cases, observed verdicts and exclusions. Reconcile the graph-root 4096 cases with the different historical 16-cubed Boolean-function triples. Publish only original or cleared reproducible inputs.

**Deliverables.** Public reproducibility packets and per-claim verification passports; preserved historical reports.

**Acceptance.** A reviewer can derive each case count and rerun the named program; an arbitrary small bound is explained, not advertised as sufficient; all production imports or their absence are disclosed.

**Adversarial check.** Remove a necessary assumption and inject an implementation defect. A checker unable to detect the intended defect cannot support that assertion; same-code reruns are not independent validation.

**Start boundary.** Brain prepares the explanatory records now; KC-SWE later executes the exact prepared public packet on the required host.

## RM-03

### Publish the research roadmap on Contract Place

**Priority:** P0 · **Owner:** KC-SWE · **Required outputs:** none.

**Gap.** Readers need a visible separation between current results, known limits and planned research.

**Work.** Implement the prepared roadmap reading surface using the canonical repository files, the existing site build and its pinned source revision. Provide localized navigation, task anchors, priorities, dependencies and truthful delivery state. Follow SITE_DELIVERY.md; do not create a second independent task database.

**Deliverables.** A site PR, generated roadmap pages, navigation entry, deployment and readback receipt.

**Acceptance.** The deployed page identifies the exact source commit, shows all roadmap items and their definitions, preserves current paper routes, works on desktop/mobile and exposes no private execution data. The report includes real URLs, build/deploy identity and substantive content checks.

**Adversarial check.** Test a stale source pin, broken task anchor, missing task and blocked/no-evidence status. None may render as completed research.

**Start boundary.** Ready for the necessary site/server work after reconciling existing tasks and the reviewed source PR; no completed theory is a prerequisite.

## RM-04

### Bind roadmap definitions to the execution work graph

**Priority:** P0 · **Owner:** KC-SWE · **Required outputs:** none.

**Gap.** Public roadmap IDs describe planned work; they are not verified task identities or execution status.

**Work.** Reconcile each item against existing Muneral work, including the existing editorial, validation and consumer tasks. Reuse or split existing scope without losing history; create only genuinely missing work items. Return actual IDs, owners and typed dependencies privately. Publish only a sanitized, timestamped status projection where supported.

**Deliverables.** A complete private RM-ID to real-work-item map and evidence-backed public status policy.

**Acceptance.** All 25 definitions resolve to existing or newly created real tasks, or an exact unresolved binding is named. No invented UUIDs, duplicate engineering dispatch or status inferred from mail delivery; dependencies match the roadmap graph.

**Adversarial check.** Attempt duplicate registration and conflicting status updates. Reconciliation preserves one execution authority and reports disagreement.

**Start boundary.** Ready for the narrow registry operation now; task creation is not permission to run every research experiment.

## RM-05

### Write the foundations: from human meaning to usable knowledge

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-01, RM-06.

**Gap.** The corpus has semantic objects and conditional results but lacks a single accessible foundations treatment spanning human meaning and agent use.

**Work.** Draft a standalone introduction with scope, research questions and a terminology map. Separate expression, referent, proposition, intended meaning, context, interpretation, truth, justification, applicability and authorization. Trace human abstraction to explicit representation, formal interpretation, checked operation, knowledge storage and bounded agent use. State where ambiguity or judgment cannot be made deterministic by declaration.

**Deliverables.** A proposed foundations PAPER.md, examples, glossary changes and a map to existing papers; no automatic publication-catalogue promotion.

**Acceptance.** A new reader can follow one example end to end and locate all assumptions. Existing work and external ideas are credited. The text distinguishes definitions, conjectures, established arguments and implementation proposals.

**Adversarial check.** Use ambiguous intent, metaphor, context-dependent reference and conflicting norms to test whether the proposed account overclaims a universal reduction of human meaning.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-06

### Establish related work and the boundary of novelty

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-01.

**Gap.** Standard mathematical constructions and project-specific integration need a transparent comparison with prior work.

**Work.** Review primary sources in semantics/pragmatics, model theory and logic, program correctness, abstraction, database views/provenance, conceptual or vector representations and knowledge graphs. Compare assumptions, operations and guarantees rather than matching names. Treat unavailable or unpublished material as unavailable, not a reconstructed authoritative theory.

**Deliverables.** A primary-source matrix, bibliography additions and a novelty/non-novelty statement for each proposed contribution.

**Acceptance.** Every borrowed definition or result has a specific attribution; unsupported priority or novelty claims are removed; external theories are not silently identified with KC.

**Adversarial check.** Seek earlier work that already supplies the claimed contribution; narrowing or abandoning a novelty claim is an acceptable result.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-07

### Specify the human-to-formal semantic bridge

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-05.

**Gap.** The structure of a semantic object does not itself define a correct conversion of arbitrary language into computable content.

**Work.** Define a bounded typed representation with scoped negation, quantifiers, conditions, units, time, referents, attribution, alternatives, provenance and uncertainty. Specify candidate extraction separately from deterministic validation. Define abstract/concrete mappings, supported language fragments, loss accounting, computability limits and refusal or unresolved outcomes. Connect it to professional artifacts without treating a skill file as capability.

**Deliverables.** A representation/adapter specification, conversion contract and worked human-text to formal-object to artifact examples.

**Acceptance.** Each mapping has a declared domain/codomain, assumptions, loss record and executable checks where feasible; competing readings survive until justified resolution; unsupported constructs are not coerced into false precision.

**Adversarial check.** Find a text pair collapsed into the same representation despite different required actions, or a round trip that drops a mandatory qualifier.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-08

### Complete the profile algebra of meaning operations

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-01, RM-06, RM-07.

**Gap.** Operations exist, but a coherent family of carriers, partial domains and laws is not fully traced to all intended uses.

**Work.** Specify equivalence, entailment, conjunction/merge, common consequence, projection, residual, reconstruction, composition and transfer for named profiles. State partial domains, nonempty/consistent interpretations, representative independence, supported decision procedures and resource limits. Distinguish observation equivalence from identity and similarity; list laws that do not hold.

**Deliverables.** An algebra profile document, law register, proof obligations and bounded executable reference semantics.

**Acceptance.** Every operation has types, domain, semantics, at least one positive and adverse example, and an explicit proof/test status. A standard Boolean result is not relabeled as a new theory or a universal document operation.

**Adversarial check.** Attack domain congruence, noninjective reconstruction, incompatible observation interfaces, inconsistent premises, and claims of minimal residual size.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-09

### Build practical algebra examples and adversarial controls

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-07, RM-08, RM-10.

**Gap.** Small synthetic spaces do not provide a diverse test set of practically meaningful transformations.

**Work.** Instantiate the algebra families in EXPERIMENTS.md using original or licensed sources. Cover units, exceptions, roles, scoped negation, attributions, changing recipients, residuals, conflicting sources and cross-domain transfer. Preserve source anchors and both positive and minimally changed negative cases. Separate visible development cases from withheld evaluation cases.

**Deliverables.** A versioned algebra benchmark, independent annotations/oracles and a case-to-law coverage matrix.

**Acceptance.** Every required semantic phenomenon has an expected observation and a counterexample control; ambiguous cases have sets of permissible answers rather than fabricated single labels; coverage is reported by family, not just count.

**Adversarial check.** Have the independent architect construct unseen cases that defeat the proposed rule; retain failures, annotation disagreement and dataset leakage findings.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-10

### Maintain proof obligations and a falsification docket

**Priority:** P1 · **Owner:** Agent-Brain · **Required outputs:** RM-01.

**Gap.** A failed premise, failed implementation and counterexample to a theorem are different diagnoses.

**Work.** For every selected claim record quantifiers, assumptions, carrier, intended observation, proof route and attempted refutation. Classify evidence as deductive argument, bounded model, implementation regression or empirical comparison. A theorem counterexample satisfies all premises and violates the conclusion; premise-breaking cases test boundaries or conformance instead.

**Deliverables.** A claim/falsification register with adversarial cases, proof gaps and disposition rules.

**Acceptance.** Each major claim has a concrete attack and criterion for supported-within-scope, refuted, inconclusive or not measured. A verified counterexample forces correction/retraction of the affected claim, not a cosmetic roadmap note.

**Adversarial check.** Search for vacuous success, hidden policy vetoes, inconsistent carriers, circular oracles and quantifier changes. Report unsuccessful searches with their actual bounds.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-11

### Scale bounded checks and connect them to implementation

**Priority:** P1 · **Owner:** KC-SWE · **Required outputs:** RM-02, RM-09, RM-10.

**Gap.** Three-vertex enumeration and the fixed iteration limit do not establish large-graph or production correctness.

**Work.** Run the Brain-prepared plan with parameterized graph sizes, independent closure oracle, long chains/cycles, generated and mutation cases, and explicit deterministic budgets. Start with complete n=1..4 scope when feasible and use justified generated cases beyond it. Replace size-specific loop bounds only through reviewed implementation; separate model-only runs from tests importing actual code.

**Deliverables.** Versioned runner/results, mutation report, seed and environment manifest, time/resource measurements.

**Acceptance.** Counts are derived and regenerated; original 4096 cases remain reproducible; long-chain defects are detected; model-only, production and unexecuted scopes remain separate. Exhaustive n=5 is not an arbitrary release requirement.

**Adversarial check.** Inject missing-edge, early-stop, wrong-root, inconsistent-oracle and vacuous-case mutations; surviving mutants are reported and explained.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-12

### Develop the geometry-of-meaning profile

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-01, RM-06, RM-07.

**Gap.** Historical geometry arguments exist, but a current explicit and validated geometry profile is not established.

**Work.** Specify what points/regions represent, the embedding map and version, dimensions, context conditioning, similarity or distance, topology if used, and claimed invariants. State metric axioms only when proved or verified for the chosen definition; separate pseudometric, similarity and directed entailment. Define information loss and the limits of inverse interpretation.

**Deliverables.** A geometry research document with precise definitions, candidate claims, countermodels and an evaluation plan.

**Acceptance.** No geometric term is decorative: each has a carrier, operation and intended use. Similarity never grants truth, equivalence or authority by itself; no embedding is advertised as complete human meaning.

**Adversarial check.** Construct threshold nontransitivity, collisions, norm changes and context-dependent nearest-neighbor reversals; a contradiction narrows or rejects the affected claim.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-13

### Test geometry against semantic distinctions

**Priority:** P1 · **Owner:** Agent-Brain · **Required outputs:** RM-09, RM-10, RM-12.

**Gap.** Geometric similarity has not been validated against the distinctions required by concrete KC tasks.

**Work.** Prepare a frozen comparison of high-similarity contradictions and low-similarity equivalent expressions. Include negation, quantifier scope, units, numbers, actor swaps and context. Compare lexical, vector and formal/profile-aware routes. Calibrate thresholds only on development data; keep separate unseen evaluation and explicit coverage/refusal outcomes.

**Deliverables.** A geometry benchmark/protocol and a server-ready run packet; actual results supplied by the engineering executor.

**Acceptance.** Report unsafe equivalence/merge decisions, retrieval coverage, calibration and variability by phenomenon. Fix sample size, primary measures and confidence/uncertainty method before the held-out run; one favorable example is not a measured advantage.

**Adversarial check.** Search for a system that looks precise only because it refuses everything, learns test labels, or uses similarity as an unexamined correctness oracle.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-14

### Specify hybrid retrieval without semantic overreach

**Priority:** P1 · **Owner:** Agent-Brain · **Required outputs:** RM-07, RM-12, RM-13.

**Gap.** Candidate ranking and contract-based admissibility need a documented interface between the geometric and logical layers.

**Work.** Specify geometry/lexical retrieval as candidate generation, followed by source, scope, dependency, policy and semantic checks. Record ranking exclusions versus mandatory rejections. Define adapters to Scrutator without inventing new grants or namespaces. Retain an uncertainty/refusal route and a useful positive path.

**Deliverables.** A consumer interface/decision record and positive/adversarial fixtures with explicit handoff conditions.

**Acceptance.** A similar but incompatible record is not delivered as accepted knowledge; a valid record can complete the path; cost and recall losses of checks are measured separately.

**Adversarial check.** Attempt metadata-hash substitution, omitted dependency, misleading similarity, wrong reader and context-budget truncation.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-15

### Trace theory to requirements, code and observations

**Priority:** P1 · **Owner:** Agent-Brain · **Required outputs:** RM-01, RM-10.

**Gap.** Existing propositions, specifications, standalone checks and services are not connected by a complete verified map.

**Work.** For each selected property identify the exact definition/proposition, requirement ID, implementation function/build, tests, raw evidence and limits. Distinguish code read, component tested and live behavior observed. Mark specified-but-unimplemented operations explicitly; reuse existing consumer/readiness tasks rather than dispatch duplicates.

**Deliverables.** A versioned traceability matrix with missing links and bounded implementation requests.

**Acceptance.** Every claimed implemented guarantee has a resolvable source and appropriately scoped observation; a document next to a model does not count as enforcement.

**Adversarial check.** Follow an allegedly supported guarantee to an unrelated test, stale build, stub or unsupported representation; downgrade that row instead of treating the matrix as proof.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-16

### Run production-representative conformance and fault tests

**Priority:** P1 · **Owner:** Agent-SWE · **Required outputs:** RM-11, RM-15.

**Gap.** Finite reference checks do not establish that the deployed implementation enforces the same contract.

**Work.** Execute prepared fixtures against named actual builds in authorized environments. Exercise malformed data, unsupported profiles, missing dependencies, wrong subject/recipient, stale evidence and altered outputs; include positive controls and independent observable counters. Preserve secrets and unrelated environments.

**Deliverables.** Build-pinned execution reports, raw logs, input manifests, coverage and unresolved defects.

**Acceptance.** Every result names the exercised boundary and exact implementation; failures before a boundary do not verify later checks. No global conformance verdict from a subset.

**Adversarial check.** Mutate or bypass an actual gate and show the test observes the intended violation; zero downstream calls require a positive-path control.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-17

### Evaluate extraction, ambiguity and source fidelity

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-07, RM-09, RM-10.

**Gap.** Well-formed records do not show that all material semantic conditions were extracted from a source.

**Work.** Prepare independently annotated, rights-cleared tasks for extraction and transformation, with source coordinates, preserved alternatives and damage/uncertainty labels. Define omission, hallucination, attribution and operator-scope errors separately. Freeze the evaluation protocol before any model run and preserve human/agent reviewer roles honestly.

**Deliverables.** Annotation guide, evaluation split, source-bound reference answers and exact run plan.

**Acceptance.** Disagreement and inaccessible source regions remain visible; no producer-only judgment is called independent ground truth; deterministic validation is not confused with semantic completeness.

**Adversarial check.** Insert a crucial exception in a table, footnote, image or different chapter and test whether a structurally valid artifact silently loses it.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-18

### Demonstrate accepted knowledge in a bounded agent task

**Priority:** P1 · **Owner:** Agent-Brain · **Required outputs:** RM-14, RM-15, RM-17.

**Gap.** Prepared artifacts, indexed entries, exact retrieval and successful task use are separate stages.

**Work.** Prepare an advanced research demonstration of one accepted semantic artifact and its finite required closure, including the RM-14 hybrid-retrieval interface, then reuse a suitable existing private consumer route for exact readback, complete context delivery and bounded task use. Bind source, representation, revision, purpose and assessment. Engineer executes only the required ingestion/service operations.

**Scope separation.** RM-18 is an advanced research extension whose own acceptance depends on RM-14, RM-15 and RM-17. The existing Live Lab exact-consumer baseline has its own approved KCLIVE prerequisites and can supply earlier evidence without satisfying RM-18. Do not alias the whole RM-18 task to that baseline or import geometry / hybrid-retrieval dependencies into an otherwise ready KCLIVE task. Link only an actually matching, reviewed output; keep both task identities and their distinct acceptance conditions.

**Deliverables.** An exact-byte handoff manifest, task output, assessment and trace across storage/retrieval/use.

**Acceptance.** Whole-document returned bytes match accepted hashes; all mandatory dependencies are present; the actual output is evaluated. Native task-run authority is not inferred from ordinary-session use.

**Adversarial check.** Change one source, request, reader grant or dependency while retaining the old artifact; stale acceptance must not silently survive.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-19

### Verify current-use authority and revision races

**Priority:** P1 · **Owner:** Agent-Brain · **Required outputs:** RM-10, RM-15.

**Gap.** A recent check or TTL does not establish authorization at the protected operation or safe publication ordering.

**Work.** Specify a concrete admission point, supported snapshot/lease/lock assumptions, generation identity and revocation behavior. Prepare races involving check-then-revoke, slow-old-writer, lost/reordered invalidation and changed recipients. Reuse existing authority/readiness/install work and request only missing bounded observations.

**Deliverables.** A concurrency/failure model, test fixtures and a requirements-to-observation review.

**Acceptance.** The coordination mechanism is named and tested at its actual boundary; no native success from CONTRACT_MISSING; event deduplication is not presented as recovery of lost events.

**Adversarial check.** Force the interleaving that violates the claimed current-state property and check whether the implementation detects or prevents it.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-20

### Measure practical benefit against strong alternatives

**Priority:** P2 · **Owner:** KC-Brain · **Required outputs:** RM-16, RM-18, RM-19.

**Gap.** The corpus does not establish universal quality, latency or economic superiority.

**Work.** Design task-matched comparisons among no reuse, simple strong reuse, lexical/vector retrieval and contract-aware routes where applicable. Equalize required quality and authority. Account for preparation, storage, validation, retries, review and coordination without double counting. Choose sample size and uncertainty reporting before evaluation.

**Deliverables.** A preregistered comparison protocol and, after execution, complete results including ties and adverse outcomes.

**Acceptance.** Separate causal claims from observations, retain all declared outcomes and report when overhead exceeds benefit. No selection of only successful cached tasks.

**Adversarial check.** Test conditions where a simple baseline ties or wins and where safe rejection creates apparent speed improvements at the expense of usefulness.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-21

### Test multilingual, multimodal and shifted-context limits

**Priority:** P2 · **Owner:** Agent-Brain · **Required outputs:** RM-12, RM-17.

**Gap.** Language/genre and modality transfer cannot be inferred from one textual profile.

**Work.** Prepare paired cross-language and multimodal cases with independently checked references, including numeric notation, image legends, OCR damage, missing assets and changed professional context. Keep interface translation separate from manuscript translation. Bound intended use instead of promising universal transfer.

**Deliverables.** A robustness suite, profile applicability table and per-family report.

**Acceptance.** Failures and unresolved readings remain distinct; correlations across translated cases do not inflate independent sample counts; model/data versions and rights are recorded.

**Adversarial check.** Find a translation or visual normalization that leaves topical similarity unchanged but reverses a scoped condition or numerical interpretation.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-22

### Recover historical evidence without rewriting history

**Priority:** P1 · **Owner:** KC-Brain · **Required outputs:** RM-01.

**Gap.** Some historical programs/fixtures remain unavailable and source-rights constraints limit reproducibility.

**Work.** Audit the existing recovery inventory and cited reports; request only exact missing exports/logs from their owners. Preserve originals and hashes; distinguish recovered original, reconstructed view and new synthetic reproduction. Prepare public substitutes only when clearly labeled and appropriately licensed.

**Deliverables.** An updated recovery inventory, evidence provenance and permitted reproduction bundles.

**Acceptance.** Every gap has recovered, unavailable or superseded-by-new-study disposition; no invented past execution or retrospective alteration of raw data.

**Adversarial check.** Try to reproduce a historical conclusion from only available inputs; an inability is reported, not repaired by substituting a new result without disclosure.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-23

### Validate editorial skills and reader comprehension

**Priority:** P2 · **Owner:** KC-Brain · **Required outputs:** RM-01, RM-02.

**Gap.** Russian applied-writing skills and a single-section tie do not establish English scientific-editing effectiveness.

**Work.** Define a bounded genre/language adaptation and protected-claim contract. Evaluate complete documents with separate scientific review and comprehension questions, and compare with a well-specified ordinary editing baseline where a benefit claim is intended. Preserve measured ties and unknown reader results.

**Deliverables.** An adaptation profile, edit trace, independent review and appropriately scoped comprehension study.

**Acceptance.** Critical conditions, negations, equations and citations are retained or explicitly corrected; readable does not mean shorter; author self-review is not called external peer review.

**Adversarial check.** Seek a clearer-sounding edit that turns sufficient conditions into necessary ones, deletes a qualifier or increases confidence without evidence.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-24

### Integrate new findings through versioned research updates

**Priority:** P2 · **Owner:** KC-Brain · **Required outputs:** RM-01, RM-10.

**Gap.** New theory and negative results need a controlled route back into papers, specifications, studies and appendices.

**Work.** For each completed work package prepare its claim-level impact set, corrected manuscript/specification/study, evidence links and historical compatibility mapping. Add new foundations or geometry papers to the catalogue only when actual reviewed documents exist. Preserve task outcome separately from scientific support.

**Deliverables.** Reviewed versioned changes, impact/review records and repository/site/index readback where applicable.

**Acceptance.** A positive, negative or inconclusive research outcome is accurately reflected in every affected claim; planned work is never cited as completed evidence. Integrate incrementally, not after the entire backlog.

**Adversarial check.** Check for stale downstream theorems, unsupported catalogue entries, rewritten old evidence or a site serving a different source commit.

**Start boundary.** After the named dependency outputs are reviewed; design can start earlier without claiming them complete.

## RM-25

### Finish the bounded editorial publication pass

**Priority:** P0 · **Owner:** KC-Brain · **Required outputs:** none.

**Gap.** Unlimited research expansion must not prevent a readable, scientifically honest release of the existing corpus.

**Work.** Freeze the current editorial inventory at the 29 catalogue documents, then review sections one document at a time with protected scientific content, genre-specific structure and exact repository changes. Include specifications, studies, glossary, bibliography and appendices. Repair material false claims locally; defer enrichment to this roadmap. Existing approved first/second-document publication work is preserved.

**Deliverables.** A finite per-document editorial checklist, reviewed changes and verified publication handoffs.

**Acceptance.** Each document has readable structure, correct attribution, intact or explicitly corrected claims, visible limitations, working references and actual site confirmation after release. No requirement to solve all meaning research first.

**Adversarial check.** Reject a pass that only looks scholarly, hides an unsupported result, lacks source traceability or treats successful typography/CI as scientific validation.

**Start boundary.** The earlier roadmap-only checkpoint is superseded by [FOUNDATIONS_RELEASE_PLAN.md](FOUNDATIONS_RELEASE_PLAN.md) (§§1, 3, 7). For otherwise unassigned general editorial work, use that plan's F01–F06 preparation order and the precise "foundation package available" threshold defined in [ROADMAP.md](../ROADMAP.md) §2. This is a preparation priority, not a prerequisite that all research experiments, independent publications or the 25 RM tasks finish. Preserve the already authorized first-two-paper reviews and delivery, roadmap-site publication and material-defect fixes. Later explicit author instructions for particular existing papers take precedence over this default order; they do not waive scientific review, DCO, CI or site verification.
