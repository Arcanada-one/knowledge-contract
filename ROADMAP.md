---
title: Knowledge Contract research roadmap
sources: none
status: planned
updated: 2026-11-06
---

# Knowledge Contract research roadmap

**A bounded publication now; a transparent programme of research next.**

This roadmap separates two commitments: finish a readable and scientifically honest edition of the existing corpus, and develop missing foundations and verification without pretending that planned work is already evidence. It defines 25 work packages, priorities, acceptance conditions and adversarial checks. None of the future research results is asserted as completed.

Read the [task definitions](roadmap/TASKS.md), [dependency graph](roadmap/dependencies.json), [experiment and falsification plan](roadmap/EXPERIMENTS.md), and [Contract Place delivery specification](roadmap/SITE_DELIVERY.md).

## 1. Baseline and scope

The baseline is Knowledge Contract commit `717c43deb514adc5b40f76837e7ee0fb2da37102`. Its [publication catalogue](publication-catalog.json) contains 29 documents: eight papers, eleven engineering specifications, six studies, a glossary, a bibliography and two appendices. Editorial proposals already made for the first two papers are separate from this baseline; their current review and publication states need their own evidence. This roadmap does not rewrite those manuscripts or imply their deployment.

We are not starting from an absence of mathematics. [Semantic objects](papers/semantic-objects-and-context/PAPER.md) and [constrained transformations](papers/constrained-transformations/PAPER.md) already define objects, observations, conditional preservation, equivalence, composition and reconstruction. The [source map](appendices/source-map/APPENDIX.md) preserves earlier work, but its topical mapping is not a claim-by-claim completeness audit. Historical algebra/geometry drafts are research inputs, not automatically current normative authority.

The missing work includes a coherent introduction from human meaning to explicit computational abstractions; a fuller family of algebraic and geometric profiles; diversified examples and attempted refutations; and verified links from claims through requirements to actual code, deployment and useful task outcomes. Mathematical notation alone, a schema pass, a small exhaustive enumeration and a production observation have different evidential roles.

The scope is the Knowledge Contract scientific/engineering corpus and its agent/knowledge-base interfaces. It is not an instruction to restart a bulk conversion of third-party books. Existing source-derived skills may be used within declared applicability, rights and review limits.

## 2. Two tracks and a finite release rule

**Track A: editorial completion (RM-25).** Review the frozen catalogue document by document, including chapters, references and appendices. Improve research questions, contribution statements, definitions, argument order, examples, conclusions and typography. Preserve mathematical premises, normative identifiers and raw evidence; identify substantive corrections separately. Use genre-specific structures for papers, specifications and studies. Apply each accepted change to the owning repository, then verify the actual site output through the normal publishing workflow.

**Track B: research and engineering (RM-01 to RM-24).** Develop the missing materials as bounded work packages. A failed or inconclusive hypothesis is a valid research result when the method, evidence and consequence are reported honestly. It is not a reason to conceal the study or claim success.

New research does not automatically block Track A. A local release block is justified only when a known defect makes an affected assertion false or materially misleading, a required evidence/source/rights condition fails, or the document/site delivery is broken. Correct, narrow or explicitly withdraw that assertion; do not wait for a universal theory. Optional richer examples, larger tests and future geometry results remain roadmap items. Completion of the existing corpus is not completion of all future research.

The original roadmap-only restart checkpoint was superseded by the author's later [foundations-first manuscript plan](roadmap/FOUNDATIONS_RELEASE_PLAN.md) (§§1, 3 and 7). The default preparation order is F01 → F02 → F03 (a substantive revision at the existing transformation-paper path) → F04 → F05 → F06, with each subsequent document started only under an explicit user-directed step. F labels are manuscript units, not Muneral IDs; this preparation order is not an additional `requires_output` graph. Roadmap delivery (RM-03), existing first-two-paper review/publication and material-defect corrections remain independently authorized. Later direct author instructions to edit particular existing papers supersede the old roadmap-only hold for those papers; they must not be retroactively rejected.

For the default general editorial resumption, **foundation package available** means that all six units have complete substantive, inspectable manuscript candidates at their canonical paths (F03 changes the existing paper, F06 reports actual derived or executed cases rather than unperformed tests), and a version-pinned definitions/claims/sources/corpus-relations map records remaining uncertainties and conflicts. Availability does not mean that independent scientific reviews, merge, deployment, indexing, every future experiment or all 25 RM tasks have succeeded. Each scientific release still follows its own exact-revision review and publication controls; a newer explicit per-document author instruction may change the preparation order without changing these release controls.

## 3. Known gaps and work packages

| Gap or requested extension | Work packages | Nature of the gap |
| --- | --- | --- |
| Historical mathematical material is not mapped at claim level | RM-01, RM-22 | Traceability and evidence recovery |
| Finite counts lack sufficient explanation of carrier, bounds and implementation scope | RM-02, RM-11 | Reporting and verification design |
| Readers cannot see the planned programme and actual execution bindings | RM-03, RM-04 | Public communication and task reconciliation |
| No unified foundations treatment from human interpretation to bounded computable use | RM-05, RM-06, RM-07 | Exposition, research positioning and representation contract |
| Algebra profiles and practically diverse transformation examples are incomplete | RM-08, RM-09, RM-10 | Theory, examples and attempted refutation |
| Geometry is not yet a sufficiently explicit, validated current profile | RM-12, RM-13, RM-14 | Definitions, evaluation and retrieval interface |
| Specification and reference models do not establish deployed enforcement | RM-15, RM-16, RM-18, RM-19 | Traceability and runtime conformance |
| Correct extraction of material context and ambiguity is not established by record validity | RM-17, RM-21 | Source fidelity and robustness |
| General quality/cost benefit is not established | RM-20 | Controlled empirical comparison |
| Cross-language editorial effectiveness and comprehension remain bounded | RM-23 | Applicability and reader evaluation |
| Results need controlled integration without an endless publication hold | RM-24, RM-25 | Revision and finite editorial completion |

This is the currently identified scope, not a claim that no undiscovered gap exists. RM-01 refines the ledger without silently enlarging the frozen editorial release.

## 4. Priorities and dependency structure

P0 means immediate transparency or release enablement: RM-01, RM-02, RM-03, RM-04 and RM-25. P1 means next substantive foundations, algebra, geometry and verification work. P2 means subsequent robustness, comparisons and result integration. These are proposed ordering priorities, not dates or proof that a worker has started.

The machine graph has 25 nodes and 45 `requires_output` edges. An edge means that the named reviewed output is needed for acceptance or dependent execution. Preliminary reading and design may proceed earlier. Four `informs_not_blocks` links are advisory and do not create execution cycles. The graph does not mean that a whole upstream research programme must finish before a useful incremental result can be used.

The main research path is:

```text
Claim inventory -> related work -> human-meaning foundations -> formal bridge
    -> algebra profiles -> practical cases -> scaled checks -> conformance
    -> geometry profile -> geometry tests -> hybrid retrieval -> agent use
Claim inventory -> falsification docket -> theory/code/evidence trace
    -> runtime and revision checks -> controlled comparisons
```

These lines summarize the graph; [dependencies.json](roadmap/dependencies.json) is the exact edge definition. Site publication and task reconciliation run beside the research path. Editorial work is not dependent on completion of that path.

## 5. Ownership, tasks and status

KC-Brain owns foundations, mathematical interpretation, manuscript content and scientific acceptance. Agent-Brain owns integration analysis, the independent adversarial view and cross-component designs. Brains write and review the actual artifacts themselves. Engineers receive only necessary server, implementation, registry or deployment operations with prepared inputs and acceptance conditions.

The public `RM-xx` labels identify these definitions. They are not invented Muneral identifiers and do not establish execution status. Muneral remains the execution authority. RM-04 reconciles existing work and creates only missing items, retaining original task history. Its private binding report maps every public definition to actual work items or a precisely stated unresolved binding; no private identifiers, credentials, server locations or mail content need be published.

A public status update is a dated projection of actual task evidence. At this roadmap revision, task execution bindings are **not verified here** and research is **planned**. Do not label all items scheduled, in progress or completed merely because they are written down. Avoid unsupported completion percentages and fixed delivery dates. Public status values may include planned, active, under review, blocked, completed or deferred only with the corresponding dated source; unknown remains unknown.

Completing a task means delivering and assessing its promised output. A research output can refute the proposed hypothesis. Completion never means that a theory has become universally true.

## 6. Startable work

KC-Brain can begin RM-01 and RM-02 without waiting for a server. Agent-Brain can review the gap map and prepare the RM-10 adversarial docket from identified claims. KC-SWE can immediately reconcile the task graph (RM-04) and implement/publish the prepared roadmap surface (RM-03) under the repository and deployment rules. There is no broad instruction to delegate the theoretical work to SWE.

Later server runs require a finite prepared input packet: source/build pins, cases, permitted operations, expected evidence, budgets and negative controls. Do not run a new costly benchmark merely because its task exists. Reconcile the existing consumer, readiness, editorial and verification work before adding a duplicate.

## 7. Baseline sources and evidence boundaries

The baseline references are project documents, not new experiments:

- [Catalogue at the audited commit](https://github.com/Arcanada-one/knowledge-contract/blob/717c43deb514adc5b40f76837e7ee0fb2da37102/publication-catalog.json).
- [Semantic objects and applicability](https://github.com/Arcanada-one/knowledge-contract/blob/717c43deb514adc5b40f76837e7ee0fb2da37102/papers/semantic-objects-and-context/PAPER.md).
- [Transformations, composition, equivalence and residuals](https://github.com/Arcanada-one/knowledge-contract/blob/717c43deb514adc5b40f76837e7ee0fb2da37102/papers/constrained-transformations/PAPER.md).
- [Historical source map and explicit limits of consolidation](https://github.com/Arcanada-one/knowledge-contract/blob/717c43deb514adc5b40f76837e7ee0fb2da37102/appendices/source-map/APPENDIX.md).
- [Engineering claim/evidence index](engineering/studies/evidence-index.json) and [historical recovery inventory](engineering/studies/historical-recovery-gaps.json).
- [Operation contracts](engineering/specifications/contract-family/SPECIFICATION.md) and [semantic representations](engineering/specifications/semantic-types/SPECIFICATION.md).
- [Publication procedure](PUBLISHING.md), [contribution rules](CONTRIBUTING.md) and [site build contract](https://github.com/Arcanada-one/contract-place-site/blob/main/README.md). The site's actual build source must be pinned again during delivery; this mutable documentation link is not a deployment receipt.

The roadmap changes no theorem, wire profile, publication edition, allowlist or runtime permission. Proposed new foundations/geometry manuscripts enter the publication catalogue only after they exist and pass the relevant reviews.
