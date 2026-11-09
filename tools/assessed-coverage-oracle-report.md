# Assessed-coverage finite oracle report (Layer S)

Marker: `kc-brain-pr82-f1-f2-semantic-adjudication-20261109-v1`.
Specification: PR #82 Agent-Brain review 6739618710; KC-Brain adjudication 6739733958; Muneral e445c6a4.
Round 5: F1 assessment identity (complete-record) + F2 established applicability violation.
Base reviewed head: `d85842508a1bdaae0015ece886f8726105fded6a`.

## Source blobs (working tree, pre-commit)

| Path | git blob SHA |
| --- | --- |
| `tools/assessed_coverage_oracle.py` | `971990aadf834148821981a7d46ad98b2fb01e6f` |
| `tools/test_assessed_coverage_oracle.py` | `ed51a87a76d70d4382fff9eb19caafc11505b4f8` |

## Per-case results (S-layer)

| Case id | Fixture file | Expected | Observed | Reasons | Fixture blob |
| --- | --- | --- | --- | --- | --- |
| K01-assessment-binding-missing | `K01-assessment-binding-missing.json` | `unknown` | `unknown` | assessment_binding_missing | `d1aba966edb2c771ff2ec3bc9d756fae2b457e4b` |
| K02-member-entailment-unchecked | `K02-member-entailment-unchecked.json` | `unknown` | `unknown` | member_entailment_unchecked | `56700029632a570ac1c257cf83b1680d8cf93a30` |
| K03-revisions-unpinned | `K03-revisions-unpinned.json` | `unknown` | `unknown` | reviewer_revision_unpinned, rule_revision_unpinned | `252879932e0ac1c08154a82b71f0d8b7a4a84ea3` |
| K04-malformed-collection-records | `K04-malformed-collection-records.json` | `fail` | `fail` | malformed_input | `9efffcbaf287d25dda12e7b026d306574b3f4399` |
| K05-na-evidence-missing | `K05-na-evidence-missing.json` | `unknown` | `unknown` | na_evidence_missing | `93237ab3b588feec2e20f05d983248ced40b553d` |
| K06-malformed-required-profiles | `K06-malformed-required-profiles.json` | `fail` | `fail` | malformed_input | `007087869871591f6f16f8d81c3f46acdf82e4d6` |
| K07-evidence-current-use-unverified | `K07-evidence-current-use-unverified.json` | `unknown` | `unknown` | evidence_current_use_unverified | `6c28139b81f9138d327a132af0ab18f8f61dd35f` |
| K08-time-fractional-stale | `K08-time-fractional-stale.json` | `fail` | `fail` | evidence_validity_excludes_evaluation_time | `0ab1340d70a27dbfbcdf78fd9f6ba75d8df4842e` |
| K09-wrong-bound-after-good | `K09-wrong-bound-after-good.json` | `fail` | `fail` | binding_mismatch | `ad8ae014bfb1d7284a334f2e4e6cef4b15604adf` |
| K10-evidence-identity-conflict-content | `K10-evidence-identity-conflict-content.json` | `fail` | `fail` | evidence_identity_conflict, evidence_missing | `b9b0d5740f5b044587060690df5f8653aa60646c` |
| K11 | `K11-temporal-candidate-order.json` | `pass` | `pass` | all_mandatory_members_discharged | `df1a0d4f1d1e364171a61155f04c7b3bf8afaca0` |
| K11b | `K11b-temporal-no-common-snapshot.json` | `unknown` | `unknown` | temporal_support_incoherent | `ccab5e6509f077c344b56b27b16c4eedcc048a1a` |
| K12 | `K12-na-scope-mismatch-after-valid.json` | `fail` | `fail` | not_applicable_authorized, na_scope_mismatch | `094407591867a1265ac0daa350c1972390923277` |
| K13 | `K13-member-rule-not-trusted.json` | `unknown` | `unknown` | member_rule_not_trusted_premise | `0a6ac796cdebedae67ba6b1a3cf30f4eaae82b83` |
| K14 | `K14-member-caller-boolean.json` | `unknown` | `unknown` | caller_boolean_not_premise | `8eea895ea7282b7a63c129b9d90afc0f943fa01a` |
| K15 | `K15-independence-flag-string.json` | `fail` | `fail` | malformed_input | `a1b059c9337221d7f89fc6dbd33ed77e42261c8d` |
| K16 | `K16-na-binding-missing.json` | `unknown` | `unknown` | na_binding_missing | `292c4b9207a6a7af1c017ab77dfd2288239443a7` |
| K17 | `K17-no-support-time.json` | `unknown` | `unknown` | temporal_support_unverified | `3b73f7e08e8e1b5612998c89e91ae74267211786` |
| K17b | `K17b-mixed-support-time.json` | `unknown` | `unknown` | temporal_support_unverified | `b0ffd85bdd3a5065ef3685973f2b6cb489119d55` |
| K18 | `K18-na-with-wrong-bound.json` | `fail` | `fail` | binding_mismatch, not_applicable_authorized | `96eccd68c5b7fe57018c55b1f51c3d6fac86701c` |
| K18b | `K18b-na-wrong-bound-reversed.json` | `fail` | `fail` | binding_mismatch, not_applicable_authorized | `36a37f89f4ad92841edcfc0bfc7f56a147c489a9` |
| K19-assessment-identity-content-conflict | `K19-assessment-identity-content-conflict.json` | `fail` | `fail` | assessment_identity_conflict, missing_assessment:a | `a6208ac7be6f4c13dbb9952f29d47e4efeac49a8` |
| K19b-assessment-identity-content-conflict-reversed | `K19b-assessment-identity-content-conflict-reversed.json` | `fail` | `fail` | assessment_identity_conflict, missing_assessment:a | `e4731845d191f247dd7044c12f25c0eaa3873cd0` |
| K20-assessment-identical-duplicate | `K20-assessment-identical-duplicate.json` | `pass` | `pass` | all_mandatory_members_discharged | `a39e3f41b27fc81033a346bad734d30a47a33788` |
| K21-applicability-coincident-established | `K21-applicability-coincident-established.json` | `fail` | `fail` | applicability_violation_established | `5e7d3837ac889ec4abde1faf40b1e880278b963f` |
| K21b-applicability-coincident-absent | `K21b-applicability-coincident-absent.json` | `pass` | `pass` | all_mandatory_members_discharged | `f08014275d3380d903df225e6c01f890389d9a3a` |
| K21c-applicability-flag-wrong-bound | `K21c-applicability-flag-wrong-bound.json` | `fail` | `fail` | binding_mismatch | `2b80f0f6a1e52503ae48d02cb6ea2531f6e7f25f` |
| S01 | `S01.json` | `pass` | `pass` | all_mandatory_members_discharged | `90a839688036fdd77c6cedecae4bd01a7598d534` |
| S02 | `S02.json` | `unknown` | `unknown` | missing_assessment:b | `514cd736a5d2b5d99607965e995a8cb081f77ec9` |
| S03 | `S03.json` | `unknown` | `unknown` | conjunction_incomplete | `4c3566aa1e234531c7cf485e4101fe9dd2de963a` |
| S04 | `S04.json` | `pass` | `pass` | all_mandatory_members_discharged | `f93765ff59d2465629e5f941b8ba2c1df48f7cca` |
| S05 | `S05.json` | `unknown` | `unknown` | member_entailment_unchecked | `5e57d3f4e69ef4775ee38bbd45df337b2bb46600` |
| S06 | `S06.json` | `unknown` | `unknown` | missing_assessment:b | `15a12dc1fe8a70bd6ea1f6282dbda7cbbb69f128` |
| S07 | `S07.json` | `unknown` | `unknown` | required_profile_uninterpretable | `19fbd2480d496aeaf7bfebe05807b960fd202ba9` |
| S08a-absent | `S08a-absent.json` | `unknown` | `unknown` | mandatory_inventory_absent | `16e0b36dea134269f0b4aac1964ed6a84c718b79` |
| S08b-empty-unjustified | `S08b-empty-unjustified.json` | `unknown` | `unknown` | empty_set_unjustified | `a79e063435515c9de31518aa05b3c57608253eff` |
| S09 | `S09.json` | `pass` | `pass` | empty_set_justified | `d2e2e4c58267493b825d0ec4ef6286b8b8d65729` |
| S10 | `S10.json` | `unknown` | `unknown` | unresolved_mandatory_dependency | `62f6fc6b5ff72b2932430ca8dab89793fc3114ae` |
| S11 | `S11.json` | `fail` | `fail` | mandatory_conflict_established | `27afc71853895c1312d73021c99b982119cd014f` |
| S12a-revision | `S12a-revision.json` | `fail` | `fail` | binding_mismatch | `f5860bcd466d52046e4866c883088c0ed9c3a897` |
| S12b-actor | `S12b-actor.json` | `fail` | `fail` | binding_mismatch | `89eec9869e09cb8d1bd83aec682cd5c3f098e831` |
| S12c-resource | `S12c-resource.json` | `fail` | `fail` | binding_mismatch | `62b4aa11380cf579a2f6e8eb7cc5f2577644c65f` |
| S12d-environment | `S12d-environment.json` | `fail` | `fail` | binding_mismatch | `8952f7676d24c2be84cd05f8ded8b14e42dfd25e` |
| S12e-recipient | `S12e-recipient.json` | `fail` | `fail` | binding_mismatch | `dd8126a3fe8f16ddb96dffcdd6265003f30957ce` |
| S12f-payload | `S12f-payload.json` | `fail` | `fail` | binding_mismatch | `1185a771f0514d70130f7ad1cead0677a19394f8` |
| S13a-revoked | `S13a-revoked.json` | `fail` | `fail` | evidence_revoked_for_required_use | `b2f3a4793f0c34240f6d0b39305c9552b16359ec` |
| S13b-stale | `S13b-stale.json` | `fail` | `fail` | evidence_validity_excludes_evaluation_time | `301c889a019451f828dde6c30dd4d8f560cb439b` |
| S14a-unavailable | `S14a-unavailable.json` | `unknown` | `unknown` | evidence_service_unavailable | `4b32d41f92aa0b9d1a8a8618cc9836e896bdee7b` |
| S14b-denied | `S14b-denied.json` | `fail` | `fail` | required_use_denied | `f92c4ada608ecc5557618b6d2570b763f1c3244e` |
| S15a-caller-boolean | `S15a-caller-boolean.json` | `unknown` | `unknown` | caller_boolean_not_premise | `ccdec095dc1d47a90250c4a2e16bce945e2bd909` |
| S15b-unrecognized-revision | `S15b-unrecognized-revision.json` | `unknown` | `unknown` | unrecognized_reviewer_revision | `72c9643e08a8a39579287912dbcb293b37d4e616` |
| S15c-invalid-provenance | `S15c-invalid-provenance.json` | `fail` | `fail` | invalid_provenance | `d1a9dcc1244b1c79a8c26f7b700615cb6c6f35d7` |
| S16 | `S16.json` | `pass` | `pass` | not_applicable_authorized, all_mandatory_members_discharged | `ac8fc9cd63b1fd59255889ad2c7a8d699c61d588` |
| S17a-caller-only | `S17a-caller-only.json` | `unknown` | `unknown` | caller_boolean_not_premise | `34cba31d440c2cd8df873767d3c2245989e35e31` |
| S17b-wrong-scope | `S17b-wrong-scope.json` | `fail` | `fail` | na_scope_mismatch | `b10a7d973a2fde12fc3dfc71165b9f2e0e097e42` |
| S17c-missing-evidence | `S17c-missing-evidence.json` | `unknown` | `unknown` | na_evidence_missing | `73f4a833b28e5e49417bdefe8d4c21ff79c1455c` |
| S18 | `S18.json` | `fail` | `fail` | assessment_identity_conflict, missing_assessment:a | `9b4a5b5860bc026718304f1b82fe0090a6589d18` |
| S19a-incompatible-times | `S19a-incompatible-times.json` | `unknown` | `unknown` | temporal_support_incoherent | `2f845145e582df866911dd7709e9173286357dbe` |
| S19b-applicability-violation | `S19b-applicability-violation.json` | `fail` | `fail` | temporal_support_incompatible_fail, applicability_violation_established | `1a2e7b68df97bdf08bf36afc3b6fb86b15121c76` |
| S20 | `S20.json` | `pass` | `pass` | all_mandatory_members_discharged | `55254e9e5cba872e619cc586ce0f603d6f1d5e65` |
| S21a-unresolved-conflict | `S21a-unresolved-conflict.json` | `unknown` | `unknown` | mandatory_conflict_unresolved | `75248d6c7ae8caef28d48dcd5943d453e6a97490` |
| S21b-established-inconsistency | `S21b-established-inconsistency.json` | `fail` | `fail` | mandatory_conflict_established | `c4404491135e0d5ce1d2ce0ce81e943c72393bb1` |
| S22a-same-origin | `S22a-same-origin.json` | `fail` | `fail` | independence_same_origin | `35c35aee818a1e5631097763d7e259d300105de2` |
| S22b-independence-unknown | `S22b-independence-unknown.json` | `unknown` | `unknown` | evidence_origin_missing | `54fc6751b132de1b4e29486aaa936b9927491d35` |

Fixture count: **64**. Positives S01, S04, S09, S16, S20 remain `pass`. New useful controls: K20 (identical duplicate pass), K21b (coincident applicability absent pass).

## Round-5 rules (KC-Brain 6739733958)

### F1 — assessment identity

`assessment_id` denotes one immutable content identity. Matching *claimed*
`immutable_bytes_digest` / `revision_claim` does not prove content equality.
Complete-record inequality ⇒ `fail` / `assessment_identity_conflict`; the id is
dropped (like `_evidence_index`) so neither record discharges the member. Identical
complete records collapse to one. Applied at admission before discharge/temporal.

### F2 — established applicability violation

Trusted, B0-matched `applicability_violation_established: true` forces
`fail` / `applicability_violation_established` even when support times coincide.
Incompatible times still emit `temporal_support_incompatible_fail`; when both hold,
both reasons are reported. Untrusted/wrong-bound flags grant nothing. Established
violation dominates missing-support UNKNOWN. Flag name unchanged.

## S18 re-pin (coordinator ruling A)

Dropping the conflicted `assess-a` identity changes member discharge. Allowed re-pin:

- Before blob `61e7cd83781338ff6d0599e4ee52bdcb605f7db4`: `{"addressed_members": ["a", "b"], "closure_verdict": "fail", "effects_authorized": false, "member_verdicts": {"a": "discharged", "b": "discharged"}, "missing_members": [], "reason_codes": ["assessment_identity_conflict"], "scope": "synthetic_semantics_only", "unresolved_dependencies": []}`
- After blob `9b4a5b5860bc026718304f1b82fe0090a6589d18`: expected closure `fail`; reasons contain `assessment_identity_conflict` and `missing_assessment:a`; member_verdicts `a=missing_assessment`, `b=discharged`; addressed `[b]`; missing `[a]`.

## S19b reason re-pin

- Before blob `e17b936cbe40300a2c7c89cf2d14256892adcac4`: reasons `['temporal_support_incompatible_fail']`
- After blob `1a2e7b68df97bdf08bf36afc3b6fb86b15121c76`: reasons `['temporal_support_incompatible_fail', 'applicability_violation_established']` (closure still `fail`).

## New discriminators

| Fixture | Expected | Observed | Notes |
| --- | --- | --- | --- |
| `K19-assessment-identity-content-conflict.json` | `fail` / assessment_identity_conflict, missing_assessment:a | `fail` / assessment_identity_conflict, missing_assessment:a | members {'a': 'missing_assessment', 'b': 'discharged'} |
| `K19b-assessment-identity-content-conflict-reversed.json` | `fail` / assessment_identity_conflict, missing_assessment:a | `fail` / assessment_identity_conflict, missing_assessment:a | members {'a': 'missing_assessment', 'b': 'discharged'} |
| `K20-assessment-identical-duplicate.json` | `pass` / all_mandatory_members_discharged | `pass` / all_mandatory_members_discharged | members {'a': 'discharged', 'b': 'discharged'} |
| `K21-applicability-coincident-established.json` | `fail` / applicability_violation_established | `fail` / applicability_violation_established | members {'a': 'discharged', 'b': 'discharged'} |
| `K21b-applicability-coincident-absent.json` | `pass` / all_mandatory_members_discharged | `pass` / all_mandatory_members_discharged | members {'a': 'discharged', 'b': 'discharged'} |
| `K21c-applicability-flag-wrong-bound.json` | `fail` / binding_mismatch | `fail` / binding_mismatch | members {'a': 'fail', 'b': 'discharged'} |

K21c: coincident times with `applicability_violation_established=true` on a wrong-bound
`assess-a`. Existing B0 gate yields `fail` / `binding_mismatch` only — the flag does **not**
emit `applicability_violation_established`.

## Mutation table

Unmutated baseline run first: pass. Round-5 revert mutants:

| Mutant | State |
| --- | --- |
| baseline_unmutated | pass |
| digest-only-assessment-identity (F1 revert) | killed |
| skip-applicability-coincident (F2 revert) | killed |
| last-write-dedup (updated for F1) | killed |
| temporal-union / skip-support-time-required (needles retargeted) | killed |
| all other prior section-5 mutants | killed |

## Probes at this tree

- `/tmp/kcswe_or82p1b.py`: BAD 0 of 25
- `/tmp/kcswe_or82p5.py`: BAD 0 of 19 (Q3 now fails with `assessment_identity_conflict`)

## Native tests

`python3 -B -m unittest tools.test_assessed_coverage_oracle` → 11 tests OK.

## Boundaries

No book-package/2, G11, schemas, migrations, Auth/pricing, routes changes.
No second oracle, no Boolean parser, no real producer trust markers, `effects_authorized=false`.
PR remains draft; no merge/release.
