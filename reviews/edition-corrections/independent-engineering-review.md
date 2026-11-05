# Independent engineering review — edition 1.1

**Final finding: no confirmed unresolved blocker in the bounded reviewed scope.** The critical rights/readiness/digest/status gates passed the exercised local controls. Two concrete defects are preserved below with their verification history: independent finding IER-01 and root-discovered INT-01 are both resolved. Proceeding with the edition corrections is supported within this profile; this report does not certify full interoperability, a production deployment, authenticated evidence, or runtime admission.

## Confirmed findings and resolution

### IER-01: Internal directory symlinks bypass the no-symlink component-path rule

Severity: **medium**. Final status: **resolved_independently_verified**. Discovery: independent_engineering_review.

Start with the valid synthetic RLE package. Copy objects.jsonl to real/objects.jsonl, create alias -> real inside the package, change components.objects.path to alias/objects.jsonl while preserving its correct digest. check_package accepted the package and candidate_projection produced three candidates.

Only the final path entry was lstat-checked; ancestor directory symlinks inside the root passed resolution containment.

Mismatch with the specified no-symlink gate. The reproduction stays inside the package root and preserves hashes; it does not establish a rights bypass, an out-of-root read, or a digest bypass.

Maintainer changed safe_file to reject absolute/parent traversal paths and lstat each component below the supplied package root: real directories for intermediate entries and a regular final file. Source inspection confirmed the change.

**Before/after evidence:** the unchanged standalone regression ran before the fix with exit 1 (3 tests in 0.687s); the directory-symlink assertion failed while its normal-directory control and both INT-01 cases passed. After the correction, the same script returned exit 0 (3 tests in 0.645s). A regular nested path still validates and yields three proposals; the directory-symlink path is rejected and yields zero.

Checker SHA256 before fix: `fbb101808055f79222ee866287c0d0fc042f25e06e1a7bb24689ba942ed7ee4c`. After fix: `290ed9251ff923aeb21dc42e6e67297d054e5a3ddf5957beea1cb8221f5b813f`.

### INT-01: Exhausted dependency counter must block publication after an unrecordable revocation

Severity: **high**. Final status: **resolved_independently_verified**. Discovery: root integration reviewer, not the independent reviewer.

Root reported that change(authority, revoked=True) raised at MAX_EPOCH but publish of the unchanged read set returned True. This review did not execute the pre-fix version.

publish now rejects if any current dependency epoch equals MAX_EPOCH.

Constructed authority epoch MAX_EPOCH with generation zero, observed change(..., revoked=True) raise ProfileError, then verified old and fresh read sets both fail to publish and head stays None. Also advanced MAX_EPOCH-1 through the final normal change and verified fresh publication fails with head None.

In-memory epoch/revocation subset only; output grants, semantic validity, build checks and distributed persistence are not established.

## What the evidence supports

### Restricted and unknown rights

**pass_in_exercised_scope**. Both classes validate as private packages with no license and empty publishable_layers, and emit zero projection rows. Adding CC-BY-4.0 plus knowledge publication causes validation errors and zero rows. Existing regression suite additionally exercises license/layer combinations and render refusal.

### Supported independent complete ready review

**pass_in_exercised_scope**. Independent mutations of unsupported result, same_session_agent, same reviewer/producer identity, incomplete relation scope, candidate object, and failed/unknown/empty extraction checks cannot retain knowledge_ready and produce no export proposals. Existing suite also exercises partial reviews, all object/relation statuses, sample counts, missing object scope and assessment references.

### Digest-bound review and edit binding

**pass_in_exercised_scope**. An incorrect review objects hash and changed semantic text without review rebinding are rejected. Existing ledger/render tests exercised accepted-edit overlap even with an empty declared dependency list, stale relation propagation and exact replay. The separate independent stale-edit mutation failed at replay, so it is not counted as an isolated test of anchor-impact detection.

### Status derivation and legal unverified state

**pass_in_exercised_scope**. Existing test group executed the finite 3,240-combination derivation table. Independent unverified representation with partial_pilot accepted. The first independent probe used nonexistent knowledge_partial; that was a reviewer error, preserved and corrected, not a defect.

### Projection/render and attribution containment

**pass_in_exercised_scope_after_ier01_fix**. Read source for immutable snapshot validation, internal rendering and digest projection; existing tests executed arbitrary-input refusal, render hash binding, full-record retention and adversarial Markdown heading/fence cases. IER-01 was a separate explicit component-path mismatch, now fixed and independently retested with a normal nested-directory positive control.

### Strict exchange JSON and finite epochs

**pass_in_exercised_scope**. Independent decoder probes reject duplicate and nested duplicate members, overflow 1e999, NaN, UTF-8 BOM, and escaped surrogate keys/values. Existing tests additionally exercise exact-byte digest identity, event monotonicity and rollback/ABA. INT-01 retested independently.

### Requirement register

**pass_for_consistency_and_reference_resolution**. Final checker confirms 283 numbered requirements match the source register; final AST inspection resolves all 18 cited methods, including the BPK-R005 path regression. These finite references are examples, not proof of complete clause implementation.

### API receipt shape and decision vocabulary

**pass_for_synthetic_schema_controls**. Five tests run as part of C02, including 2,187 combinations, required checks and path/identity/date controls. The harness explicitly supplies the existing UTC-seconds format checker; it does not establish all RFC3339 support or default-validator format assertions.

## Commands actually executed

Interpreter: `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python`. jsonschema: **4.23.0**. Working directory: `/workspace/scratch/4a4b36d07b29/knowledge-contract/tools`.

These test runs overlap; their counts are not added into a purported unique-test total. The 98-test run preceded the later fixes. The 21-test run includes the corrected publication model and the five receipt tests. The final focused run checks the actual source after the symlink correction. I did not repeat or claim ownership of the maintainer’s full integration gate.

- **C01** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B -m unittest test_book_package test_build_book_package test_book_package_review test_contract_profile -v` — exit 0; Ran 98 tests in 8.350s; OK Before the root INT-01 and IER-01 patches; retained as actual earlier execution evidence, not as a test run against the final hashes.
- **C02** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B -m unittest test_contract_profile test_index_release_receipt` — exit 0; Ran 21 tests in 3.013s; OK After INT-01 correction and before IER-01 correction.
- **C03** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B check_requirement_register.py` — exit 0; REQUIREMENT_REGISTER_PASS requirements=283
- **C04** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B - <<'PY' (inline independent mutation harness; tool transcript contains exact source)` — exit 0; 26 observations: 24 expected outcomes, one invalid reviewer-harness input, one confirmed product finding IER-01. Exit zero means the harness completed; it did not assert all observations passed.
- **C05** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B - <<'PY' (corrected unverified-state probe)` — exit 0; unverified + partial_pilot accepted with zero errors
- **C06** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B - <<'PY' (AST resolution of requirement-register method references)` — exit 0; 17 unique references, zero missing
- **C07** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B /workspace/scratch/4a4b36d07b29/edition-review-input/independent-engineering-review-reproduce.py` — exit 1; Ran 3 tests in 0.687s; FAILED (failures=1). IER-01 failed; INT-01 checks passed. Before the IER-01 correction; intentional failing control.
- **C08** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B /workspace/scratch/4a4b36d07b29/edition-review-input/independent-engineering-review-reproduce.py` — exit 0; Ran 3 tests in 0.645s; OK. After the IER-01 correction; unchanged independent reproduction and positive control.

- **C09** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B check_requirement_register.py` — exit 0; REQUIREMENT_REGISTER_PASS requirements=283 Final rerun after the traceability-only BPK-R005 regression reference was added.
- **C10** — `/workspace/scratch/4a4b36d07b29/kc-restructure-review/finish-python-env/bin/python -B - <<'PY' (final AST resolution of requirement-register method references)` — exit 0; 18 unique references, zero missing Final rerun after the BPK-R005 regression reference was added. C06 retains the historical 17-reference result.

The inline probe observations are preserved in `independent-engineering-probes.json`. Its original apparent status failure was caused by my use of the nonexistent `knowledge_partial` value; the corrected `partial_pilot` probe passed and is preserved separately. That harness error is not a product finding. The separate stale-edit mutation was rejected at replay, so it does not independently isolate anchor-impact detection; the existing ledger tests provide that regression evidence. C07 intentionally captures the real pre-fix path failure, and C08 captures its resolution.

## Scope and limitations

AGENTS.md; original ES01–ES28 review; book schema, validator, fixture builder, builder and regression tests; book specification; contract-observation schema and full bounded validator/model; relevant cache/status/profile boundaries; API receipt schema and test harness; requirement-register generator and references. Some long file reads were partial or truncated: this is not a claim of line-by-line review of every specification and test.

The hash inventory covers the implemented review surface and related registered specifications/fixtures. Hashing a file is not evidence that every line was reviewed.

- Full interoperability across every Knowledge Contract document or profile
- Production API deployment, actual index observations, remote identity authentication or cross-record receipt correspondence
- Authenticity of a declared human/blind-agent reviewer, source-rights claims, integrity observer or expected source digest
- Truth of semantic records, extraction fidelity on arbitrary corpora, unseen formats or independent scientific validity
- Distributed linearizability, persisted nonreused counters, namespace migration, output-specific authority grants or complete runtime admission
- Hostile concurrent filesystem replacement resistance or an OS-level race-free path-open boundary
- Exhaustive fuzzing, complete renderer/browser security, all Unicode or RFC3339 forms
- Reproduction of the parent integration review, site build or external delivery

The schema controls establish structural restrictions and deterministic local decisions for synthetic inputs. They do not authenticate evidence or prove that a real service observed what a receipt claims. The publication model explicitly covers epochs and revocations; its source and cache-spec description separate that subset from output-specific grants, semantic validity and build checks. A receipt may satisfy its schema without establishing cross-record correspondence: the specification assigns those checks to the operator and the local tests do not implement an API.

The receipt tests explicitly use the existing UTC-seconds format checker because the minimal dependency set does not activate every optional JSON Schema format assertion. The observed date controls therefore establish the exercised UTC-seconds subset only, not general RFC3339 acceptance or an assertion that every default schema consumer validates formats.

## Source identity

Branch: `edition-review-corrections`. Published base/current uncommitted working-tree HEAD: `ed2e188c89a1a50a187f3d55bf32baab54c87f7e`. Edition: 1.1. Finalized: `2026-11-04T20:14:51.097304+00:00`. The corrected source is identified by the final SHA256 inventory below; this reviewer created no commit.

Original ES01–ES28 review SHA256: `359c7ce3bceddc5d990c8b65ca4bfb2d33164c15922fdaf13ea3e7bf270dc4c6`.

| File | SHA256 |
| --- | --- |
| `AGENTS.md` | `2e64614a966402ca765f5cff872a71151b29cdfb590a54bfaa8c8a96b47c2726` |
| `appendices/api-integration/APPENDIX.md` | `2e1c800cf2bb1c61696e34d516b23db1f3f65fa7c58f983bf3124c17854cefe3` |
| `appendices/api-integration/index-release-receipt.schema.json` | `ea2b221bde19cce079c5aa23482a216e10d2a0880138056d00808cf80a691b22` |
| `engineering/specifications/artifact-registry/SPECIFICATION.md` | `ec6584f97c5160fd3c8b17a5036aaeb8d302bf86dd61e567f2c5d858e9159470` |
| `engineering/specifications/book-package/SPECIFICATION.md` | `1ce2ce4fa9e0e2647b3472f1da0a250fa3abae00c78b7518d3497f106c09722c` |
| `engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md` | `742982eabd0d797ccc5bba4c8472d25a4236c84baed21281f13a7601a4ce2f39` |
| `engineering/specifications/compiled-artifact-contract/SPECIFICATION.md` | `2cc5e781565136b5ad9fdbb2facae47d58564b1e300173d0a91a2c6cf16d5a82` |
| `engineering/specifications/context-package/SPECIFICATION.md` | `5bba82777b44dc0cf6b1b0c218292c1476c0271806acef195db6c3b8a9448e41` |
| `engineering/specifications/contract-family/SPECIFICATION.md` | `310cd3f151275739a2391d2c8d8b7c23ad64b46f4c1a56717f7f0975866f60c8` |
| `engineering/specifications/knowledge-contract-core/SPECIFICATION.md` | `81cb01a8326eaeb0c14e929609c52cc85e5a344c61f3744d2e0def228cdc60d5` |
| `engineering/specifications/knowledge-evolution/SPECIFICATION.md` | `4662bdd76c5716cb7d9b55c1b99e00dda626b34c3565e2f03ceecb61fe15685a` |
| `engineering/specifications/requirements.json` | `cd10119f474d290054236ab949c6583ed9d931fd5dffe47a75ad68d718feb0fd` |
| `engineering/specifications/reuse-policy/SPECIFICATION.md` | `be75f0191414c07a113dafb0c983cd1d1e73834be0b670e0d610b4354f37ecd2` |
| `engineering/specifications/semantic-types/SPECIFICATION.md` | `4428c3cdacfe5e8bcf00b8d9100a79f5ce9691edecd914063698bfb3f97e8f6f` |
| `engineering/specifications/status-model/SPECIFICATION.md` | `2f66342472fc4198eba573d7d1eda5d58d5bae9de904f901f5094037dd628d0a` |
| `schemas/book-package.schema.json` | `51fd39c38c4f7cedd19b8bf1b05186ec581450ecc76e0f8f610024a094ed9ca9` |
| `schemas/contract-observation.schema.json` | `11bd4770448a2bab5214d8d984b4645390d3b14c84760447079afc98b7505cf6` |
| `schemas/fixtures/book-package/invalid/edit_blank_reason.json` | `a567fa465ec23e80c52c9628f0fdbeb3a328c6d4344d1b117bdcb2b25580eb9b` |
| `schemas/fixtures/book-package/invalid/edit_irreversible.json` | `a7d9f5e171c9730e4e7c8d558eaf250ac4db3f5fc129e3265e2638afb11837d4` |
| `schemas/fixtures/book-package/invalid/edit_unknown_basis.json` | `3e4e2d2b1b12adf1fe676d4d7988cefd24810ac67f14e2c76ea9f57a8f12f600` |
| `schemas/fixtures/book-package/invalid/edit_unsupported_asset_text.json` | `c51e8a99b58a293a2d58df9b6a60d4446ee55bb7cea1421845616aff36097fe1` |
| `schemas/fixtures/book-package/invalid/edit_without_reason.json` | `ea13c46f0c69105dfbf9f7b61bb645ff07a68d6d0e5438cd6b6467c2f05fa261` |
| `schemas/fixtures/book-package/invalid/manifest_absolute_path.json` | `8eada38ab99bf21b63f05d87d33c1fb828e9180ca12c17d9156c4523ee703203` |
| `schemas/fixtures/book-package/invalid/manifest_admitted_by_itself.json` | `58fe10892cfd583c8c3e7007d2bf8509ef51f30b130ea7150e2688b008e06c67` |
| `schemas/fixtures/book-package/invalid/manifest_bibliography_only_with_document.json` | `920077c59dcc3895260d4bf228f853ed92cfdd0f06088fbc98c0296226cca398` |
| `schemas/fixtures/book-package/invalid/manifest_document_md_marks_generated_text.json` | `0fe518edc05205a0686dafc773e5c1401bf392ffe7f6592671ac1a0d98c3e020` |
| `schemas/fixtures/book-package/invalid/manifest_integrity_without_observer.json` | `a42f37d8dc0e5243a8863858087c10295ba0ba6e2463f5cb02ccb3efaaf269f6` |
| `schemas/fixtures/book-package/invalid/manifest_legacy_profile.json` | `6a05b50ed86da94b32dbc62f71588a0d0307603d88929d497a6d065519a1a191` |
| `schemas/fixtures/book-package/invalid/manifest_mismatch_but_ready.json` | `3045e4b93e27f7f97702e302db6d4b89a93f0652c9f7823701ad968be8fa3617` |
| `schemas/fixtures/book-package/invalid/manifest_missing_asset_with_path.json` | `bd4dad1f8ae1cd5407610008fc1b45fcdd456aa590fe1d3b9d272b05f4dc7b8b` |
| `schemas/fixtures/book-package/invalid/manifest_missing_profile.json` | `9b5ca05b6debb6395e80dbc1ceb0102160a03e95d885d6fbe06be242678a41d5` |
| `schemas/fixtures/book-package/invalid/manifest_non_https_locator.json` | `b690ac15b2edc923c3aa969776d77407fedd22628b1c7f63236fdb12812ea276` |
| `schemas/fixtures/book-package/invalid/manifest_package_id_colon.json` | `9470f08f94e3710b478d5c2bf03907c1e1e6690e1985c825ac48716b810a11ea` |
| `schemas/fixtures/book-package/invalid/manifest_path_traversal.json` | `fcbca7dfb39717a5a6d7e6a55634371616cc18010de860dae7f5ba1cbd77cd4f` |
| `schemas/fixtures/book-package/invalid/manifest_ready_but_partial.json` | `33bc910dee257e5e6b70a9add5af095f2afcb547a8b3aa8e4fcf1004d722a45f` |
| `schemas/fixtures/book-package/invalid/manifest_restricted_knowledge_layer.json` | `4170981bc846f5d4e0a87c44aa471968837c9880f53060dfc1adf38a8326c72e` |
| `schemas/fixtures/book-package/invalid/manifest_restricted_open_license.json` | `5ff754b99691f3614478faeda51bd2b86f4818a0440c2257c0d41f6c56f003a4` |
| `schemas/fixtures/book-package/invalid/manifest_unknown_open_license.json` | `fd2cc399bc1435a9ca5aa3141de3af6771d14a2eee766ccb427201dc24634f51` |
| `schemas/fixtures/book-package/invalid/object_admitted_by_itself.json` | `da0aa79d5fca40fedd4d46faf2292ee203d34fd08ac94de797825291a1846748` |
| `schemas/fixtures/book-package/invalid/object_anchor_bad_sheet_range.json` | `c72a9519c5277faf80351a38d9570d7fae8668631c06e2ea79df9e27e98376e4` |
| `schemas/fixtures/book-package/invalid/object_anchor_bbox_three_numbers.json` | `ac896d38b667e5b56b96b9aaed5753905a94814d9c0e39d9d3dd20629092952d` |
| `schemas/fixtures/book-package/invalid/object_anchor_page_zero.json` | `989c48c23f3d5c87536e909e872ee32d00ae1c59c4eb569bbf7e8a51e4098f04` |
| `schemas/fixtures/book-package/invalid/object_anchor_pointer_without_slash.json` | `3f85d2645a0990138e70bd894a959f27d2f00592f565e7b3d3edca9c252eb386` |
| `schemas/fixtures/book-package/invalid/object_anchor_unknown_kind.json` | `dabf9cecec635899258384b47a50f47c9d3fa1b4e477b5a18b443f642ae12b84` |
| `schemas/fixtures/book-package/invalid/object_anchor_wrong_hash.json` | `5ae226f58f50647e683a5b883e60a7ac41082d709fc752091037e0a029c2a2e4` |
| `schemas/fixtures/book-package/invalid/object_author_with_generation.json` | `61dda3fb00f5a007652c66180ef86042984d5260702fbd7a6169cbdfae840812` |
| `schemas/fixtures/book-package/invalid/object_benchmark_without_context.json` | `59859344d375564871cfb0889fde7dd7697e67d1bd2ea49998a7b595c2c9c5ea` |
| `schemas/fixtures/book-package/invalid/object_empty_text.json` | `4a5ea2b4b07d014283a0d7718901e4ec43a4839ece89800888ba318286787e8b` |
| `schemas/fixtures/book-package/invalid/object_extra_field.json` | `d62310695ce77cbdd7713bd0b030ced4bdfd9f30cd3162624de654f487d4ec3b` |
| `schemas/fixtures/book-package/invalid/object_generated_presented_as_author.json` | `5e24fc91748f5991b5eb8e3ca4caaed1606902e167161ea2e0007413a174df22` |
| `schemas/fixtures/book-package/invalid/object_generated_without_generation.json` | `95b46320de4498d827ff4ca60ab2feb588401337986269566b0f194fa0ea6cca` |
| `schemas/fixtures/book-package/invalid/object_known_with_empty_kinds.json` | `ac5fdd1a23ae766f205005d931b9555f2dd0c0dd661d3da8b3dc7b312bdee50f` |
| `schemas/fixtures/book-package/invalid/object_missing_facet.json` | `78b601b0a1bb8989309a01e4e8a644bf1855c0045efbb233c29e8da06677b7dd` |
| `schemas/fixtures/book-package/invalid/object_no_evidence.json` | `270505c5128beee2275138b6e511020b1a1944fb7dea514812d7cc72e2f45f7b` |
| `schemas/fixtures/book-package/invalid/object_unknown_content_kind.json` | `2729b4fc25baacd0e2d21a4ab6f95dc2a5694874379eb5a0625d343aabddb04a` |
| `schemas/fixtures/book-package/invalid/object_unknown_without_reason.json` | `23780f98b8cef4a37cc2a5e417e675ca4982364b70f528c47b2f9b8121d3958f` |
| `schemas/fixtures/book-package/invalid/quality_cer_null_but_measured.json` | `f49fc871bb40e85481907bf71e0e5b4b12f6b693789b2bc7ce1128f09c320f7f` |
| `schemas/fixtures/book-package/invalid/quality_cer_zero_without_reference.json` | `a1dfa146421475494840ec81c6e46da56317288adf2a1bcc1a31b7887d15314b` |
| `schemas/fixtures/book-package/invalid/quality_na_without_basis.json` | `0dbd85a88be8210c18dac616830f297445bf0a542634caac365ac7a71ba2215a` |
| `schemas/fixtures/book-package/invalid/quality_not_built_with_objects.json` | `5ecf131d5cb8af323e24fdc5192e07740a8e012b53dd4f9ad72e0a59208326b6` |
| `schemas/fixtures/book-package/invalid/quality_overall_score.json` | `b59f6983c2b224953e8af82c5c582788f962f0b0ed5a19d59f14c73dc023d654` |
| `schemas/fixtures/book-package/invalid/quality_review_without_binding.json` | `6c0d0a7ee97b606f6829fd2cf2873683dfcca20e34075a19e622717c8d1a11b5` |
| `schemas/fixtures/book-package/invalid/quality_review_without_scope.json` | `bca3310d44dd3868ca49ad9311f9fc7dcc7a7081f6292cb9a9d5877ec82505c1` |
| `schemas/fixtures/book-package/invalid/quality_reviewed_without_review.json` | `4c84f3ee0e0191098dd975e3050d8e0ab7cdc6e560a8605ba20588691fc6d6c0` |
| `schemas/fixtures/book-package/invalid/relation_contradicts_one_sided.json` | `0fd003483d12397c41b7b6542933734873ca448f5c3f240392d9250a1228d55b` |
| `schemas/fixtures/book-package/invalid/relation_generated_without_generation.json` | `194f7d4f7dbf7850aadc835845e0399f4d008266e110d1eb9684b28ee7400d48` |
| `schemas/fixtures/book-package/invalid/relation_no_evidence.json` | `00867cc650c38ed46e06a52116785fed4938bf40f0fc892318ace6cee3f615cb` |
| `schemas/fixtures/book-package/invalid/relation_unknown_type.json` | `11eded8510265bbd5d3da9908751b88374a062cc567e4dfa15464181f86e3723` |
| `schemas/fixtures/book-package/valid/anchors/json_pointer.json` | `ea43a06d8401007239f7ce6cf3b6c2bb62ecf04714accfe4af18860f92ef271c` |
| `schemas/fixtures/book-package/valid/anchors/page_bbox.json` | `be3af798ea7d0b15b7f026b0118fc467862d848d4a7e3923769ddc5cc2488347` |
| `schemas/fixtures/book-package/valid/anchors/section_block.json` | `30109684cfa107cec3af006f9e4734a01842cd1bdd7471c01c5e23ec8462b92d` |
| `schemas/fixtures/book-package/valid/anchors/sheet_range.json` | `caf05f20f2f9d311b46fc104222cbda97b1e9a3a748e890fddbfb19ab6bf2d72` |
| `schemas/fixtures/book-package/valid/anchors/slide_block.json` | `6c9d58e7c032673ad811dd74cf370b3812bf94160ed4abf3973835853fb84562` |
| `schemas/fixtures/book-package/valid/anchors/spine_offset.json` | `2b9e959c91c03dbf6b660e6e6f77c476abd90bff7606c985266e4a8bd72aeded` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/assets/fig1.svg` | `ade38c8ba07ffcc0c23ae204abdb1ee3d6aecc2211e7bdeb1c95754eb8795961` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/document.md` | `a4e5a6653be6ec8083c0d7fe007af7a06f9a37e6a14faff6f6a09651fd3f6bdb` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/edits.jsonl` | `14301732dbfb8d3ce6b69dcd4e928c9ef14dbf072b7881315d0f3d6f433c6849` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/manifest.json` | `0065ab80e706e3c469d9db786230512b5a90a3171f11bd89275d27aea630e038` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/objects.jsonl` | `e0fc8c5b9f0c01a7e5f3368d656367223310cf753131046cbbf3e992c49517ca` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/quality.json` | `8008384a4b66b12220652a87eef04786c4ebac05c16a5f312282a2046c5d0b97` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/readable.md` | `5d0cca989f9e1d18e14d214134b7825f0b1e84617f0860011d0edd42a3484d52` |
| `schemas/fixtures/book-package/valid/synthetic-rle-primer/relations.jsonl` | `efec89289184741af9a5580ea865e1cb0866f8a1504539e1155f690932898186` |
| `schemas/fixtures/contract-observation/valid/change-revocation.json` | `671b9b54c95672971b1b8b3397ad9565e16267aa21b94a3da6121fb292537ac6` |
| `schemas/fixtures/contract-observation/valid/observation-pass.json` | `75a3badbbba9cb31c367e66db11a673a734e7235c2756125c554de3a2e19e9ea` |
| `schemas/fixtures/contract-observation/valid/profile-advertisement.json` | `eff71fdf82e156d03c6002fe424db52713038803e387c3133b8e89ca08897cb3` |
| `tools/book_package_fixture.py` | `e15ecf8ec799f17b2fcc1f2a5d04669adc91f5e1c5d7a3f62de598a134490227` |
| `tools/build_book_package.py` | `f172a2c3de6c84f539350d69cfff6aa3ddf843fbb8dde65c4ce70c317e0c2b44` |
| `tools/check_book_package.py` | `290ed9251ff923aeb21dc42e6e67297d054e5a3ddf5957beea1cb8221f5b813f` |
| `tools/check_contract_profile.py` | `33ed0d1e0d0b8cae9db87ba6329a1c2c1b96114af918bc2de19ebeb99e7e71ea` |
| `tools/check_requirement_register.py` | `620dd7d42d19f05d1a9dab841f91a4e3df408b8fd033d38637667e043735db48` |
| `tools/test_book_package.py` | `e832d225fe15f39abb68e29ee1ff789b27ea1cee4a5321756f78b19101af4322` |
| `tools/test_book_package_review.py` | `9c8c9f5f952136dfd10e5f30b3f20583336cc7f9ac3851f45548840f699f43ec` |
| `tools/test_build_book_package.py` | `c5c52ca5ecac4714fa3ad42d05d6b4beb85c1f22a98d93718884e752ae158790` |
| `tools/test_contract_profile.py` | `943f8e57b3bfe248f13425fcf3cd3ef93b52d940eecf3d6014f8b57846c256d6` |
| `tools/test_index_release_receipt.py` | `51bb27d11ff1aa9b6cde1e99a99514e579d4a6e49a5617cb36f2bdc3220b7f49` |

## Companion evidence

| File | SHA256 |
| --- | --- |
| `independent-engineering-review-reproduce.py` | `b57e32e32e9863adea9cf0d22b3f255d8074fb0fe67cc0bfcb74477d40765a6e` |
| `independent-engineering-probes.json` | `aa80dc974606d330d4e16d041796248a28866fc3efb8b506431e709be7745ae1` |
| `independent-engineering-probe-correction.json` | `bf9c3952e0113ed89be1abac932dd596204b6a2ebbae46b7cb31284dfc6b117b` |
| `independent-engineering-requirement-refs.json` | `9ae49aa6c4a5cac01b8121a5bf42f9d7c5d4406dd2bcac4832d620c25cc60123` |

## Reviewer actions

Read repository and tests; wrote only independent local review/probe artifacts outside repository. No source edits, commits, external messages or uploads.

Final traceability refresh: BPK-R005 now cites the persistent directory-symlink regression. Requirements remain 283; distinct resolved method references increased from 17 in C06 to 18 in C10. This changed only the register mapping and generated register, both rehashed in the final inventory.
