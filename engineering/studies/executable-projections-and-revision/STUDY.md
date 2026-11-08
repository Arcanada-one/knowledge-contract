---
name: "executable-projections-and-revision"
title: "Executable Projections: Addressable revisions and the limits of graph minimality"
short_title: "Executable Projections"
subtitle: "Addressable revisions and the limits of graph minimality"
previous_title: "Executable projections, addressable revisions, and the limits of graph minimality"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Finite consumer checks, paired agent tasks, addressed revision and the limits of graph minimality."
study_type: "finite-consumer-and-agent-case-study"
review_state: "internally-reviewed"
---

# Executable Projections: Addressable revisions and the limits of graph minimality

## Abstract

This report synthesizes three completed development stages: packet reading, targeted revision, and executable partial extraction. The first reader stage recorded twelve criterion violations and a reconstruction-status distribution of ten complete, 38 partial, three rejected and six unsupported main-layer results. A later development and regression boundary suite satisfied 772 declared checks across 38 calls under a revised reader and rubric. A targeted revision comparison produced equal outcomes on ten case templates instantiated for three books, yielding thirty graph-versus-row pairs. A consumer checked on 102 finite controls then extracted 24 prescribed projections from ten fresh agent responses organized as five related case pairs. Both representations succeeded on all five primary cases under a coarse rubric that reached its ceiling on the rated projections. These bounded results do not establish graph superiority or general semantic completeness. A post-hoc finding shows that a minimal set of reachable entities can still contain unnecessary claims inside entity text.

## Question and design progression

The engineering question is whether a consumer can retrieve a useful partial result without silently dropping its conditions, treating a new assessment as original provenance, or resolving an ambiguous identity by arbitrary order. The scientific arguments are developed in [Retrieval and context composition](../../../papers/retrieval-and-context-composition/PAPER.md), [Revision and governance](../../../papers/revision-and-governance/PAPER.md), and [Evidence and falsification](../../../papers/evidence-and-falsification/PAPER.md).

The stages changed interfaces, mappings, cases, and sometimes evaluation rules. They are therefore reported as related development studies. Their successive scores do not constitute a controlled estimate of improvement caused by one isolated intervention. Historical results remain unchanged.

## Initial reader: four distinct failure mechanisms

The retained [initial reader study](evidence/historical-reader-study-source.json) records 57 main-layer calls with 786 satisfied and twelve violated criteria. Their reconstruction statuses were ten complete, 38 partial, three rejected and six unsupported. These status labels are not interchangeable with satisfaction of all obligations. The public summary does not bind every main-layer status to a predeclared expected status, so it cannot establish which of the 38 partial and nine rejected/unsupported outcomes were planned rather than unexpected. That distinction remains unavailable at the case level.

The separate [book-layer report](../source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json) records eighteen calls with 252 satisfied and zero violated criteria: six base cases were complete and twelve deliberately damaged or incomplete controls were partial by design. Calls, reconstruction statuses and nested criteria are separate denominators; the criterion counts are not 1,050 independent tasks or an accuracy estimate. There were no native-model subject trials or human-subject trials in that stage.

The twelve violations fell into four groups. Five concerned the difference between an address resolving to a placeholder and content actually being available. Three concerned inconsistent derivation of revision identity between records and relation endpoints. Two concerned diagnostic pointers into a packet versus its transport envelope. Two concerned choosing the first candidate despite conflicting records.

| Original failure group | Recorded violations | Subsequent correction scope |
| --- | ---: | --- |
| Placeholder address versus available content | 5 | Contract/rubric distinction and reader change: separate address resolution from content state and availability |
| Inconsistent inferred revisions | 3 | Reader normalization and an explicit inference rule applied consistently to records and endpoints |
| Ambiguous pointer coordinate space | 2 | Diagnostic output and contract clarification: identify packet/envelope space and representation hash |
| First-candidate choice under conflict | 2 | Resolver behavior and output contract: retain the candidate set and explicit ambiguity |

This is an English summary of the original report's four-group analysis. It does not allocate each later success causally to code or rubric alone; both changed, particularly for the five placeholder cases.

This analysis matters because the violations do not all mean lost content. In the pointer cases, the invalid outer hash was detected, but the diagnostic coordinate system was ambiguous. In the placeholder cases, relationships were retained while the meaning of `resolved` differed between reader and oracle. Revising the explanation of these mechanisms does not erase the recorded violations.

## Revised reader boundaries

The later reader separated address resolution, content state, content availability, applicability, and authority. An empty supplied string, zero, or `false` was not treated as an absent field. A source-declared revision remained distinct from an inferred revision and its inference rule. Diagnostic pointers named their coordinate space and representation hash. Conflicting candidates remained an explicit set, so record order could not silently create unique identity.

The [boundary report](evidence/reader-boundary-report.json) contains 38 development calls: 26 counterexamples prepared alongside the revision and twelve regression cases from the earlier failures. All satisfied the declared checks, totaling 772 satisfied and zero violated criteria. A paired permutation control preserved ambiguity and the candidate-value hash set. The revised mapping and rubric differed from the earlier ones, so this was neither a held-out acceptance test nor an instrument-only retest. “Qualified” in the historical record means that these finite declared boundaries were checked; it does not establish correctness on arbitrary future packets.

## Targeted revision and a strong alternative

The [targeted revision report](evidence/targeted-revision-comparison.json) compares an explicit dependency graph with flat rows that contain the same material dependencies and conditions. Both use a shared evidence validator and serializer. The experimental difference is how affected records are selected. This is a deliberately strong simple alternative, not a form deprived of relevant information.

Ten distinct templates were instantiated for three books, producing thirty paired cases and sixty executions. All sixty produced the expected outcome; both representations agreed on all three book instances of every template. The shared validator and serializer restrict this comparison to the record-selection step and help explain equality once both selectors choose the same records. Thirty pairs are not thirty independently designed mechanisms.

| Template family | Paired book instances with equal outcomes |
| --- | ---: |
| No source or contract change | 3/3 |
| Valid representation map | 3/3 |
| Incorrect representation map | 3/3 |
| Missing representation map | 3/3 |
| Empty representation map | 3/3 |
| Changed source text | 3/3 |
| Changed image bytes | 3/3 |
| Required uncertainty preserved | 3/3 |
| Required uncertainty omitted | 3/3 |
| Required uncertainty unknown | 3/3 |

The outputs included 36 unresolved-mapping assessments and twelve unknown-contract assessments because those were declared outcomes of particular controls. These states are visible results, not failures concealed behind a pass total. The [addressability study source](evidence/addressability-study-source.json) describes the design and shared machinery; the machine comparison retains the per-template and per-book identities.

Source changes created separate candidate revisions and retained prior records and history. New assessments did not invent current-use authority. Timing was a single local invocation including shared decoding, not model latency or product cost. This comparison establishes no advantage for graph representation on the tested scope.

## Executable projection contract

The subsequent finite consumer accepts two representations of the same contract: nodes and typed edges, or rows with typed dependencies. It normalizes both and computes required closure from named roots. Relations distinguish content requirements, qualifications, and assessment requirements. Source attachments also distinguish content support from assessment basis. Evidence used to evaluate a card must not silently become the source from which the card's content was derived.

Typed identities carry record and revision identifiers, the contract of creation, and prior-version references. Assessments separately identify their exact target, assessment contract, and verdict. A request can include historical revisions in a separate history layer. Historical payloads and outgoing relations are preserved rather than edited to make an old record satisfy new rules.

Missing addresses, invalid sources, malformed input, or a closure exceeding the declared entity budget yield a blocked result with no usable partial output under this profile. An explicitly represented semantic unknown can remain useful content; it is not itself a schema failure. Minimality is relative to the declared relationships. The consumer cannot infer an omitted qualification merely because the author should have included it.

## Consumer qualification before the new responses

The [qualification report](evidence/consumer-qualification-report.json) records 51 control families in two forms: 102 executions, comprising 24 expected acceptances and 78 expected blocks. All matched, and normalized results agreed in all 51 pairs. A separately written verifier, which did not import the consumer, computed expected structural closure and rejected twelve deliberately damaged outputs. The verifier and consumer were developed within the same session and agent family. Separation of code paths is useful, but does not establish external independence or exclude shared assumptions.

Three pre-freeze corrections are disclosed. Invalid JSON types gained explicit guards; Python's equality between booleans and numbers could no longer mask a change in preserved JSON type; and normalized outputs explicitly retained relations and typed links. These changes preceded the new subject responses. The finite controls do not prove the consumer for every possible input or arbitrary non-JSON Python object.

## Five agent case pairs

The next stage fixed inputs, requests, reference material, rubric, implementations, and run order before obtaining ten responses in fresh agent contexts. There was one response per case and representation, with no corrective subject retry. The source-based tasks were deliberately related and comprise four source families, not ten independent samples.

| Case | Required preservation in a partial extraction | Observed result |
| --- | --- | --- |
| Unreviewed navigation description | Useful description together with uncertain notation and missing context | Both main projections retained the uncertainty and source limit |
| Experimental cooking revision | A changed branch, its prior value, and a distinct independent branch | Prescribed current, historical, and separate-branch extractions retained their respective bindings |
| Changed assessment contract | Original creation contract and prior verdict, new assessment, and a new qualified revision | Old provenance remained intact; new assessment and revision were separate |
| Navigation table | Selected values, interpolation basis, sign, and unknown applicability | Both forms retained the specified values and grounds in all prescribed views |
| Electrical diagram image | Visible block and connection structure without invented numerical signals | Both forms retained qualitative observations and limits of numerical inference |

The [measured-results record](evidence/agent-projection-results.json) reports 24 available projections checked by the separately written verifier described above. Each received the rubric's highest fidelity and task-correctness score: both axes were saturated across all 24 projections. Differences smaller than one score step could not be resolved by that instrument. All prescribed views succeeded in five of five cases for each form, with equal primary outcomes in all five pairs. The ten raw responses were different; equal outcome scores do not imply identical representations or equal quality under a more discriminating assessment.

The semantic reviewer saw the representation, participated in design review, and belonged to the same agent family. No human expert review occurred. There were 84 nested critical-obligation judgments; these are not 84 independent experiments. Exact runtime model revision, decoding, seed, token use, latency, and compute cost were unavailable. Saved outputs were copied from visible final answers rather than captured as native API streams. Therefore the study supplies an observed agent case series, not a reproducible native-model benchmark.

## Counterexample to claim-level minimality

After evaluation, two row-form projections were found to include extra numerical statements inside a shared applicability qualification. An extraction of one selected table value consequently carried another value even though the latter's dedicated calculation node was not selected. The extra values were correct, and the frozen rubric allowed additional correct information. The original scores were retained; the observation was recorded separately.

This is a counterexample to inferring claim-level minimality from entity-level closure. A minimal reachable node set does not imply that every sentence inside those nodes is necessary, or that every incidental claim has all of its own grounds in the projection. A later contract could give individual claims addresses or constrain the scope of shared qualifications. That refinement is an implication of the counterexample, not a property already demonstrated by this run.

## Evidence and reproduction boundaries

The exact machine summaries and retained source views accompany this study; [origin.json](evidence/origin.json) distinguishes original JSON bytes from reconstructed text views. The [offline replay report](evidence/offline-projection-replay-report.json) records one historical extracted-bundle replay in which all 24 projections matched and passed a separate verifier. It explicitly reports no new subject-model calls, OCR, native trials, or semantic assessments. That replay is deterministic processing of saved outputs.

This public evidence folder does not contain the complete original source packages, candidate responses and frozen requests, or the complete native runtime. In particular, the frozen synthetic control bundle, original consumer, separate verifier and mutation artifacts are not supplied. Their absence is an unresolved recovery and publication gap for project-authored material, not a claim that book rights prohibit publishing synthetic controls or software. Their bound hashes and byte lengths are listed in the [recovery inventory](../historical-recovery-gaps.json); recreating similar code would produce a new experiment, not restore the historical one. Readers can inspect retained counts and limitations, but cannot infer a complete replay environment from hashes. The [public closure study](../dependency-closure-and-package-delivery/STUDY.md) provides a separately executable graph mechanism using metadata-only inputs.

The [projection study source](evidence/projection-study-source.json), addressability source and initial reader source are Russian prose views. The design, four failure mechanisms, status distribution and limitations above are English summaries of their relevant passages; they are not a full independently reviewed translation. The [evidence language index](../evidence-language-index.json) identifies every file. Agent-judging limitations are related to the [evaluation-method references](../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods); this local rubric does not reproduce their benchmarks.

## Conclusion

The studies demonstrate finite preservation of explicitly declared content, qualifications, assessment roles, and history through selected retrieval and revision operations. They also identify useful counterarguments: simple representations can reach the same outcomes, a corrected evaluator changes the interpretation of scores, and graph minimality does not bound the number of claims inside text. These results support the explicit obligations of the contract while keeping comparative effectiveness, arbitrary-root completeness, domain correctness, and product authorization outside the established conclusion. Definitions are consolidated in the [glossary](../../../reference/glossary/GLOSSARY.md).
