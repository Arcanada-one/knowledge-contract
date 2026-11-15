---
title: "F05 candidate: partial assessment transfer on determined fibres"
owner_role: KC-Brain
prepared: 2026-11-15
status: reconstructed candidate; finite controls; not admitted
baseline_workspace_head: efc5765d1b057b3c4328e3ff0aaf95f1eeaed8f4
runtime_activation: not_verified
---

# F05 candidate: partial assessment transfer on determined fibres

## 1. Provenance and the bounded increment

This note is a **transparent reconstruction** of the reported hourly F05
candidate. The reported directory `/mnt/data/kc_f05_readonly_candidate` is
absent in this runtime (`/mnt/data` itself is absent); the reported note and
script were not found under the current workspace. Their original bytes,
hashes, execution and review have not been recovered. Agreement with the
reported counts below does not authenticate those unavailable artifacts.

The checked starting point is the existing
[Verification transfer topic](https://github.com/Arcanada-one/arcanada-workspace/blob/efc5765d1b057b3c4328e3ff0aaf95f1eeaed8f4/documentation/plans/knowledge-collective-live-lab/roles/KC-Brain/topics/meaning-graph/VERDICT_TRANSFER.md),
blob `f202a82726632ebd6f91567502695d5832dbcb6d`, and its
[finite checker](https://github.com/Arcanada-one/arcanada-workspace/blob/efc5765d1b057b3c4328e3ff0aaf95f1eeaed8f4/documentation/plans/knowledge-collective-live-lab/roles/KC-Brain/topics/meaning-graph/check_verdict_transfer.py),
blob `f04270337910b3c07b21722c132f8e97c5afbb7e`. Both blobs were read at the
actual PR1928 head `efc5765d1b057b3c4328e3ff0aaf95f1eeaed8f4`; the older head
in the PR body was not treated as current source.

The mathematical source is Pavel Valentov, *Meaning Geometry:
Representation Spaces, Distinguishability, and the Limits of Similarity*,
publication edition 1.1, research draft, Proposition 2; read on 2026-11-15 at
[Knowledge Contract commit a5b3618](https://github.com/Arcanada-one/knowledge-contract/blob/a5b3618034256f14f389c2c7de8da409c7c5310c/papers/geometry-of-semantic-representations/PAPER.md),
blob `ae74a2b7dfb768a2447622680635540c4a658387`. No separate publication date
is asserted from the supplied front matter. The source already states the
factorization criterion and explicitly excludes verification of observation
values. The result below is its elementary **partial-domain corollary**,
not a new theorem or a priority claim.

The prior diagnostic tests a global transfer rule. Its failure does not imply
that every attained observation is ambiguous. The useful increment is to
identify the largest observation domain on which a fixed assessment is
determined in the declared model, while retaining concrete refusal witnesses
elsewhere. This supplies a bounded candidate diagnostic for the existing F05
work package, not a new specification, work queue or admission mechanism.

## 2. Exact partial-domain statement

Fix a nonempty situation carrier S, a total observation map p: S -> A with
A = p(S), and one fixed total assessment map v: S -> D. Subject, criterion,
scope and relevant time are fixed as in the existing topic. For the finite
checks D = {pass, fail, unknown, not_applicable}.

For each a in A define its full fibre and assessment image:

\[
F_a=\{s\in S:p(s)=a\},\qquad
V_a=\{v(s):s\in F_a\},\qquad
U=\{a\in A:|V_a|=1\}.
\]

Every F_a is nonempty. The phrase **singleton-valued fibre** means that V_a
has one element; F_a can contain many situations.

A partial map h: B -> D, for B contained in A, is sound for this fixed model
when h(p(s)) = v(s) for every s with p(s) in B.

**Corollary.** There is a unique greatest sound partial map, ordered by
extension: its domain is U and its value at a is the sole member of V_a.
Every sound partial map is a restriction of it. A global factorization
exists exactly when U = A.

**Proof.** If a lies in the domain B of a sound partial map, every member of
F_a must receive the same value h(a), so V_a is a singleton and a lies in U.
Conversely, assigning the sole member of V_a at each a in U agrees with v
on all corresponding situations. Any sound partial map therefore has a
domain contained in U and agrees with that assignment. This proves existence,
uniqueness and greatestness. Taking B = A gives the already established global
criterion. No choice of one favourable representative is used. QED.

This is model-relative exact determination. It does not provide an efficient
procedure for an infinite S or show that the actual assessment values are
available. The finite script receives them as explicitly stipulated inputs.

## 3. Diagnostic results and refusal boundary

The executable returns a diagnostic outcome separately from an assessment:

| Condition for the queried observation | Diagnostic outcome | Assessment field |
| --- | --- | --- |
| Attained and singleton-valued in the supplied complete model | `determined_in_model` | The unchanged member of D |
| Attained but two situations require different assessments | `refused_ambiguous` | Absent; retain the conflicting index pair |
| Not attained in the supplied carrier | `refused_unattained` | Absent |
| Empty carrier, misaligned arrays, or unsupported input shape/label | Raise `ValueError` before evaluation | No diagnostic receipt for that call |

These diagnostic strings are local test vocabulary, not additional canonical
check-result values or a wire schema. An ambiguous fibre does not prove that
an actual target failed. An unattained observation is outside this model; its
value cannot be inferred by extending the partial map arbitrarily.

An all-unknown fibre determines the model's assessment `unknown`; it does not
establish the missing property. An all-not_applicable fibre preserves the
supplied `not_applicable` value, but this calculation does not establish the
inapplicability rule or its grounds. A mixed unknown/not_applicable fibre is
ambiguous. Neither label is converted to pass, and a refused transfer never
manufactures a canonical unknown or not_applicable assessment.

The interface deliberately accepts explicit nonempty tuples of equal length,
nonnegative integer observation labels (booleans excluded), an integer query,
and the four exact string assessment labels. It does not parse evidence
receipts, coerce strings or infer omitted states. The exhaustive experiment
uses only observation labels 0 and 1; auxiliary controls use the same labels.

## 4. Finite check and independent count derivation

Before execution the acceptance target is fixed: enumerate all 2^4 observation
maps paired with all 4^4 assessment maps on four labelled situations. For each
profile, query both observation labels, including an unattained label when
the observation map is constant. Compare the diagnostic with an independently
structured oracle that enumerates all 5^2 partial maps, where the fifth symbol
means undefined, rejects assignments to unattained observations, and checks
statewise agreement. The oracle must have one greatest sound partial map.
It does not call the diagnostic or use its fibre grouping or witnesses.

The following combinatorial derivation is independent of the loop:

| Observation fibre sizes | Number of observation maps | Global profiles | Partial but not global profiles | No singleton-valued fibre |
| --- | ---: | ---: | ---: | ---: |
| 4, with the other label unattained | 2 | 8 | 0 | 504 |
| 1 + 3 | 8 | 128 | 1,920 | 0 |
| 2 + 2 | 6 | 96 | 576 | 864 |
| Total | 16 | **232** | **2,496** | **1,368** |

For a constant map, only the four constant assessment assignments are
determined. For 1+3, the one-situation fibre is always determined; 16 of the
256 assignments are global and 240 are partial. For 2+2, a pair is constant
in 4 of its 16 assignments: 16 assignments are global, 2*4*12 = 96 are
partial, and 12^2 = 144 have no determined fibre. Thus all three categories
sum to 4,096. In particular, the many one-situation fibres explain part of
the finite partial count; the count is not evidence of practical usefulness.

The observation queries have a different denominator: 8,192 total, split
2,952 determined, 4,728 ambiguous, and 512 unattained. The oracle examines
102,400 partial-map candidates. Those are calculations inside the same 4,096
profiles, not additional independent experiments.

The separate controls preserve all four labels; reject pass/fail,
pass/unknown and unknown/not_applicable ambiguity; exercise a partial profile
despite global failure; and reject thirteen unsupported input shapes. A
relevant refinement separates pass from fail in a constructed model, whereas
an irrelevant refinement still groups a pass state with a fail state. These
controls test exactly which retained distinction changes the result; they
do not establish an observation's practical cost, provenance or causal role.

The adverse control replaces the diagnostic in memory with “take the first
assessment on the fibre”, runs the **unchanged** acceptance checks, and must
retain the original assertion failure. Since the suite uses assertions, an
optimized Python subprocess must exit 2 with the fixed refusal message
before emitting a finite-run receipt. A mismatch or escaped mutant fails the
script; the expected result is never substituted for observed output.

Run the self-contained check with:

```bash
python3 -B check_fibrewise_transfer.py > fibrewise-transfer-result.json
```

The retained [execution receipt](fibrewise-transfer-result.json) binds its
command, time, Python version, platform and script SHA-256. The source and
counting logic are separate in structure but share a controller, status
alphabet and supplied model. This is not a protected oracle or independent
scientific acceptance. The receipt's `runtime_authorized=false` records the
absence of native KC2 runtime proof; local authorized preparation is not
reported as a knowledge-admitted production run.

## 5. Limits that remain after a finite pass

The declaration of S must cover every situation claimed by the transfer.
Adding a state can destroy determination: one state with observation 0 and
assessment pass has a singleton-valued fibre; adding another state with the
same observation and assessment fail makes it ambiguous. The script retains
this countermodel. Arbitrary extensions, domain shift and live coverage are
therefore outside the result.

To apply a partial transfer to a real target, separate evidence must bind
that target to the stated carrier and to its actual retained observation,
justify the assessment function and its criterion, and establish that the
whole relevant fibre has been covered. A finite sample cannot replace these
premises merely because its observed labels agree. The current script does
not establish those premises.

Source identity, observer authenticity, actual consumption, task scope and
current authorization remain independent obligations. A singleton-valued
assessment image in this toy model establishes none of them. Numerical
fractions of all functions on four states are combinatorial counts, not
empirical frequencies, calibrated confidence or production success rates.

## 6. Integration and review disposition

| Surface | Disposition for this candidate |
| --- | --- |
| Existing meaning-graph topic | Add a scoped pointer to this corollary; preserve the original global criterion and historical receipt |
| Candidate note, checker and execution receipt | Keep together under the existing meaning-graph topic; bind exact file hashes in the integration record |
| Existing F05 CI step | Add a separate invocation of this checker; keep its 4,096 profile denominator distinct from the prior global check |
| F05 canonical specification/paper | No adoption performed; this remains supporting preparation for the existing owner/work package |
| RU and zh-Hans | No translation or language acceptance claimed for this new note |
| Generated site, index and runtime selection | No operation performed; serving, admission and runtime use remain NOT_VERIFIED |
| Own-role or other-role canon | No change required for this bounded topic increment |
| Task queue and PR identity | Reuse existing work; this note creates no task, PR or status transition |

The actual local run must match the fixed inventory above, kill the first-value
mutant and demonstrate optimization refusal. An exact-source non-author
review is still required before scientific admission. Same-controller review,
CI, source merge and later consumer reuse remain distinct measurements.
Rollback is an ordinary reviewed removal of the new candidate files and
their pointer/CI invocation; historical evidence stays unchanged.
