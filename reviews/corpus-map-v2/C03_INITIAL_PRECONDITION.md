---
title: "C03: Initial-state premise and a bounded countermodel"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
sources: none
status: "candidate scientific audit; independent review pending"
---

# C03: Initial-state premise and a bounded countermodel

## Scope and exact source

This original finite-model audit concerns only claim C03 in the Knowledge Contract typed reading map, not the whole transformation paper or any agent implementation. In reference/foundations/corpus-map.json (Git blob a7b2fb8cde305b8fe4145df1ee7d7179478fdd60), C03 is a *producer summary*, explicitly not an independent assessment. Its source pin is commit 3d9b184b15fdee2e67bb0a2dc2aa5815b54364d5 at papers/constrained-transformations/PAPER.md (blob 57e7f2f9bb5de51d000b8c2ff8b3f90a01bb1b7e, §3, Proposition 2). The later repository main source at 161a01afb1b756adf059ea2e1cbdd0dca29d83a2 is blob c03df8bff7a04345e9ff09c2a0fea506be1ed13c, with the same conditional claim in §3. This audit reads those exact sources; it does not retroactively change either pin or a historical result.

The paper's sufficient condition includes P₁(x₀) before invoking partial correctness and stepwise observation preservation. It also requires compatible intermediate preconditions and observations for longer chains. The precise question here is whether that **initial-state** premise can be dropped while keeping the rest of the paper's stated obligations. It cannot.

## Countermodel to the weakened inference

Take the finite carrier X₀ = X₁ = O = {0,1} and one step (n=1). Define a relation T₁ = {(0,1),(1,1)}. Let P₁(x) mean x=1; let Q₁(y) be true for every y. Both protected observations are identity: p₁⁻(x)=x and p₁⁺(y)=y.

1. **Local Hoare partial correctness holds.** For each (x,y) in T₁, P₁(x) implies Q₁(y); the only admitted input is x=1.
2. **Local observation preservation holds for admitted transitions.** The sole admitted pair is (1,1) and its observations are equal.
3. **Junction obligations hold vacuously.** With n=1, there is no intermediate junction 1 ≤ i < n.
4. **The weakened conclusion is false.** The successful relation pair (0,1) starts with P₁(0)=false and has p₁⁻(0)=0 but p₁⁺(1)=1. Thus a successful chain and valid local conditional contracts alone do not entail endpoint equality.
5. **The stated proposition survives this test.** For the admitted successful pair (1,1), P₁(1)=true and endpoint equality holds. The countermodel violates a premise of the original theorem; it is **not a refutation** of that theorem.

The producer-owned executable finite control is [tools/test_c03_initial_precondition.py](../../tools/test_c03_initial_precondition.py). Its six tests enumerate the stipulated transition relation and distinguish admitted and non-admitted traces. These tests check precisely this small constructed model; they are not a proof for arbitrary sets or arbitrary chain length.

## Two-step controls: a non-vacuous junction boundary

The original one-step witness has no junction to test. A separate finite two-step
control now enumerates the successful chains of (T_1=\{(0,1),(1,1)\}) and
(T_2=\{(1,1)\}) on (\{0,1\}). With (P_1=P_2=(x=1)),
(Q_1=(y=1)) and identity observations, both junction implications are
checked on **both intermediate states**, including the state where (Q_1) is
true. The two successful paths are (0\to1\to1) (not initially admitted;
endpoint observation changes) and (1\to1\to1) (initially admitted; endpoint
observation is retained). Thus the initial-premise omission also fails with an
actual, non-empty junction, rather than only in the vacuous (n=1) case.

Two adverse finite controls separately omit each junction implication while
keeping the other: complementing both protected observations on step 2 leaves
local observation preservation intact but breaks inter-step observation
compatibility; alternatively a step-2 precondition true only at 0 and an
output observation constantly 0 preserve step-2 local guarantees on admitted
pairs, while the reachable intermediate state 1 fails (Q_1\Rightarrow P_2).
Both produce an admitted-initial-state path that loses its final observation.
These are executable checks of the *existing* two-junction distinctions in
the manuscript, not new theorems, not a proof for all chains and not approved
evidence edges.

The test module now has ten finite checks (six one-step plus four two-step).
The C03 workflow invokes the whole module, but the added four cases require
a new exact-head hosted execution readback and separate non-author review
before any broader acceptance claim.

## Interpretation and non-implications

This shows that P₁(x₀) cannot be **omitted from these sufficient assumptions** without invalidating the general implication. It does not establish that the premise is logically necessary for *every particular* successful path: some inadmissible paths may happen to preserve the observation. Nor does it establish termination, existence of an output for every admitted input, semantic fidelity of the observation functions, permission to execute, or production conformance. The original source's induction proof, not this finite control, addresses the positive result for arbitrary finite chains under all its premises.

For the proposed knowledge-corpus-map/2 inventory, this audit is a **candidate internal-source assessment**, not an approved claim-has-ground or ground-uses-source edge. Reading a source and checking a countermodel do not supply independent acceptance, an external corroborating experiment, or a publication decision. The current candidate inventory has 34 source identifier records but zero approved evidence assessments and zero evidence edges; those zeros must not be increased by this note alone.

## Acceptance boundary

An independent reviewer (Agent-Brain or another designated non-author reviewer) should compare both pinned source versions, recalculate the six finite checks in a fresh environment, verify the universal initial-state premise of the paper's proposition and identify any premise-satisfying counterexample if one exists. Report *review* separately from source identity, local finite model, CI, merge, site rendering and index admission. No edit to the publication catalogue, v1/v2 graph, evidence register or Muneral task state is made by this candidate audit.
