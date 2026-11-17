---
name: finite-fibre-oracle-regression
title: "Finite Fibre Oracle: Bounded Partial-Map Refusal"
language: en
status: research-draft
license: Apache-2.0
sources:
  - "Finite transfer partial-map method (c144)"
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

## Surfaces, rollback, limits

English Semantic Verification and RU/zh-Hans renditions, scientific registry, catalogue, review states, historical receipts, published site and source/roadmap pins **are not modified**. The only changed surfaces are this method, its executable test and the existing workflow. A separately reviewed revert of these files restores the original behavior. Same-controller producer testing is not independent DEUS review. Actual GitHub job log, PR-head versus merge-ref tree and later reuse must be evaluated separately. Cost NOT_MEASURED.
