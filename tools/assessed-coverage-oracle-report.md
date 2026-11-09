# Assessed-coverage finite oracle report (Layer S)

Marker: `agent-brain-assessed-coverage-oracle-20261109-v1`.
Specification: arcanada-workspace PR1886 comment 6734249466; Muneral e445c6a4 (child of KCLIVE-08).

## Per-case results

| Case id | Fixture file | Expected | Observed | Reasons |
| --- | --- | --- | --- | --- |
| S01 | `S01.json` | `pass` | `pass` | all_mandatory_members_discharged |
| S02 | `S02.json` | `unknown` | `unknown` | missing_assessment:b |
| S03 | `S03.json` | `unknown` | `unknown` | conjunction_incomplete |
| S04 | `S04.json` | `pass` | `pass` | all_mandatory_members_discharged |
| S05 | `S05.json` | `unknown` | `unknown` | member_entailment_unchecked |
| S06 | `S06.json` | `unknown` | `unknown` | missing_assessment:b |
| S07 | `S07.json` | `unknown` | `unknown` | required_profile_uninterpretable |
| S08a-absent | `S08a-absent.json` | `unknown` | `unknown` | mandatory_inventory_absent |
| S08b-empty-unjustified | `S08b-empty-unjustified.json` | `unknown` | `unknown` | empty_set_unjustified |
| S09 | `S09.json` | `pass` | `pass` | empty_set_justified |
| S10 | `S10.json` | `unknown` | `unknown` | unresolved_mandatory_dependency |
| S11 | `S11.json` | `fail` | `fail` | mandatory_conflict_established |
| S12a-revision | `S12a-revision.json` | `fail` | `fail` | binding_mismatch |
| S12b-actor | `S12b-actor.json` | `fail` | `fail` | binding_mismatch |
| S12c-resource | `S12c-resource.json` | `fail` | `fail` | binding_mismatch |
| S12d-environment | `S12d-environment.json` | `fail` | `fail` | binding_mismatch |
| S12e-recipient | `S12e-recipient.json` | `fail` | `fail` | binding_mismatch |
| S12f-payload | `S12f-payload.json` | `fail` | `fail` | binding_mismatch |
| S13a-revoked | `S13a-revoked.json` | `fail` | `fail` | evidence_revoked_for_required_use |
| S13b-stale | `S13b-stale.json` | `fail` | `fail` | evidence_validity_excludes_evaluation_time |
| S14a-unavailable | `S14a-unavailable.json` | `unknown` | `unknown` | evidence_service_unavailable |
| S14b-denied | `S14b-denied.json` | `fail` | `fail` | required_use_denied |
| S15a-caller-boolean | `S15a-caller-boolean.json` | `unknown` | `unknown` | caller_boolean_not_premise |
| S15b-unrecognized-revision | `S15b-unrecognized-revision.json` | `unknown` | `unknown` | unrecognized_reviewer_revision |
| S15c-invalid-provenance | `S15c-invalid-provenance.json` | `fail` | `fail` | invalid_provenance |
| S16 | `S16.json` | `pass` | `pass` | not_applicable_authorized, all_mandatory_members_discharged |
| S17a-caller-only | `S17a-caller-only.json` | `unknown` | `unknown` | caller_boolean_not_premise |
| S17b-wrong-scope | `S17b-wrong-scope.json` | `fail` | `fail` | na_scope_mismatch |
| S17c-missing-evidence | `S17c-missing-evidence.json` | `unknown` | `unknown` | na_evidence_missing |
| S18 | `S18.json` | `fail` | `fail` | assessment_identity_conflict |
| S19a-incompatible-times | `S19a-incompatible-times.json` | `unknown` | `unknown` | temporal_support_incoherent |
| S19b-applicability-violation | `S19b-applicability-violation.json` | `fail` | `fail` | temporal_support_incompatible_fail |
| S20 | `S20.json` | `pass` | `pass` | all_mandatory_members_discharged |
| S21a-unresolved-conflict | `S21a-unresolved-conflict.json` | `unknown` | `unknown` | mandatory_conflict_unresolved |
| S21b-established-inconsistency | `S21b-established-inconsistency.json` | `fail` | `fail` | mandatory_conflict_established |
| S22a-same-origin | `S22a-same-origin.json` | `fail` | `fail` | independence_same_origin |
| S22b-independence-unknown | `S22b-independence-unknown.json` | `unknown` | `unknown` | evidence_origin_missing |

## Deny-everything stub

A deny-everything stub returns `fail` for every input. Positive cases
S01, S04, S09, S16, S20 therefore fail the stub comparison (stub verdict
≠ pinned `pass`). Observed: all five positives reject the stub.

## Mutation table (section 5)

| Target | Result |
| --- | --- |
| `baseline_unmutated` | pass |
| `any-member` | killed |
| `any-evidence-conjunction` | killed |
| `one-to-one-cardinality` | killed |
| `shared-reference` | killed |
| `alias-counting` | killed |
| `producer-optional` | killed |
| `missing-as-empty` | killed |
| `skipped-binding` | killed |
| `ignored-revocation` | killed |
| `caller-boolean` | killed |
| `ungrounded-na` | killed |
| `last-write-dedup` | killed |
| `temporal-union` | killed |
| `harmless-addition` | killed |
| `copies-as-independent` | killed |

Baseline unmutated scratch copy exits 0 before mutants run. A mutant is
counted killed only on assertion failure, not crash/import error.

## Limits

- Layer S only: synthetic semantics / structural conformance.
- N01–N06: **NOT_MEASURED** (no production admission, Auth, budget, dispatch fencing, or live provider evidence).
- No production trust, admission or authority claim.
- `effects_authorized` is always `false`; `scope` is always `synthetic_semantics_only`.
- book-package/2, G11 overlay, schemas, migrations, Auth/pricing and publication routes are unchanged.

## How to run

```sh
python3 -B -m unittest tools.test_assessed_coverage_oracle -v
```

Wired in `.github/workflows/ci.yml` job `licensing`, same pattern as the G11 overlay corpus.
