# G11 bounded cross-package preparation — worker report

- **PR:** [knowledge-contract#81](https://github.com/Arcanada-one/knowledge-contract/pull/81) (DRAFT)
- **Head SHA:** `87d22d1e026fa1b72b142208a21b90db1bb469e4`
- **Branch:** `Arcanada/g11-cross-package-preparation`
- **Clone:** `/home/dev/aup/claude-work/kcswe-g11/knowledge-contract`

## Round 9 (review must never become the evaluator result)

Base head before fix: `f6a7a0225a4a62674dd953aa2864feb3568ad5f0`.
Functional fix head: `dad7bd2340841f7f15699e576a260620111ae3c6`.

Finding: Agent-Brain PR81 comment `6725581829` (R-G11-RESULT-CONFUSION).
KC-SWE reproduced with `/tmp/kcswe_g11p10.py` (read-only): **BAD_TOTAL 7** on
the base head — an input review carrying `status` / `reason_code` / authority
flags was returned as the report (exit 0, true flags, review keys leaked).

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`/tmp/kcswe_g11p10.py` on `f6a7a022`) | 11 | 4 | 7 |
| Green-after (full `tools.test_cross_package_overlay`) | 116 | 116 | 0 |

Per-item red-before / green-after (RC1–RC4):

| Item | Red-before | Green-after |
| --- | --- | --- |
| RC1 A10 + output-shaped keys / flags | exit 0, true authority flags, review keys in report | `refused/malformed_input`; flags false; no review keys |
| RC1b A10 + status/reason only | exit 0 accepted review-as-report | `refused/malformed_input` |
| RC2 trusted R=`{A,B}`, only A discharged + injection | exit 0 (closure bypassed) | `refused/malformed_input` (strict reserved-key refusal) |
| RC2 control without injection | exit 3 `use_closure_incomplete` | unchanged |
| RC3 A5 no evidence + status/reason | exit 0 `contradicts_under_retained` | `refused/malformed_input` |
| RC4 A10 / A5 positives | pass | pass retained |
| A10 review `status=refused\|unresolved` `reason_code=x` | emitted as caller-chosen refusal/unresolved | `refused/malformed_input` (not `x`) |

### Structural fix

1. **Disjoint internal return.** `require_independent_review` returns
   `ReviewSelection(refusal=…)` or `ReviewSelection(review=…)`. Callers branch
   on those fields — never on `"status" in dict`.
2. **Trusted result boundary.** Every emitted report is built by `outcome()`
   (and `seal_report()` before CLI / `evaluate_document` emission) with
   `effects_authorized`, `execution_granted`, `proof_promoted`,
   `bounded_preparation`, and `released_schema` fixed by the evaluator. Input
   objects are never returned or merged into a report; review-shaped keys are
   stripped at seal.
3. **Reserved keys on review input.** Pin-matching reviews carrying any of
   `status`, `reason_code`, `also_reason_code`, `effects_authorized`,
   `execution_granted`, `proof_promoted`, `bounded_preparation`,
   `released_schema` → `malformed_input`. Documented in `tools/README.md`.

### Return-channel / kind-inference audit (`tools/cross_package_overlay.py`)

| Site | Pattern | Disposition |
| --- | --- | --- |
| `require_independent_review` success path | formerly `return matched` (input dict) | **Fixed** — `ReviewSelection(review=matched)`; never emitted |
| A10 / A5 callers | formerly `"status" in review_*` to detect refusal | **Fixed** — `review_selection.refusal is not None` |
| `outcome` / `refuse` | constructor for all evaluator reports | **Hardened** — authority flags always forced false |
| `seal_report` | final emission guard | **Added** — rebuild via `outcome`; drop review-shaped keys |
| `require_current_permissions` / `require_present_non_empty_string` / representation helpers | `dict \| None` where `None` means OK and dict is always `refuse(...)` | **Safe** — kind is Optional presence, not key inference; never returns input |
| `mandatory_closure_result` | returns `outcome`/`refuse` or `None` | **Safe** — evaluator-built only |
| `prefer_unresolved_mandatory` | reads `primary.get("status")` / `reason_code` | **Safe after fix** — `primary` is always an evaluator report, never a review |
| `load_input` | `(document, {})` vs `(None, refuse(...))` | **Safe** — discriminated by `document is None` |
| `report_exit_code` | `"status" not in report` | **Safe** — validates sealed evaluator reports only |
| `isinstance(..., dict)` elsewhere | structural validation of packages, pins, digests, lineage items | **Safe** — input shape checks, not return-channel tagging |
| Other `tools/*.py` checkers | own schemas; do not share review-selection return channel | **Out of scope / safe** for this finding |

### Probe

- `/tmp/kcswe_g11p10.py` left unmodified (read-only). After fix: **BAD_TOTAL 2**
  — the two `status=refused/unresolved` lines still expect `want=pos`; they now
  correctly refuse with `reason_code=malformed_input` (not caller `x`).
- Adapted copy `/tmp/kcswe_g11p10_probe.py`: those two cases expect
  `malformed_input` refusal. Change vs original: dropped `want="pos"` for the
  reserved-key refusal cases and added `expect_rc="malformed_input"` on RC1–RC3
  and the status-injection lines. **BAD_TOTAL 0**.
- `/tmp/kcswe_g11p9.py` unmodified: **BAD_TOTAL 0**.

### Sweep (`python3 -B /tmp/kcswe_g11r7_sweep.py`)

- mutations **1707**, exit0 **90**, crash **0**

### Local unit checks

`tools.test_cross_package_overlay` + retrieval-context + sources/DCO/CI/separation:
overlay **116** + related (same set as Round 8).

## Round 8 (typed identities before every equality)

Base head before fix: `6da3361d48f3bbb1d7b8de5fb3aaa9c8fb09df49`.
Functional fix head: `1eb745f081f06616bc29b009f5096d4d7a1f5d7f`.

Finding: Agent-Brain PR81 comment `6725034836`. KC-SWE reproduced with
`/tmp/kcswe_g11p8.py` (read-only; unmodified): both absent `relation_id`, both
absent revisions, and equal int `relation_id` each exited 0
`scoped_inspection_ok` on the base head.

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound8Tests` on `6da3361d`) | 15 | 7 | 8 |
| Green-after (full `tools.test_cross_package_overlay`) | 108 | 108 | 0 |

Per-item red-before / green-after:

| Item | Controls | Red-before | Green-after |
| --- | ---: | ---: | ---: |
| Both revisions absent | 1 | fail (exit 0 `scoped_inspection_ok`) | pass → `malformed_input` |
| Both relation ids absent | 1 | fail (exit 0) | pass → `malformed_input` |
| Equal non-string identities (int/list/dict/bool) | 4 | fail (exit 0) | pass → `malformed_input` |
| Review missing typed identities (A10 / A5) | 2 | already correct path | pass → `review_edge_mismatch` / `no_bound_edge_review` |
| Pins / units / conditions / scope paired controls | 4 | 1 fail (non-string units/scopes) | pass |
| A10 + A5 positive exact string identities | 2 | already pass | pass retained |

### Equality-audit table

Caller-supplied `==` / `!=` / membership comparisons in
`tools/cross_package_overlay.py` and how both sides are typed before equality.
Missing on both sides never counts as equal.

| Comparison | Guarantee / change |
| --- | --- |
| `overlay_revision` vs review `reviewed_edge_revision` | **Added** `require_present_non_empty_string` on overlay; review skipped unless non-empty string; then `==` |
| `relation.relation_id` vs review `relation_id` | **Added** same as revision pair |
| `pins_equal` (request / overlay / review pins) | **Changed** — both A/B values must be non-empty strings before `==` |
| `digests_equal` (package/endpoint/review manifests, representation digests) | **Changed** — requires `digest_complete` + `digest_malformed is None` on both sides before tuple `==` |
| Package `package_id` / `release_id` (A vs B; endpoint vs package) | Earlier loop requires non-empty strings via `require_non_empty_string` |
| `package_identity` / `endpoint_identity` tuples | Built only after package/endpoint string+digest validation |
| Representation id key lookup / digest bind | Rep keys and endpoint `representation_id` validated as non-empty strings; digests via `digests_equal` |
| Declared representation `language` vs `CANONICAL_LANGUAGE` / endpoint language | Declared language required non-empty string before `!= "en"`; endpoint optional |
| `representation_digest.source_revision` vs `release_id` | Both sides already non-empty strings before `!=` |
| Grounding anchors vs endpoint `source_anchor` | Anchors required non-empty strings (or A4 one-sided path); endpoints validated earlier |
| Reviewer vs relation / package / review author | Reviewer required non-empty string; authors compared only when `is_non_empty_string` |
| Review `scope` vs `assessment.scope` | **Changed** — review scope must be non-empty string; assessment scope, when present, must be non-empty string before `!=` |
| PREMISE_OVERLAP_FIELDS (A5 + R3 units/scope/conditions/time) | **Changed** — both sides must be non-empty strings before `!=`; missing/empty/non-string → unproven/missing, never equal |
| `task_requirements.members` / discharge `id` set ops | Members and ids refused unless non-empty strings before set membership |
| `verdict` / `kind` / derivative `support_kind` membership | Compared against closed constant frozensets after structural checks |
| Permission / `discharged` booleans | Real boolean type checks; not string-identity equality |

Paired both-absent controls added for changed comparisons: revisions, relation
ids, pin values, conditions (R3), plus equal non-string units/scopes.

### Probe

- `/tmp/kcswe_g11p8.py` left unmodified (read-only). After fix: all four cases
  exit 1 `refused/malformed_input`.
- `/tmp/kcswe_g11p7.py` left unmodified: `BAD_TOTAL 2` (same Round-7 fixture
  drift: A9 complete without trusted-R shape expectations in that probe, A3
  baseline). Adapted `/tmp/kcswe_g11p7_probe.py` still `BAD_TOTAL 0`.
- No probe file was copied or adapted in Round 8.

### Sweep (`python3 -B /tmp/kcswe_g11r7_sweep.py`)

- mutations **1707**, exit0 **90**, crash **0**

### Local unit checks

`tools.test_cross_package_overlay` + retrieval-context + sources/DCO/CI/separation:
**198** ran, **0** failed (108 overlay + 90 related).

## Round 7 (prior)

Base head before fix: `8f9e1be8067a021874f76c476edbc7b84c4aad9e`.

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound7Tests` on `8f9e1be8`) | 14 | 1 | 13 (11 FAIL + 2 ERROR from fixture helper before override fix) |
| Green-after (full `tools.test_cross_package_overlay`) | 93 | 93 | 0 |

## Round 6 (prior)

Base head before fix: `1cd98f186e593913e925fcd878d7b4854f5ae8d4`.

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound6Tests` on `1cd98f18`) | 12 | 1 | 11 |
| Green-after (full suite then) | 79 | 79 | 0 |

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

`gh pr checks 81` on tip `8eb5098b1476197594c60ef37dae8b6aaaec31fe` (run 42510265806): all listed checks **pass** (book-package, candidate-export, cases, corpus-map, dco, decision-separation, licensing, link-check, markdown-lint, publication-integrity, security-audit).
