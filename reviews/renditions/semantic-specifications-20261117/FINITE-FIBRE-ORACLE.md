---
name: finite-fibre-oracle-regression
title: "Finite Fibre Oracle: Bounded Partial-Map Refusal"
language: en
status: research-draft
license: Apache-2.0
sources:
  - "Finite transfer partial-map method (c144)"
  - "Swapped-fibre reconstruction and execution (17 November 2026)"
---

# Finite Fibre Oracle: Bounded Partial-Map Refusal

**Status: author-side method candidate, NOT independent scientific acceptance or native KC2 admission.** This is a source-bound regression for the stipulated finite model in Semantic Verification §7.4, not an empirical evaluation of an agent.

## Pre-change baseline, hypothesis and scope

At PR124 head `992ab3a89109c607e9659798510f96180059fc8f`, the local c143 candidate demonstrated that earlier c140 verification used `assert` for expected counts; a wrong `determined=2953` was refused in ordinary Python but accepted with `-O`. This was a defect of that local test harness, not a refutation of the English specification or a deployed consumer. The original c140/c143 bytes and adverse results remain unchanged.

**Hypothesis:** explicitly raised errors and separately checked normal/optimized paths can reproduce 4,096 profiles, 8,192 fibre queries and 102,400 candidate partial maps, reject four defective algorithms and refuse tampering in both modes.

**Role:** KC-Brain scientific-method author-side auditor. **Skill:** finite enumeration/adversarial checks candidate. **Blueprint:** source pin → enumerate all 25 partial maps/profile → positive reference → four mutants → tamper normal/-O → exact-head CI → independent reviewer. **Constraints:** no new normative requirement, no review-state promotion, no publication or native authority. **Success criteria:** fixed counts and nonzero explicit refusal in both modes.

## Positive, negative and provenance

In the stipulated model `2^4 × 4^4 = 4096` profiles; each has two queried observation labels and `(4+1)^2 = 25` partial-map candidates. Accepted partial maps total 7,272. The query outcomes are determined 2,952; ambiguous 4,728; unattained 512. Four tested defects: accept-all (95,128 false accepts), refuse-all (7,272 false refusals), allow unattained (2,080 false accepts), omit last situation (3,672 false accepts). These synthetic counts do not measure production correctness.

[check_finite_partial_map.py](check_finite_partial_map.py) is a **derivative** of the retained local c143 candidate, originally SHA-256 `3f756a1db019c7ec495c5668858630ce369be0d8993674e1e2db33c88313b8ea`; the new interface adds deliberate expected-count tampering with explicit exit 3. It is not represented as the original artifact. The existing rendition workflow runs the new source both normally and with `-O`, checks outputs and four mutant counts, then demands exit 3 and the exact mismatch message after injecting 2953.

## Independent aggregate count — c145 successor

A bounded cross-check now derives the allowed-map population without calling the candidate membership predicate. With `q=4` values and a fibre containing `k` situations, sum over all `q^k` valuation assignments: every assignment admits the undefined partial map, while the `q` constant assignments admit one additional defined value. Hence the summed weight is `F(0)=1` for an unattained fibre and `F(k)=q^k+q` for `k>0`.

For two observation labels and four situations, distribute positions between the two fibres with binomial multiplicity. The symbolic population is `Σ_{k=0}^4 binom(4,k)F(k)F(4−k) = 260+2176+2400+2176+260 = 7272`. The implemented checker computes this expression separately from enumerated valid candidates and requires both populations to agree with the declared expected total. The `--expect-accepted 7273` counterexample must exit 3 with `FINITE_FIBRE_REFUSED: closed-form accepted partial-map cardinality mismatch` under both regular and optimized Python. Preserve the earlier wrong-query 2953 control and four original algorithm mutations; this is additional falsification, not a replacement.

This checks only the explicitly stipulated `4×2×4` finite model; the closed form assumes independent valuation choices across disjoint fibres and makes no claim about uncertain, correlated or real agent observations. Its arithmetic is an author-side derivation, not a separate scientific reviewer or native KC2 admission. Exact source and rollback boundaries above remain unchanged. Current downstream site release and live index are separate.

## Cardinality-preserving wrong-value adversary — c146

The c145 closed-form check verifies **how many** partial maps are admissible, not which assessment value a defined map returns. A cyclic permutation of all four model values in every attained fibre (`x -> (x+1) mod 4`) is a concrete adversary: it preserves the count of accepted candidates per profile and the total **7,272**, yet changes exact membership. On the stipulated 4,096 profiles × 25 candidates, the wrong-value predicate accepts 7,272 and differs from the correct predicate in **3,176 false acceptances and 3,176 false rejections**.

Minimal refuter: with observations `(0,0,0,0)` and assessments `(0,0,0,0)`, the partial map `(0,undefined)` is correct but the cyclic-shift mutant rejects it; `(1,undefined)` is incorrect but the mutant accepts it. The prior aggregate formula, candidate count and profile classification cannot distinguish these two oracles. The existing exact-value `correct_valid` comparison can, provided the mutant is actually executed.

The existing finite checker now includes `cyclic_value_shift` as an actual decision mutant and records `accepted_count` for each mutant. The rendition workflow requires its accepted count **7,272**, false accepts **3,176** and false rejects **3,176**, in addition to all prior positive counts and negative 2953/7273 controls. Run the same JSON under ordinary and optimized Python and compare bytes. The separately written local control was executed in both modes (Python SHA-256 `b3ce2809b7f2e5c3d347df3def579cee94578517bda5f606e9f442f3633a6bab`; result SHA-256 `d39683603227345f2a92cdcf10f34f017cdd1b288bb4cc6ce7019f25fc53a583`), but remains a same-controller methodological check, not an independent role review.

**Method lesson:** a matching inventory cardinality does not establish correctness of value assignments. Include a cardinality-preserving adversary, positive exact-value witnesses and two-sided decision divergence. This bounded lesson does not establish source/target semantic translation equivalence, actual permissions, deployed use or native KC2 admission. Revert only the new method/checker/workflow increment if required; never rewrite retained receipts.

## Symmetry-preserving wrong-fibre adversary — new c148 reconstruction

Cardinality is not the only necessary-but-insufficient control. A deliberately
wrong predicate can also commute with every renaming of assessment values and
with exchange of the two observation labels. This successor reconstructs the
counterexample described in the [c148 record](https://github.com/Arcanada-one/knowledge-contract/pull/124#issuecomment-6953592470).
The original c148 local script and output were unavailable in this session.
The changed checker and the [new execution record](swapped-fibre-reconstruction/EXECUTION.json)
are new artifacts; they do not authenticate or replay those unavailable bytes.

When both observation fibres are attained, each has a constant assessment, and
their assessments differ, the adversary checks each defined partial-map output
against the *other* fibre's value. On every other profile it uses the original
predicate. Undefined outputs remain allowed. The minimal retained witness is
observations `(0,0,0,1)` and assessments `(0,0,0,1)`: the correct predicate accepts
`(0,1)` and rejects `(1,0)`, while the swapped-fibre predicate does the reverse.

There are `2^4 - 2 = 14` observation assignments with both labels attained, and
`4 × 3 = 12` ways to choose two different constant assessment values. Thus
`14 × 12 = 168` profiles are affected. Each predicate accepts four partial maps
on each affected profile, but the only shared map is `(undefined,undefined)`.
The resulting disagreements are therefore `168 × 3 = 504` false acceptances
and the same number of false rejections. On the other 3,928 profiles the
predicates agree. Their accepted-map cardinalities agree on all 4,096 profiles
and sum to 7,272 for each predicate. This derivation is separate from candidate
enumeration; it assumes exactly the stipulated finite model.

The executable control builds truth tables by actually evaluating both
predicates for all 102,400 candidates. It then checks 2,457,600
profile/candidate/value-permutation comparisons (all 24 value permutations)
and 102,400 observation-label-exchange comparisons against those evaluated
tables. Each comparison checks both predicates; these are not additional
independent samples or agent runs. The undefined sentinel stays fixed under
value renaming, and exchanging observation labels also exchanges the two
candidate output positions. This checks the two generating symmetry actions
separately. It does not claim to enumerate all 48 combined actions.

All existing five mutants and the 2953/7273 adverse expectations remain in
place. `--expect-swapped-false-accept 505` must explicitly refuse with exit 3 in
both ordinary and optimized Python; correct runs must produce identical JSON.
The current result is retained in [result.json](swapped-fibre-reconstruction/result.json).
The existing rendition workflow executes these cases and reads their concrete
outputs; a workflow success without this step would not satisfy this contract.

**Method lesson:** counts and symmetry checks can expose some defects, but do
not determine the correct assessment attached to each observation. Preserve
positive exact-value witnesses, their adverse counterparts and pointwise
comparison to the source rule. The correct oracle is not refuted by this
constructed wrong algorithm. This is a bounded regression example, not a new
general theorem, evidence of a real consumer failure, a fidelity verdict for
the translated specifications, independent DEUS acceptance or native admission.

## Surfaces, rollback, limits

English Semantic Verification and RU/zh-Hans renditions, scientific registry, catalogue, review states, historical receipts, published site and source/roadmap pins **are not modified**. The changed surfaces are this method, its executable test, the existing workflow, new reconstruction receipts and their SOURCES registration. A separately reviewed follow-up revert restores the prior checker behavior while preserving historical evidence. Same-controller producer testing is not independent DEUS review. Actual GitHub job log, PR-head versus merge-ref tree and later reuse must be evaluated separately. Cost NOT_MEASURED.

## Pointwise constructive source tether — c149 candidate

The independent count and equivariance checks above can both pass for the
`swapped_constant_fibres` adversary. For a stronger check grounded in
[Semantic Verification §7.4](../../../engineering/specifications/semantic-verification/SPECIFICATION.md),
construct the set of permissible outputs **before** calling the candidate
membership predicate. For each observation label, if its fibre is attained
and has exactly one distinct assessment value `v`, its allowed outputs are
`{undefined, v}`; otherwise only `{undefined}` is allowed. Take the
Cartesian product of those sets. This specifies the exact decisions for all
25 candidates, not only the number accepted. Unattained fibres remain
undefined and ambiguous fibres cannot silently receive a value.

The existing checker now requires, on all 4,096 profiles and 102,400
profile/candidate pairs, that the direct source predicate and this independently
constructed permitted-map set agree pointwise. The constructed set also
contains the previously derived maximal map. No historical result.json or
EXECUTION.json is altered: the default correct-path JSON remains byte-identical.
The workflow additionally executes `--source-under-test swapped_constant_fibres`
and `--source-under-test cyclic_value_shift` in ordinary and optimized Python.
Each *must* exit 3 with `constructive exact-map mismatch`; these are real
executable guard-falsification controls, not an unsupported claim that the
mutants are deployed. The earlier 2953/7273/505 refusals remain.

**Pre-change scope:** PR124 `78bbbd40faeb62e9800e6fe13f5641f8e4a9ac2d`;
the accepted-cardinality, equivariance and two-sided divergence evidence
was real but lacked a separate, constructive exact-membership comparator.
**Goal:** catch any future change to the direct source predicate that violates
the stipulated §7.4 rule while preserving its superficial counts. **Adverse
controls:** both value-shift and fibre-swap must be rejected using the same
comparison that admits the correct predicate. **Affected consumers:** this
checker and its existing hosted rendition step only. Scientific source, all
EN/RU/zh-Hans bodies, catalogue, review states, published site, stored receipts,
parent PR104 and native agent permissions do not change. **Rollback:** revert
this three-file method/checker/workflow increment on the existing PR branch;
retained earlier evidence stays unchanged.

This is a second formulation by the same author/controller, not an
independent reviewer, authenticated real observation or deployed consumer
oracle. It cannot establish soundness of arbitrary source evidence, reviewer
independence, real agent behavior or native KC2 admission. Seek a non-author
source-rule review on the exact final head before merging; cost NOT_MEASURED.

## Defined-output grade histogram — c150 author-side candidate

The existing finite check confirms the total of 7,272 admissible partial maps, but
an aggregate is insufficient to distinguish a change in how many observation
outputs are defined. For an explicit additional necessary invariant, define
(N_r) as the number of accepted (observation profile, assessment profile,
partial-map) triples having exactly (r) defined outputs, with (n=4)
situations, (m=2) observation labels and (q=4) assessment values.

Choose which (r) labels are defined and their (q^r) values. Each situation
can select one of those (r) labels with its prescribed assessment, or any
of the remaining (m-r) labels with any of (q) assessments. Inclusion-exclusion
ensures every defined label is attained:

[
N_r = \binom{m}{r} q^r \sum_{j=0}^{r} (-1)^j \binom{r}{j}
      \big((m-r)q+r-j\big)^n.
]

At ((n,m,q)=(4,2,4)), the independently derived histogram is
**(N_0=4096,;N_1=2952,;N_2=224)**. Their sum is 7,272. This
is a count over profile/map pairs, not a claim about distinct mathematical
functions or agent evaluations. It is compatible with the 232 globally
determinate profiles: eight of those have one unattained label, while 224 have
both labels attained and constant.

The checker computes this finite formula without calling its candidate
membership predicate and separately counts the actually accepted outputs by
grade. It demands equality and preserves the default JSON bytes, so earlier
recorded executions are not silently refreshed. The existing Rendition step
continues its full correct-path normal/optimized execution and retained-output
comparison. An additional hosted negative case
`--expect-two-defined 225` must refuse with exit 3 and
`FINITE_FIBRE_REFUSED: two-defined partial-map grade mismatch`
in both modes.

**Local adverse demonstration:** a deliberately incorrect predicate can
replace the accepted two-defined map `(0,1)` with the rejected one-defined
map `(2,undefined)` only in profile observations `(0,0,0,1)`,
assessments `(0,0,0,1)`. The total 7,272 is unchanged, while the
histogram becomes `4096/2953/223`. This is a separate local probe,
not a newly deployed mutant or a claim that the site has this defect.
Conversely, the existing swapped-fibre mutant preserves even the per-profile
grades, so **this histogram is also insufficient alone**. Exact source-value
membership remains mandatory.

**Scope and rollback:** this is a method/checker/workflow regression bound to
Semantic Verification §7.4, not a new normative clause. EN/RU/zh-Hans manuscript
bodies, catalogue, sidecars, review states, previous evidence receipts and
production source/roadmap pins are unchanged. Revert this exact three-file
increment on the existing PR if its checks fail, keeping historic evidence.
Both computations share the stipulated model and author/controller;
independent semantic review and native KC2 admission are NOT_VERIFIED.
Cost NOT_MEASURED.
