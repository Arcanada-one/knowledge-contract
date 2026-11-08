# G11 bounded cross-package preparation — worker report

- **PR:** [knowledge-contract#81](https://github.com/Arcanada-one/knowledge-contract/pull/81) (DRAFT)
- **Head SHA:** `b3541911f4cab1249c7205394f57b9f2967fe95b`
- **Branch:** `Arcanada/g11-cross-package-preparation`
- **Clone:** `/home/dev/aup/claude-work/kcswe-g11/knowledge-contract`

## Round 7 (KC-Brain / Agent-Brain A5 + A9 semantic decisions)

Base head before fix: `8f9e1be8067a021874f76c476edbc7b84c4aad9e`.

Decisions read in full: KC-Brain comment `6724519834`; Agent-Brain comment `6724344740`.
R1 package-declared representations rule kept (literal `canonical-en` is not a rule).

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound7Tests` on `8f9e1be8`) | 14 | 1 | 13 (11 FAIL + 2 ERROR from fixture helper before override fix) |
| Green-after (full `tools.test_cross_package_overlay`) | 93 | 93 | 0 |

Per-item red-before / green-after:

| Item | Controls | Red-before | Green-after |
| --- | ---: | ---: | ---: |
| A5 metadata ≠ proof / evidence required | 2 | fail (retained without `evidence`; helper ERROR on overrides) | pass → `no_bound_incompatibility_assessment` / retained with evidence |
| A5 unequal time → unresolved | 1 | fail (`conditions_incompatible` refuse) | pass → `premise_alignment_unsupported`, both retained |
| A5 empty/missing `common_assumption` | 2 | fail (refuse / wrong code) | pass → `common_assumption_missing` |
| A5 positive `x<=10` vs `x>10` | 1 | already exit 0 on old head without evidence | pass with bound `evidence`, no winner, `effects_authorized: false` |
| A9 bind to trusted R | 6 | fail (discharges alone completed; empty set ignored) | pass precise unresolved / empty justified complete |
| A3/A5 early return keeps unresolved mandatory | 2 | fail (missing `unresolved_mandatory` / A5 retained) | pass `use_closure_incomplete` + `unresolved_mandatory` |

### Field names (KC-SWE mapping; pending Brain confirmation)

| Concept | Wire field | Source |
| --- | --- | --- |
| Common applicability domain | `relation.assertions.common_assumption` or `relation.grounding.common_assumption` (non-empty string; **not** `conditions`) | Overlay §§3–6 “common assumption”; coordinator Round-7 ask |
| Incompatibility explanation | R2-bound review `evidence` (non-empty string) | Overlay §3 “assessment evidence”; coordinator ask |
| Trusted requirements set | `context.task_requirements = {revision, members[, empty_set_justification]}` | Overlay §5 `R`; coordinator ask |
| Discharge witness reference | `mandatory_dependencies[].witness_ref` (recorded reference, not admission proof) | Coordinator ask; admission NOT_MEASURED |
| Absent vs empty requirements | absent key vs `members:[]` + non-empty `empty_set_justification` | Agent-Brain; coordinator ask |

### Probe

- Original `/tmp/kcswe_g11p6.py` left unmodified (read-only); A5 fixtures predate Round 7 → `BAD_TOTAL 3` against new evaluator.
- Adapted copy `/tmp/kcswe_g11p7_probe.py`: A5 uses `a5_conflict_assertions()` + `bound_review(evidence=...)`; adds no-evidence and unequal-time controls.
- Adapted result: **`BAD_TOTAL 0`**.

### Sweep (`python3 -B /tmp/kcswe_g11r7_sweep.py`, Round-6 fixture)

- mutations **1707**, exit0 **90**, crash **0**

### Local unit checks

`tools.test_cross_package_overlay` + retrieval-context + sources/DCO/CI/separation: **183** ran, **0** failed.

## Round 6 (prior)

Base head before fix: `1cd98f186e593913e925fcd878d7b4854f5ae8d4`.

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound6Tests` on `1cd98f18`) | 12 | 1 | 11 |
| Green-after (full suite then) | 79 | 79 | 0 |

Genuine positives retained: A10 `scoped_inspection_ok`, A5 `contradicts_under_retained` (now with `common_assumption` + review `evidence`).

## Round 5 (prior)

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound5Tests` on `1e5db531`) | 15 (18 subtests) | 0 | 18 |
| Green-after (full suite then) | 67 | 67 | 0 |

## NOT_MEASURED

- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- overlays beyond exactly two canonical English packages
- released `cross-package-relations` wire schema registration
- admission behind `witness_ref` (reference recorded only)
- KC-Brain / Agent-Brain confirmation of Round-7 wire field names

## Hosted CI

Filled after `gh pr checks 81` on the Round-7 tip.
