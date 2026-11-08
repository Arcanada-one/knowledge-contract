# G11 bounded cross-package preparation — worker report

- **PR:** [knowledge-contract#81](https://github.com/Arcanada-one/knowledge-contract/pull/81) (DRAFT)
- **Head SHA:** *(filled after Round 6 commit)*
- **Branch:** `Arcanada/g11-cross-package-preparation`
- **Clone:** `/home/dev/aup/claude-work/kcswe-g11/knowledge-contract`

## Round 6 (KC-SWE review of Round 5 — R3 / R1 / R2)

Base head before fix: `1cd98f186e593913e925fcd878d7b4854f5ae8d4`.

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (`FailClosedRound6Tests` on `1cd98f18`) | 12 | 1 | 11 |
| Green-after (full `tools.test_cross_package_overlay`) | 79 | 79 | 0 |

Per-finding red-before / green-after:

| Finding | Controls | Red-before | Green-after |
| --- | ---: | ---: | ---: |
| R3 full `PREMISE_OVERLAP_FIELDS` | 4 | 4 fail (missing time/conditions still exit 0 with `unit_scope_aligned=True`) | 4 pass → exit 3 `unit_scope_unresolved` |
| R1 package `representations` map | 5 | 4 fail + 1 already failing differently | 5 pass (`representation_identity_mismatch` / `rendition_endpoint_refused` / `malformed_input`) |
| R2 edge-bound review selection | 3 | 2 fail (other-first refused; disagreeing verdicts accepted first) / 1 pass (own-first) | 3 pass (both orders OK; conflict → `review_verdict_conflict`) |

Genuine positives retained: A10 `scoped_inspection_ok`, A5 `contradicts_under_retained`.

### R1 interpretation (coordinator option c; pending KC-Brain)

Overlay §2 does not name a literal canonical representation id. KC-SWE enforces package-declared binding: required `representations` map; endpoint id/digest must match; declared language must be `en`; optional `endpoint.language` must equal declared. Fixture id `canonical-en` is not a rule.

### Probe (`python3 -B /tmp/g11p5.py`)

- `BAD_TOTAL 0`
- A10 / A5 positives exit 0; R1 undeclared `ru-draft` refused; R2 both review orders exit 0; R3 missing time/conditions with `aligned=True` → exit 3

### Sweep (`python3 -B /tmp/g11r2/kcswe_sweep.py`, Round-6 adapted fixture)

- mutations **1707**, exit0 **90**, crash **0**
- Exit-0 mutation justifications:
  - `packages.*.path` deleted or non-empty string tokens — optional path; present value must be a string
  - `relation.from/to.object_id|component_id` string tokens — required non-empty strings, open vocabulary
  - `relation.from/to.language` absent/empty — optional; when present must equal declared representation language
  - `reviews[0].reviewer` alternate non-empty strings ≠ author — R2 requires non-empty string reviewer
  - `reviews[0].author` / `overlay.author` alternate or absent values ≠ reviewer — self-authorship refused only when equal
  - `overlay.assessment` deleted/non-object or `assessment.scope` empty/absent — review still carries compatible scope
- Note vs Round 5: `representation_id` / `representation_digest.byte_domain` open-token exit-0 classes are gone (must equal package-declared representation binding).

### Local unit checks (same family as Round 5)

`tools.test_cross_package_overlay` + `tools.test_verify_retrieval_context` + sources/DCO/CI/separation: **169** ran, **0** failed.

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
- KC-Brain confirmation of the Round-6 package `representations` map reading of overlay §2

## Hosted CI

Filled after `gh pr checks 81` on the Round-6 tip.
