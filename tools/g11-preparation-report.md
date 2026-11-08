# G11 bounded cross-package preparation — worker report

- **PR:** [knowledge-contract#81](https://github.com/Arcanada-one/knowledge-contract/pull/81) (DRAFT)
- **Head SHA:** `1adebf889c667e9d87f5b9b96a7a8a1d10d2cb71`
- **Branch:** `Arcanada/g11-cross-package-preparation`
- **Clone:** `/home/dev/aup/claude-work/kcswe-g11/knowledge-contract`

## Round 4 (strict input types / no crashes)

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (FailClosedRound4Tests on a51dbab) | 9 | 0 | 9 |
| Green-after (full `tools.test_cross_package_overlay`) | 52 | 52 | 0 |

### Sweep (`/tmp/g11r4_kcswe_sweep.py`, positive includes `revoked: false`)

- mutations **813**, exit0 **44**, crash **0** (was 787 / 204 / 16 on a51dbab)
- Remaining exit-0 paths are legitimate non-empty string equivalents:
  - `package_manifest_digest.byte_domain` / `source_revision` ∈ {`x`,`true`,`EN`,`a2`,`b1`} — required non-empty strings, open vocabulary
  - `packages.*.path` deleted (absent OK), `''`, or string tokens above — present path must be a string
  - `relation.from/to.object_id` string tokens above — required non-empty strings

### Probes (updated fixtures with `revoked: false`)

- probe1: positive exit 0 `scoped_inspection_ok`; refusals keep typed codes (endpoint_not_permitted, review_missing, …)
- probe2: positive exit 0; A9a exit 3; A9b exit 0 with `effects_authorized` false; `revoked="true"` exit 1 `malformed_input`
- Note: probe2 duplicate-key replace needle no longer matches after `revoked` was added to the fixture JSON; covered by unit test `test_r3_08_duplicate_json_keys_malformed`

## Prior rounds

| Stage | Ran | Passed | Failed |
| --- | ---: | ---: | ---: |
| Red-before (stub, commit 299a8d4) | 18 | 0 | 18 |
| Green-after (evaluator, commit 06d02df) | 18 | 18 | 0 |

## NOT_MEASURED

- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- overlays beyond exactly two canonical English packages
- released `cross-package-relations` wire schema registration

## Hosted CI (`gh pr checks 81` on 1adebf8)

All required checks **pass** (run 42498586179).
