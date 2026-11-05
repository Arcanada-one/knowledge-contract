---
name: "dependency-closure-and-package-delivery"
title: "Dependency closure, readable artifact layouts, and a pinned package replay"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Historical package evidence and a public exhaustive replay of a finite dependency graph."
study_type: "finite-graph-and-integration-evaluation"
review_state: "internally-reviewed"
---

# Dependency closure, readable artifact layouts, and a pinned package replay

## Abstract

A task package is useful only if selecting an artifact also delivers its required conditions and dependencies. This study examines that obligation in a frozen editorial knowledge package with 110 records and twelve skill roots. Its retained selftest matched 44 ordinary checks: 21 expected acceptances and 23 expected rejections. Two additional structural-boundary counterexamples were accepted as designed and are reported separately. The dependency portion exhaustively examined all 4,096 skill subsets and 24,576 one-step inclusion pairs, with no disagreement against a separate fixed-point implementation. A public replay reproduces that graph portion without distributing the source book. A later metadata calculation shows that the actual editorial request delivered 108 of 110 records, so the observed package does not demonstrate a small context. A separate migration report records preservation of all 110 payloads, and a pinned historical replay reproduced an unresolved preliminary decision. The results establish bounded graph, layout, and integration behavior, not semantic completeness or agent competence.

## The delivery problem

An editorial skill can depend on a rule, a condition under which that rule applies, an acceptance criterion, and a source fragment. Selecting only the top-level skill description can omit the qualification that makes its use appropriate. The consumer follows explicitly required dependencies and treats navigation separately. Avoiding arbitrary navigation is a design motivation; it is not evidence that this package is selective or economical. The retained package was derived from the supplied OCR representation of Ilyakhov and Sarycheva's *Пиши, сокращай*, identified in the [editorial-source note](../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input).

This study distinguishes three identities: the artifact's stable identity, the immutable content revision, and its human-readable path. A renamed folder need not create different knowledge. A changed condition cannot be dismissed as a cosmetic rename. The scientific obligations are developed in [Retrieval and context composition](../../../papers/retrieval-and-context-composition/PAPER.md), [Constrained transformations](../../../papers/constrained-transformations/PAPER.md), and [Revision and governance](../../../papers/revision-and-governance/PAPER.md).

## Model and algorithms

Let \(V\) be the fixed finite set of artifact records and \(D(v)\) the required dependencies of record \(v\). For selected roots \(S\), the intended closure is the least set \(C(S)\) satisfying

\[
S\subseteq C(S), \qquad v\in C(S)\Rightarrow D(v)\subseteq C(S).
\]

Only declared `required` groups with the `all` operator participate in this tested profile. An alternative-choice dependency would need another selection policy and is not silently interpreted as `all`. A dependency's identity, revision, expected type, and payload hash are checked when loading the original package. Unknown roots and cycles cause explicit rejection in the consumer.

The production-side algorithm performs depth-first traversal with separate active and completed sets. The reference implementation repeatedly computes

\[
S_{k+1}=S_k\cup\bigcup_{v\in S_k}D(v)
\]

until the set stops growing. On a finite graph, the latter terminates after at most \(|V|\) strict increases. The comparison examines agreement, idempotence, monotonicity, and the union equation for this declared dependency relation. These are graph properties; they do not state that the natural-language content has a complete semantic dependency model.

## Exhaustive finite checks

Twelve selectable skill roots yield \(2^{12}=4,096\) subsets. The selftest evaluates every subset, compares consumer closure with the separate reference, checks \(C(C(S))=C(S)\), and checks that the closure equals the union of the individual root closures. It also examines every pair formed by adding one absent skill. There are \(12\cdot2^{11}=24,576\) such pairs; each must satisfy inclusion of the smaller closure in the larger one.

The retained [finite-package selftest](evidence/finite-package-selftest.json) records no reference disagreements, idempotence failures, union failures, or monotonicity failures. Union, idempotence and monotonicity are consequences of least closure; the subset sweep mainly checks their implementation on this fixed adjacency relation, rather than supplying thousands of distinct semantic observations. These counts are not independent samples of tasks and cannot be converted into a probability that arbitrary knowledge is complete.

The historical file contains 46 rows: 44 ordinary checks (21 expected acceptances and 23 expected rejections) and two accepted trust-boundary counterexamples. The latter are excluded from ordinary conformance, following the [common counting convention](../README.md#counting-and-interpretation). Additional controls include stale review bindings, a changed protected number, missing change grounds, a wrong source relation, an omitted critical qualification, another task's context, stale competency dependencies, attempted execution without supplied capability and authority, package tampering, and immutable receipt behavior. A synthetic positive review fixture is explicitly labeled as synthetic; it is not evidence that a real reviewer judged the text.

Two intentionally passing boundaries are especially informative. A structurally valid rule can state a false proposition. An output can contain the exact protected numeric string while negating its meaning. The checker accepted those inputs in the respective structural and literal-preservation checks. Therefore neither structural conformance nor exact string presence is a substitute for semantic review.

## A public reproduction of the graph result

The [dependency graph](evidence/dependency-graph.json) publishes required adjacency data and opaque vertex identities, with no artifact bodies, source passages, OCR, or book images. It was extracted after the original loader checked the frozen package's referenced records. Its source graph, index, and loader hashes are recorded in the file. The supplied [replay program](evidence/replay_closure.py) uses the original traversal rule and a separately written fixed-point comparison in the same publication workflow. This is algorithmic separation, not independent external replication.

From this study directory, run:

```bash
python3 evidence/replay_closure.py
```

The [saved public replay](evidence/public-closure-replay.json) reproduces 4,096 subset comparisons and 24,576 inclusion checks, and rejects an unknown root and a constructed cycle. This is a new replay of the extracted historical graph. It does not pretend to rerun all 46 historical checks, validate the source book, or observe a new model response. No additional Python packages or network calls are required.

## Delivered record counts and fault controls

The least-fixed-point background and the limited role of program mutation are identified in the [methodological references](../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods). The measurements below concern this retained finite graph and these declared faults.

The [post-review graph check](checks/check_closure_size_and_mutations.py) calculates closure sizes from the same 110-vertex, 405-edge graph. Its [saved output](checks/closure-size-and-mutation-check.json) includes every skill, both roles, both blueprints and the top-level agent root. Counts describe records, not bytes, tokens or attention cost. Human-readable names come from the retained path migration; the historical IDs remain in the machine result for traceability.

| Selected roots | Delivered records |
| --- | ---: |
| Individual skill roots | 45–57 out of 110 (40.9–51.8%) |
| All twelve skills together | 102 |
| Main editor role | 105 |
| Review role | 57 |
| Editing blueprint | 73 |
| Top-level assistant | 110 |
| Editorial pilot: editing blueprint plus both roles | 108 (98.2%) |

The twelve single-skill counts in historical selector order are 45, 57, 45, 49, 53, 51, 51, 47, 49, 55, 53 and 45; the output maps each count to a readable name. The pilot declared five applied skills out of twelve delivered. This is no demonstration that dependency closure produces a compact task context. It establishes delivery of the declared closure; whether dependency granularity and role-level roots can reduce package size remains unmeasured.

The same new check tests three explicit implementation mutations: omitting cycle rejection, skipping a required child, and treating an unknown root as a leaf. A two-node cycle, a three-node chain and an unknown-root control distinguish all three mutants from the unchanged traversal. These are post-review synthetic fault controls, separate from the historical 44 ordinary checks and two boundary counterexamples. They show sensitivity to those three defects, not general mutation adequacy.

```bash
python3 checks/check_closure_size_and_mutations.py
```

## Readable layout migration

The later editorial toolkit layout replaced code-like filenames with descriptive paths while retaining the underlying artifact identities and payload revisions. The [preservation report](evidence/layout-preservation-report.json) records the migration tool's assertion of byte equality for all 110 records and unchanged source bytes. Each row stores one hash and `bytes_equal: true`, not two separately observed old/new hashes. Thus the report alone cannot independently re-establish both byte sequences. Old and new paths are listed explicitly, so a reader can distinguish reported relocation from revision; the original report is preserved without adding invented observations.

The [layout conformance report](evidence/layout-conformance-report.json) records nine successful tests. Its positive inventory includes 110 document passports, 110 records, twenty operational closures, four constraints, 163 Markdown files, 1,294 local links, and 24 adapters. These are different inventory units and are not added into a single success rate. Other checks examine alias equivalence, forty source locators, and delivery of constraints as critical content.

Negative controls remove a constraint passport, remove a required constraint from delivery, introduce an invalid slug, break a link while updating its file hash, and create disagreement between the index and registry. Each is rejected by the expected diagnostic family. The updated-hash broken-link control is a useful counterexample: internally consistent checksums do not imply usable navigation.

## Historical package replay

An integration gate was pinned to the earlier package, not to the later layout. Reusing that gate against changed folder membership would compare different targets. The retained [historical replay](evidence/historical-package-replay.json) instead used the exact earlier target manifest and [declared environment](evidence/historical-replay-environment.json). The five command exits matched their expected sequence: 0, 0, 0, 3, 0. The source and temporary replay copy each retained all 239 checked payload files unchanged.

The exit of 3 belonged to preliminary admission. Its expected decision was `needs_resolution`, with `R_EXPECTED_HEAD` as the resolution code. Reproducing that decision means the gate reproduced the specified unresolved condition. It does not mean the package was accepted by a server. The record explicitly reports no new model runs, no new text outcomes, no external semantic review, server admission not evaluated, and production readiness false.

The recorded environment was Python 3.12.14 on Linux with five exact dependency versions. That environment claim belongs to the pinned historical replay. The later layout also has dependencies with version ranges; matching the earlier environment does not establish an exact later environment.

## Claim, evidence, and boundary

| Claim | Evidence | Counterexample or failure control | Limit |
| --- | --- | --- | --- |
| Required closure follows the declared graph | Exhaustive subset replay and separately implemented fixed point | Unknown root, cycle and three new implementation mutants | Completeness of the declared graph is an external premise |
| The migration tool reports unchanged content | 110 equality assertions, with one hash per row | Layout/index disagreement | Both old and new byte sequences are not separately pinned in that report |
| Constraints are actually delivered | Explicit critical-constraint checks | Missing passport and missing delivery | Only the four declared constraints are covered |
| A matching package hash means the package is usable | Navigation and preliminary-admission checks | Broken link with updated hash; unresolved expected head | Integrity, navigation, and admission remain separate |
| Exact strings imply preserved meaning | Deliberately negative meaning with the same numeric string | The literal check accepts it | A semantic reviewer remains necessary |

## Conclusion

This study provides a reproducible finite dependency result and inspectable layout and package-replay records. It shows how readable artifact names can coexist with stable identity, and how constraints can remain visible in the delivered closure. It also preserves the failure boundaries that make these results interpretable: a complete graph traversal may follow an incomplete annotation; almost the whole package may be delivered; an intact package may require resolution; a string-preserving edit may change meaning. The [editorial pilot](../editorial-skill-pilot/STUDY.md) evaluates actual text separately. Definitions are collected in the [glossary](../../../reference/glossary/GLOSSARY.md).

The original report identities remain in [origin.json](evidence/origin.json). The evidence is mostly English-keyed JSON, with retained Russian descriptions where present; its [language index](../evidence-language-index.json) identifies individual files. The prose above supplies English summaries of the false-rule and reversed-meaning controls. The newly generated graph measurements and mutation outcomes are identified separately in the [correction record](../review-corrections.json).
