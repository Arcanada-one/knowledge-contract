---
title: "Coherent Relations and Outcome Geometry: Bounded Engineering Review"
author: "Pavel Valentov and Knowledge Contract Arcana contributors"
language: en
license: "CC-BY-4.0"
sources:
  - "Knowledge Contract relational semantics controls"
status: "executed finite controls; candidate scientific extension; no external acceptance"
---

# Coherent Relations and Outcome Geometry: Bounded Engineering Review

## Problem and result

The existing transformation paper specified representative independence for deterministic partial functions but left the relation-valued criterion open. The geometry paper established deterministic preservation and incomplete-observation envelopes without a composition theorem for sets of possible transformation outcomes.

The candidate adds Proposition 4 to [Knowledge Transformations](../../papers/constrained-transformations/PAPER.md) and Proposition 7 to [Meaning Geometry](../../papers/geometry-of-semantic-representations/PAPER.md). Earlier proposition numbers, evidence and conclusions remain. The results are explicit applications of standard relation/powerset and finite Hausdorff constructions; no general mathematical priority or empirical superiority is claimed.

For a relation, the set of reachable output observations must be identical for every representative of an input observation class, including the empty set. This condition is necessary and sufficient for the exact quotient. Two coherent relations with the same intermediate profile compose exactly. Without that condition, existentially merging representatives can introduce an output or path absent from the concrete chain.

For compatible maps to finite nonempty outcome sets, Hausdorff distance gives a Lipschitz bound for union composition. Equal alternative sets have distance zero even when two individually realized outcomes could differ; this result does not replace the existing bounds over all completion pairs.

## Implementation and finite acceptance

[semantic_relations.py](../../tools/semantic_relations.py) supplies explicit finite partitions, relations, a counterexample witness, exact/coarse quotient operations, relational composition, exact rational metric validation, Hausdorff distance, union composition and the least finite Lipschitz bound. Its prototype carrier limit is 12 states, with actual integer state identifiers and exact `int`/`Fraction` distances. Booleans and float distances are rejected. The mathematical propositions do not acquire a twelve-state restriction from this implementation bound. Inputs must already be finite. This cardinality validation is not a bound on reading arbitrary iterators, execution time or memory; the API materializes iterable inputs before validating their size.

The [separately authored oracle](../../tools/test_semantic_relations.py) uses bit-mask Boolean rows and matrix composition instead of edge-set implementation helpers. It computes Hausdorff distance by the smallest radius giving mutual neighbourhood coverage, and searches exact possible Lipschitz bounds. It does not import private implementation helpers.

| Written obligation | Executed control | Observed scope |
| --- | --- | --- |
| Exact observation quotient, including absent successful outputs | Enumerate every 3×3 relation under partition `((0,1),(2,))`; validate each counterexample from the original edges | 512 relations: 160 coherent, 352 incoherent; one coherent empty relation and 133 coherent relations with every input image nonempty |
| Compatible coherent relations preserve successful composition | Compare concrete Boolean composition and quotient composition for every ordered coherent pair | 25,600 pairs; 649 empty composites and 24,951 nonempty composites; 20,021 have nonempty images for every source state |
| Exact set distance | Compare API and neighbourhood-coverage oracle on all nonempty subset pairs of `{0,1/2,1}` | 49 ordered pairs |
| Least finite Lipschitz constant | Enumerate all nonempty-valued maps on that metric carrier | 343 maps; constants 0/1/2 occur 7/182/154 times |
| Union composition and product bound | Compare composed images and test the bound for all ordered map pairs | 117,649 pairs; 40,345 equalities and 77,304 strict inequalities; 30,061 constant composites |
| Boundary sensitivity without an all-reject checker | Four explicit one-rule API-behaviour wrappers, each with a distinguishing adverse case and a preserved valid case | 4/4 detected and 4/4 positive controls preserved |

The negative wrappers omit the coherence guard, ignore empty representative images, use the closest pair in place of Hausdorff aggregation, or assign zero distance to an empty set. They are not an exhaustive source mutation campaign. Other API tests cover different class orderings, incompatible dimensions, invalid state aliases, invalid metrics and useful zero/tight positive bounds. All twelve unit tests pass in the recorded local check.

The executed [RESULTS.json](RESULTS.json) binds the implementation, oracle and runner bytes, Python version and actual counts. These are different complete finite spaces, not independent empirical trials to be summed. The initial oracle run was authored by a separate agent; the retained final run binds the integrated files. All contributors share the controller/model family/host.

## Reproduction

From the repository root:

```bash
python3 -B -m unittest tools.test_semantic_relations -v
python3 -B reviews/relational-semantics-20261114/run_finite_oracle.py \
  --repository . --output /tmp/kc-relational-semantics-new-run.json
```

Use a fresh output path. The runner refuses to overwrite an existing receipt and checks that implementation/oracle bytes did not change during the run. Its `base_commit` is the local checkout base, not a claim that all working files equal that commit. Per-file hashes identify the executed programs. [MANIFEST.json](MANIFEST.json) records the integration parent and exact candidate inputs without attempting a self-referential commit hash. Wall time is a local run observation, not a benchmark.

The combined [local gates](LOCAL_CHECKS.json) executed 113 tests: 93 existing publication/source/separation/DCO/CI tests, eight existing formal-result tests and twelve new API/oracle tests. The first invocation mistakenly used system Pandoc 3.1.11.1 and failed 15 publication tests. Rerunning the same source with required Pandoc 3.1.3 passed all 113. Publication, source, naming and the unchanged 349-requirement register also passed.

CI runs the complete twelve-test suite in `publication-integrity`, including both exhaustive enumerations. The unchanged corpus-map gate receives the same immutable retained-source fetch already accepted in PR106. No scientific validator, historical map or retained source pin is weakened.

## Additional non-author API review

A separate agent reviewed the API against the formulas and added [three bounded probes](review_probes.py); the [actual report](REVIEW_PROBES.json) binds the inspected module and oracle hashes. Relations with different carrier sizes `4 → 5 → 3` and a coherent dead end compose exactly. A `3 → 2 → 4` metric example gives exact constants `3/5`, `35` and composite `21`, attaining the product bound.

The third probe found a real implementation limitation: the 12-state carrier check happens after iterable materialization. A bounded sentinel shows that it is not an early input-consumption limit. This is retained as `BOUND_NOT_ENFORCED`, not hidden under an all-pass label. The supported profile requires already finite inputs and makes no streaming, memory or time bound claim. No blocking mathematical/API finding remains within that profile. The review is non-author relative to the implementation, but uses the same controller/model family/host.

## Review and release boundaries

The source integration parent is the reader-inventory merge `d6c3615cca2fe777f20d344f46266bbf89cdcdbd`. This package extends the existing canonical papers within edition 1.1; retaining series metadata is not approval of the new bytes. The content pull request is a review candidate, not a corpus decision or allowlist change. Prior receipts continue to describe their original files.

The author-side proof review and API/oracle checks establish the stated deductions and finite implementation observations. The new scientific revision still requires its version-specific review and publication process. Website deployment, index admission and production conformance are not measured by this package. A subsequent review or hosted result must identify the actual head rather than silently changing this record's scope.

The model contains successful relation edges. It does not observe refusal, unknown information, nontermination, probabilities, costs or authority unless such outcomes are explicitly supplied as additional state. Empty output is therefore not a generic unknown marker. The Hausdorff profile requires nonempty values. Hidden history or context must be represented at an intermediate interface before its composition law applies.

Completeness of an extracted relation, fidelity of semantic annotations, appropriateness of the selected observations, usefulness to an LLM agent and human meaning remain separate research obligations. The [priority map](../../roadmap/PRIORITIES_20261114.md) gives the next bounded Semantic Bridge and agent-lifecycle steps.

Rollback is a revert of the candidate content change. The earlier canonical paper bodies, finite reports and publication decisions remain recoverable from the integration parent and are not retroactively relabelled as tests of this extension.
