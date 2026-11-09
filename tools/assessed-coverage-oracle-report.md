# Assessed-coverage finite oracle report (Layer S)

Marker: `kc-brain-oracle-pr82-k17-k18-semantic-adjudication-20261109-v1`.
Specification: arcanada-workspace PR1886 comment 6734249466; Muneral e445c6a4 (child of KCLIVE-08).
Round 4: KC-Brain re-pins K17/K18 (PR #82, comment 6736573962) at prior head
`0d3349fe1e3841787f9115aeb204d2c4ddfa9193`.

## Per-case results (S-layer)

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
| K01 | `K01-assessment-binding-missing.json` | `unknown` | `unknown` | assessment_binding_missing |
| K02 | `K02-member-entailment-unchecked.json` | `unknown` | `unknown` | member_entailment_unchecked |
| K03 | `K03-revisions-unpinned.json` | `unknown` | `unknown` | reviewer_revision_unpinned, rule_revision_unpinned |
| K04 | `K04-malformed-collection-records.json` | `fail` | `fail` | malformed_input |
| K05 | `K05-na-evidence-missing.json` | `unknown` | `unknown` | na_evidence_missing |
| K06 | `K06-malformed-required-profiles.json` | `fail` | `fail` | malformed_input |
| K07 | `K07-evidence-current-use-unverified.json` | `unknown` | `unknown` | evidence_current_use_unverified |
| K08 | `K08-time-fractional-stale.json` | `fail` | `fail` | evidence_validity_excludes_evaluation_time |
| K09 | `K09-wrong-bound-after-good.json` | `fail` | `fail` | binding_mismatch |
| K10 | `K10-evidence-identity-conflict-content.json` | `fail` | `fail` | evidence_identity_conflict, evidence_missing |
| K11 | `K11-temporal-candidate-order.json` | `pass` | `pass` | all_mandatory_members_discharged |
| K11b | `K11b-temporal-no-common-snapshot.json` | `unknown` | `unknown` | temporal_support_incoherent |
| K12 | `K12-na-scope-mismatch-after-valid.json` | `fail` | `fail` | not_applicable_authorized, na_scope_mismatch |
| K13 | `K13-member-rule-not-trusted.json` | `unknown` | `unknown` | member_rule_not_trusted_premise |
| K14 | `K14-member-caller-boolean.json` | `unknown` | `unknown` | caller_boolean_not_premise |
| K15 | `K15-independence-flag-string.json` | `fail` | `fail` | malformed_input |
| K16 | `K16-na-binding-missing.json` | `unknown` | `unknown` | na_binding_missing |
| K17 | `K17-no-support-time.json` | `unknown` | `unknown` | temporal_support_unverified |
| K17b | `K17b-mixed-support-time.json` | `unknown` | `unknown` | temporal_support_unverified |
| K18 | `K18-na-with-wrong-bound.json` | `fail` | `fail` | binding_mismatch, not_applicable_authorized |
| K18b | `K18b-na-wrong-bound-reversed.json` | `fail` | `fail` | binding_mismatch, not_applicable_authorized |

Fixture count: **58**. Positives S01, S04, S09, S16, S20 remain `pass` (unchanged;
all assessment-discharged positives already carried `support_time`).

## Round-4 rules (KC-Brain 6736573962)

### Q6 / K17 — assessment discharge needs demonstrated support time

Every member discharged by assessment must show at least one `support_time` on
a trusted binding-matched candidate. A coherent snapshot is one support_time
shared by every such member. Missing support time on any assessment-discharged
member — including the mixed missing/present case — yields closure `unknown` /
`temporal_support_unverified`; do not intersect over a partial mandatory set.
Members discharged only by a valid NA are exempt (S16 stays `pass`).

Optional positive control (separately declared trusted same-snapshot premise at
B0): **skipped** — no clean explicit field exists without inventing a default;
absent-by-default documentation would be speculative.

### Q8 / K18 — integrity before NA discharge

Evaluate every submitted assessment candidate for a member **before** the NA
discharge decision. A valid NA plus a wrong-bound assessment for the same
member yields closure `fail`, retains `binding_mismatch` and the NA's
`not_applicable_authorized` reason as evidence, and does **not** emit
`all_mandatory_members_discharged`. S16 (valid NA, no invalid companion) stays
`pass`. Reversed-order variant permutes both `assessments` and `na_decisions`.

### Letter-102 expectations (unchanged)

Assessment binding absent → `unknown` / `assessment_binding_missing`; unequal
B0 binding → `fail` / `binding_mismatch`. Unpinned reviewer/rule revision →
`unknown`. Missing current-use signals → `unknown` /
`evidence_current_use_unverified`. Good-plus-wrong-bound → `fail` /
`binding_mismatch`. Duplicate evidence identity with equal claimed digest and
different content → `fail` / `evidence_identity_conflict`.

## Round-4 K fixtures

| Defect | Fixture | Expected / observed | Reasons |
| --- | --- | --- | --- |
| Q6 all-absent | `K17-no-support-time.json` | `unknown` | temporal_support_unverified |
| Q6 mixed | `K17b-mixed-support-time.json` | `unknown` | temporal_support_unverified |
| Q8 NA+wrong-bound | `K18-na-with-wrong-bound.json` | `fail` | binding_mismatch, not_applicable_authorized |
| Q8 reversed | `K18b-na-wrong-bound-reversed.json` | `fail` | binding_mismatch, not_applicable_authorized |

## Mutation table

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
| `missing-binding-ok` | killed |
| `skip-revision-pin` | killed |
| `ignore-malformed-reason` | killed |
| `skip-na-evidence-resolve` | killed |
| `skip-profile-shape` | killed |
| `skip-current-use-signals` | killed |
| `lex-time-compare` | killed |
| `first-wins-assessment` | killed |
| `digest-only-evidence-identity` | killed |
| `ignored-revocation` | killed |
| `caller-boolean` | killed |
| `ungrounded-na` | killed |
| `last-write-dedup` | killed |
| `temporal-union` | killed |
| `harmless-addition` | killed |
| `copies-as-independent` | killed |
| `temporal-first-candidate` | killed |
| `skip-support-time-required` | killed |
| `na-before-assessments` | killed |
| `na-first-match` | killed |
| `skip-member-trust-mark` | killed |
| `string-independence-ok` | killed |
| `skip-na-binding-required` | killed |

Baseline unmutated scratch copy exits 0 before mutants run. Round-4 revert
mutants: `skip-support-time-required` (Q6) and `na-before-assessments` (Q8).

## KC-SWE probes

### `kcswe_or82p1b.py`

`BAD 0 of 25`.

### `kcswe_or82p3.py`

`BAD 1 of 14` — only **Q8**:

| Row | Status | Note |
| --- | --- | --- |
| Q1–Q7, controls | OK | Q6 now `unknown` / `temporal_support_unverified` |
| Q8 | BAD (probe gap) | Probe flips `member_id==b` on S16, but S16 has no b assessment (NA-only). Mutation is a no-op → still `pass`. Coordinator: leave S16 unchanged; K18/K18b are the witness. KC-SWE will fix the probe to inject a wrong-bound b assessment. |

## Unit tests

```sh
python3 -B -m unittest tools.test_assessed_coverage_oracle -v
```

Observed: `Ran 11 tests` … `OK` (58 fixtures via corpus subTests; deny stub;
seal; reason classification; permutation independence over K11/K12/K17/K17b/K18/K18b;
mutation harness with unmutated baseline).

## Limits

- Layer S only: synthetic semantics / structural conformance.
- N01–N06: **NOT_MEASURED**.
- No production trust, admission or authority claim.
- `effects_authorized` is always `false`; `scope` is always `synthetic_semantics_only`.
- book-package/2, G11 overlay, schemas, migrations, Auth/pricing and publication routes are unchanged.
- Optional trusted same-snapshot B0 premise control: not added (no clean field without inventing a default).

## How to run

```sh
python3 -B -m unittest tools.test_assessed_coverage_oracle -v
```

Wired in `.github/workflows/ci.yml` job `licensing`, same pattern as the G11 overlay corpus.
