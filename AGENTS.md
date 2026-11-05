# Working on Knowledge Contract

## Canonical reading structure

Read [README.md](README.md) and [publication-catalog.json](publication-catalog.json) first. Scientific arguments are in `papers/<topic>/PAPER.md`; normative requirements are in `engineering/specifications/<topic>/SPECIFICATION.md`; actual evaluations are in `engineering/studies/<topic>/STUDY.md`. Shared terms and primary references are in `reference/`; supporting migration and API material is in `appendices/`.

The old numerical paper paths and `spec/` files are compatibility links. Their full previous contents are preserved at the pinned historical commit in the source map. Add or revise the canonical document, not a second competing copy.

## Artifact and terminology conventions

Follow [the artifact registry](engineering/specifications/artifact-registry/SPECIFICATION.md). Use meaningful unique lowercase hyphenated directory names and the main filename defined for the type. New publication documents require the catalogue entry and standard front matter. For installed skills follow the external Agent Skills format; do not impose publication metadata as unsupported required skill fields.

A role is a responsibility. A skill is a reusable method. A competency specifies or assesses ability under conditions. A blueprint is a solution structure. A constraint restricts admissible use or action and must be linked explicitly. A skill file is not evidence of capability or a grant. Use **Work Item** in prose and `WorkItem` only for the same entity's literal code identifier.

## Claims and evidence

Keep proofs, finite tests, illustrative examples, practical outcomes and causal claims distinct. Bind claims to exact records through `engineering/studies/evidence-index.json`. Preserve negative results, comparator ties, trust assumptions and unresolved observations. Never change a retained raw report to improve its appearance. Explain whether an evidence file is exact original JSON, a reconstructed prose view, a metadata extraction, or a new public example.

Scientific papers must be readable without private artifact identifiers, missing-release markers, operational iteration histories or domain walkthroughs. Put practical cases in engineering studies and link them. Keep protocol compatibility details in the engineering appendix. A completed document edition does not upgrade a runtime protocol or prove empirical superiority.

## Verification commands

Use Python 3 and Pandoc 3.1.3. Run relevant existing checks and the publication gate:

```sh
python3 -B tools/check_publication.py .
python3 -B tools/check_sources.py .
python3 -B tools/check_requirement_register.py
python3 -B -m unittest tools.test_check_publication tools.test_check_sources tools.test_check_separation tools.test_check_dco tools.test_ci_workflow -v
```

When changing the book-package schema, validator or exchange subset, run `cd tools && python3 -B -m unittest test_book_package test_build_book_package test_book_package_review test_contract_profile test_index_release_receipt -v` using the CI dependency `jsonschema==4.23.0`, validate the synthetic package, and check regenerated fixtures against their committed bytes. The `book-package/2` profile uses explicit version-2 record tags; a version-1 package needs a declared migration and new observations, not a metadata-only upgrade.

Run the formal regression controls with `python3 -B -m unittest tools.test_reviewed_formal_results -v`. They check finite counterexamples and models; they do not replace the papers' proofs or historical model experiments.

Preserve existing requirement identifiers when editing a specification or the API appendix. `tools/check_requirement_register.py --assign --update` assigns identifiers only to new normative clauses and regenerates the register; review that change before committing. A listed regression test is a bounded check, not proof that a complete implementation conforms. The default command detects stale or missing register entries without editing files.

The four edition-1.0 public replay scripts remain unchanged under the studies' `evidence/` directories. Their historical limitations remain explicit. The corrected checks are:

```sh
python3 -B engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py
python3 -B engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py
python3 -B engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py
```

These programs use Python's standard library. Run relevant old and corrected programs when their inputs or claims change. Retained evidence and origin manifests must not be rewritten to improve a result; a corrected check gets its own identified file and scope. Do not pretend that a new synthetic example reruns a historical model experiment. See [the current review record](reviews/edition-corrections/REVIEW.md) for exact correction dispositions and any missing historical inputs.

## Publication boundaries

Preserve the existing separation between content changes, publication decisions and corpus allowlist changes. The catalogue organizes reading; it does not authorize indexing. Existing corpus receipts certify their original bytes only. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for review, attribution and DCO. Do not manufacture a human sign-off or a review receipt.

The site is built in the separate `contract-place-site` repository from an exact source commit. A backend index refresh and a deployment require their own actual readback. Record what was built or checked locally separately from what was merged or deployed.
