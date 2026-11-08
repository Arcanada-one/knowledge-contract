# G11 bounded cross-package preparation — worker report

- **PR:** [knowledge-contract#81](https://github.com/Arcanada-one/knowledge-contract/pull/81) (DRAFT)
- **Head SHA:** `d6ccaf03d5bbd16382fd6eca91f6469a87e7ba8d`
- **Branch:** `Arcanada/g11-cross-package-preparation`
- **Clone:** `/home/dev/aup/claude-work/kcswe-g11/knowledge-contract`

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
