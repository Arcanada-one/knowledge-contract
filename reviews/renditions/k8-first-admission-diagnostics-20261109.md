---
title: "K8 first rendition admission diagnostics (2026-11-09)"
sources: none
status: "diagnostic only; iteration-2 import recorded; native compile still refused on link depth; draft PR evidence for KC-Brain"
updated: 2026-11-09
---

# K8 first rendition admission diagnostics

## Iteration 1 (2026-11-09) — initial eight-entry admission

## Scope

Draft PR: [Arcanada-one/knowledge-contract#86](https://github.com/Arcanada-one/knowledge-contract/pull/86)
Branch head at report authorship: `1b321d553c25fb0552a970e8861ae1cd09580c2c` (sidecar admission tip was `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`).
Site compiler: `contract-place-site` `main` in a separate local checkout.
No rendition bytes were modified after admission. No compiler remapping of old-commit GitHub blob URLs was applied.

Pre-write verification for all eight admission-list rows: current EN blob on `main` matched the listed blob; rendition blob at PR76 head `4ce30f167b32b9b811b269a3cfa0a22ec2080359` matched the listed blob; EN bytes from `## Abstract` through EOF matched the earlier EN at `a0450428704fcd41b411203f2fc88c06c779610b`.

## Outcome

`scripts/build_publication.py` against the admission tip **refuses** the sidecar. No entry reaches a published `reviewed` page state. Review objects in the sidecar would bind to `reviewed` under `resolve_state` (independent Agent-Brain review bound to current EN + rendition blobs with `coverage: full`), but structural parity fails first.

knowledge-contract required checks on the draft PR were green for the admission tip (DCO, publication-integrity, licensing, and the other required jobs). Those checks do not run the site rendition compiler. This diagnostic file is added so KC-Brain can repair content against exact compiler refusals.

## Ownership split

- **KC-Brain / translator content (must change rendition bytes + re-review):** absolute `https://github.com/.../blob/a0450428.../` links instead of English-relative targets; missing EN historic-anchor preamble (`<!-- markdownlint-disable-next-line MD033 -->` + `<a id="..."></a>`) on two studies; front-matter `source_commit` / `source_git_blob` / `translation_status: author-draft` still naming the earlier source identity.
- **KC-SWE sidecar values already set on this branch (not the compile blockers above):** `publication-renditions.json` schema v2 entries, catalogue key, section maps from pandoc anchors, review evidence path/blob, source/rendition pin revisions and sha256 digests. Sidecar pin ancestry verifies cleanly against the admission tip; the dry-run `RENDITION_REVISION_PIN` rows are an artifact of dry-run using the publication HEAD as `source.revision` while the rendition file commit is earlier.

## Summary table

| Work | Language | Source blob | Rendition blob | Source sha256 | Rendition sha256 | resolve_state (review bind) | First compile failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dependency-closure-and-package-delivery` | `ru` | `42294151076e662129a8716ea13a29dc2f967ec9` | `5aa9ee44986a68c0e47d99c801ec11a2fe1ddd9e` | `5edb3262dc193a32fd2a577d8a887e939d80e9386e36afc542514446dd2672ce` | `8d4ff8363466f9eb1f63332052cf5f6ebcdda210eb3f04396ea582e1ce54d76e` | `reviewed` | `RENDITION_REFERENCE_DROPPED` |
| `dependency-closure-and-package-delivery` | `zh-Hans` | `42294151076e662129a8716ea13a29dc2f967ec9` | `6d78e14dd29bbe751e5d7699a8ff76383395dc62` | `5edb3262dc193a32fd2a577d8a887e939d80e9386e36afc542514446dd2672ce` | `bc595b4c88f71f388a3ebfc0307a59b869bcd2c7caf0b560e5dd0ce56945bc42` | `reviewed` | `RENDITION_REFERENCE_DROPPED` |
| `source-transcription-and-uncertainty` | `ru` | `8ca885fc3f144d89e95e4813868fd953450f1f71` | `4a8e7b8d986c3eb846cb6ea381dcc1b0685755d1` | `3278cca0cdbb752dc70b73809c5218019584e0a0e832f4e170c339c7d327710a` | `66cb5efc16efcbe36e028b8c34346e6536125d6ee34268716a1ffb43e6c863ac` | `reviewed` | `RENDITION_SECTION_MISSING` |
| `source-transcription-and-uncertainty` | `zh-Hans` | `8ca885fc3f144d89e95e4813868fd953450f1f71` | `1be23f4f57ae705870149cc61964c3bb2c1d3784` | `3278cca0cdbb752dc70b73809c5218019584e0a0e832f4e170c339c7d327710a` | `32fbb5eceff4bdaca7088d6a518f04b44c5d092866262299199529cd00f4be0f` | `reviewed` | `RENDITION_SECTION_MISSING` |
| `executable-projections-and-revision` | `ru` | `b2306980ba150d0a0841896b6123df5ff72fc319` | `f9361172e1fe559e90aac4be615f19474dc7a941` | `77a4bcd95428f40ab0faa33fcda50ebb6c85ed10efa738ed30bb05fc66197255` | `f575edd55379c02f0d44cd1942aabfe036c8509084b1bde6b52e7858666143c8` | `reviewed` | `RENDITION_REFERENCE_DROPPED` |
| `executable-projections-and-revision` | `zh-Hans` | `b2306980ba150d0a0841896b6123df5ff72fc319` | `346d23b860650abbebfe55e3f7d9f90e85dcedd2` | `77a4bcd95428f40ab0faa33fcda50ebb6c85ed10efa738ed30bb05fc66197255` | `b62759e482c6134cab1f69137df1d2e63ea84010aa9156da25d8d00790629f94` | `reviewed` | `RENDITION_REFERENCE_DROPPED` |
| `reuse-admission-and-cost-controls` | `ru` | `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac` | `90bca419fac0c0834fe4bce4513772812958bbec` | `dc4bba37e36d4b6825131f4c8a9fca4bdf398e27c024e094a29cf66a21d80e13` | `a82156801e051e597a78c0fd83ee0487f846f39a529b413a0a271f5d14705f9a` | `reviewed` | `RENDITION_SECTION_MISSING` |
| `reuse-admission-and-cost-controls` | `zh-Hans` | `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac` | `1c3cbeff2939888d2a95414ec3315b2671cb46f0` | `dc4bba37e36d4b6825131f4c8a9fca4bdf398e27c024e094a29cf66a21d80e13` | `f630c56a85092972232199cf259b0e7f27241ad257f05fc54aba2238e122bfc7` | `reviewed` | `RENDITION_SECTION_MISSING` |

## Per-entry diagnostics

### `dependency-closure-and-package-delivery / ru`

- Rendition path: `translations/ru/engineering/studies/dependency-closure-and-package-delivery/STUDY.md`
- Sidecar source.revision: `e17d33711210331b1ab1377a92d728e58eb93c02`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=63078110074e82b47f76a8f132a3cfdcbfb555b1`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `dependency-closure-and-package-delivery / ru`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#editorial-input` | line 25: `../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` |
| 28 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md` | line 27: `../../../papers/retrieval-and-context-composition/PAPER.md` |
| 28 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md` | line 27: `../../../papers/constrained-transformations/PAPER.md` |
| 28 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md` | line 27: `../../../papers/revision-and-governance/PAPER.md` |
| 52 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json` | line 51: `evidence/finite-package-selftest.json` |
| 54 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md#counting-and-interpretation` | line 53: `../README.md#counting-and-interpretation` |
| 60 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json` | line 59: `evidence/dependency-graph.json` |
| 60 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py` | line 59: `evidence/replay_closure.py` |
| 68 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json` | line 67: `evidence/public-closure-replay.json` |
| 72 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | line 71: `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` |
| 74 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py` | line 73: `checks/check_closure_size_and_mutations.py` |
| 74 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json` | line 73: `checks/closure-size-and-mutation-check.json` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json` | line 95: `evidence/layout-preservation-report.json` |
| 98 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json` | line 97: `evidence/layout-conformance-report.json` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json` | line 103: `evidence/historical-package-replay.json` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json` | line 103: `evidence/historical-replay-environment.json` |
| 122 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md` | line 121: `../editorial-skill-pilot/STUDY.md` |
| 122 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 121: `../../../reference/glossary/GLOSSARY.md` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json` | line 123: `evidence/origin.json` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 123: `../evidence-language-index.json` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json` | line 123: `../review-corrections.json` |

#### Section / structure codes — `dependency-closure-and-package-delivery / ru`

- No `RENDITION_SECTION_*` raised for this entry under the real sidecar (heading counts and mapped h2/h3 anchors align).

#### Reference / other RENDITION codes — `dependency-closure-and-package-delivery / ru`

- `RENDITION_REFERENCE_DROPPED`: RENDITION_REFERENCE_DROPPED: dependency-closure-and-package-delivery/ru: references or footnotes of the source are missing: ["('Link', 'engineering/studies/README.md#counting-and-interpretation')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json')"], footnotes 0 -> 0
- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/studies/README.md#counting-and-interpretation') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py') x1`
  - `('Link', 'engineering/studies/editorial-skill-pilot/STUDY.md') x1`
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/review-corrections.json') x1`
  - `('Link', 'papers/constrained-transformations/PAPER.md') x1`
  - `('Link', 'papers/retrieval-and-context-composition/PAPER.md') x1`
  - `('Link', 'papers/revision-and-governance/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#editorial-input') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=21
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md#counting-and-interpretation') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json') x1`
  - … and 16 more

#### RENDITION_REVISION_PIN — `dependency-closure-and-package-delivery / ru`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_REFERENCE_DROPPED`/parity, `RENDITION_REVISION_PIN`/pins

### `dependency-closure-and-package-delivery / zh-Hans`

- Rendition path: `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/STUDY.md`
- Sidecar source.revision: `e17d33711210331b1ab1377a92d728e58eb93c02`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=63078110074e82b47f76a8f132a3cfdcbfb555b1`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `dependency-closure-and-package-delivery / zh-Hans`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#editorial-input` | line 25: `../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` |
| 28 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md` | line 27: `../../../papers/retrieval-and-context-composition/PAPER.md` |
| 28 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md` | line 27: `../../../papers/constrained-transformations/PAPER.md` |
| 28 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md` | line 27: `../../../papers/revision-and-governance/PAPER.md` |
| 52 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json` | line 51: `evidence/finite-package-selftest.json` |
| 54 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md#counting-and-interpretation` | line 53: `../README.md#counting-and-interpretation` |
| 60 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json` | line 59: `evidence/dependency-graph.json` |
| 60 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py` | line 59: `evidence/replay_closure.py` |
| 68 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json` | line 67: `evidence/public-closure-replay.json` |
| 72 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | line 71: `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` |
| 74 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py` | line 73: `checks/check_closure_size_and_mutations.py` |
| 74 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json` | line 73: `checks/closure-size-and-mutation-check.json` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json` | line 95: `evidence/layout-preservation-report.json` |
| 98 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json` | line 97: `evidence/layout-conformance-report.json` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json` | line 103: `evidence/historical-package-replay.json` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json` | line 103: `evidence/historical-replay-environment.json` |
| 122 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md` | line 121: `../editorial-skill-pilot/STUDY.md` |
| 122 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 121: `../../../reference/glossary/GLOSSARY.md` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json` | line 123: `evidence/origin.json` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 123: `../evidence-language-index.json` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json` | line 123: `../review-corrections.json` |

#### Section / structure codes — `dependency-closure-and-package-delivery / zh-Hans`

- No `RENDITION_SECTION_*` raised for this entry under the real sidecar (heading counts and mapped h2/h3 anchors align).

#### Reference / other RENDITION codes — `dependency-closure-and-package-delivery / zh-Hans`

- `RENDITION_REFERENCE_DROPPED`: RENDITION_REFERENCE_DROPPED: dependency-closure-and-package-delivery/zh-Hans: references or footnotes of the source are missing: ["('Link', 'engineering/studies/README.md#counting-and-interpretation')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json')", "('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json')"], footnotes 0 -> 0
- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/studies/README.md#counting-and-interpretation') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json') x1`
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py') x1`
  - `('Link', 'engineering/studies/editorial-skill-pilot/STUDY.md') x1`
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/review-corrections.json') x1`
  - `('Link', 'papers/constrained-transformations/PAPER.md') x1`
  - `('Link', 'papers/retrieval-and-context-composition/PAPER.md') x1`
  - `('Link', 'papers/revision-and-governance/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#editorial-input') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=21
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md#counting-and-interpretation') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json') x1`
  - … and 16 more

#### RENDITION_REVISION_PIN — `dependency-closure-and-package-delivery / zh-Hans`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_REFERENCE_DROPPED`/parity, `RENDITION_REVISION_PIN`/pins

### `source-transcription-and-uncertainty / ru`

- Rendition path: `translations/ru/engineering/studies/source-transcription-and-uncertainty/STUDY.md`
- Sidecar source.revision: `548abd01d089faf81570efaafd41ef873c693e47`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=5f19fc3d33fa0e185c34056188ce7746742bee87`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `source-transcription-and-uncertainty / ru`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md` | line 28: `../../../papers/semantic-objects-and-context/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md` | line 28: `../../../papers/constrained-transformations/PAPER.md` |
| 37 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/structural-corpus-report.json` | line 39: `evidence/structural-corpus-report.json` |
| 43 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json` | line 45: `evidence/corpus-audit-source.json` |
| 57 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/uncertainty-projection-source.json` | line 59: `evidence/uncertainty-projection-source.json` |
| 72 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md` | line 74: `../executable-projections-and-revision/STUDY.md` |
| 82 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/local-export-integration-report.json` | line 84: `evidence/local-export-integration-report.json` |
| 88 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/origin.json` | line 90: `evidence/origin.json` |
| 90 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py` | line 92: `checks/demonstrate_uncertainty_projection.py` |
| 90 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/synthetic-base.txt` | line 92: `checks/synthetic-base.txt` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/uncertainty-projection-check.json` | line 98: `checks/uncertainty-projection-check.json` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/replay_uncertainty_projection.py` | line 98: `evidence/replay_uncertainty_projection.py` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/public-projection-demonstration.json` | line 98: `evidence/public-projection-demonstration.json` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json` | line 98: `../review-corrections.json` |
| 98 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 100: `../evidence-language-index.json` |
| 102 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | line 104: `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | line 106: `../executable-projections-and-revision/evidence/addressability-study-source.json` |
| 106 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 108: `../../../reference/glossary/GLOSSARY.md` |

#### Section / structure codes — `source-transcription-and-uncertainty / ru`

- `RENDITION_SECTION_MISSING`: RENDITION_SECTION_MISSING: source-transcription-and-uncertainty/ru: section (preamble) has text in the source but none in the rendition
- Cause: English has a preamble historic-anchor block (`<!-- markdownlint-disable-next-line MD033 -->` plus `<a id="…legacy-anchor…"></a>` before the H1). The rendition places the legacy id on the H1 via `{#…}` and has an empty preamble, so parity reports preamble text in the source and none in the rendition.
- Source anchors in the sidecar map (h2/h3 only; preamble is implicit): `abstract`, `question-and-source-scope`, `audit-and-transformation-method`, `preserving-uncertainty-as-a-testable-obligation`, `domain-specific-consequences`, `trace-defects-and-later-integration`, `public-illustration-and-retained-evidence`, `limits-and-conclusion`

#### Reference / other RENDITION codes — `source-transcription-and-uncertainty / ru`

- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/STUDY.md') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'engineering/studies/review-corrections.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/checks/synthetic-base.txt') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/checks/uncertainty-projection-check.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/local-export-integration-report.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/public-projection-demonstration.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/replay_uncertainty_projection.py') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/structural-corpus-report.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/uncertainty-projection-source.json') x1`
  - `('Link', 'papers/constrained-transformations/PAPER.md') x1`
  - `('Link', 'papers/semantic-objects-and-context/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=18
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py') x1`
  - … and 13 more

#### RENDITION_REVISION_PIN — `source-transcription-and-uncertainty / ru`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_SECTION_MISSING`/parity, `RENDITION_REVISION_PIN`/pins

### `source-transcription-and-uncertainty / zh-Hans`

- Rendition path: `translations/zh-Hans/engineering/studies/source-transcription-and-uncertainty/STUDY.md`
- Sidecar source.revision: `548abd01d089faf81570efaafd41ef873c693e47`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=5f19fc3d33fa0e185c34056188ce7746742bee87`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `source-transcription-and-uncertainty / zh-Hans`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md` | line 28: `../../../papers/semantic-objects-and-context/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md` | line 28: `../../../papers/constrained-transformations/PAPER.md` |
| 37 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/structural-corpus-report.json` | line 39: `evidence/structural-corpus-report.json` |
| 43 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json` | line 45: `evidence/corpus-audit-source.json` |
| 57 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/uncertainty-projection-source.json` | line 59: `evidence/uncertainty-projection-source.json` |
| 72 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md` | line 74: `../executable-projections-and-revision/STUDY.md` |
| 82 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/local-export-integration-report.json` | line 84: `evidence/local-export-integration-report.json` |
| 88 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/origin.json` | line 90: `evidence/origin.json` |
| 90 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py` | line 92: `checks/demonstrate_uncertainty_projection.py` |
| 90 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/synthetic-base.txt` | line 92: `checks/synthetic-base.txt` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/uncertainty-projection-check.json` | line 98: `checks/uncertainty-projection-check.json` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/replay_uncertainty_projection.py` | line 98: `evidence/replay_uncertainty_projection.py` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/public-projection-demonstration.json` | line 98: `evidence/public-projection-demonstration.json` |
| 96 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json` | line 98: `../review-corrections.json` |
| 98 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 100: `../evidence-language-index.json` |
| 102 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | line 104: `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | line 106: `../executable-projections-and-revision/evidence/addressability-study-source.json` |
| 106 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 108: `../../../reference/glossary/GLOSSARY.md` |

#### Section / structure codes — `source-transcription-and-uncertainty / zh-Hans`

- `RENDITION_SECTION_MISSING`: RENDITION_SECTION_MISSING: source-transcription-and-uncertainty/zh-Hans: section (preamble) has text in the source but none in the rendition
- Cause: English has a preamble historic-anchor block (`<!-- markdownlint-disable-next-line MD033 -->` plus `<a id="…legacy-anchor…"></a>` before the H1). The rendition places the legacy id on the H1 via `{#…}` and has an empty preamble, so parity reports preamble text in the source and none in the rendition.
- Source anchors in the sidecar map (h2/h3 only; preamble is implicit): `abstract`, `question-and-source-scope`, `audit-and-transformation-method`, `preserving-uncertainty-as-a-testable-obligation`, `domain-specific-consequences`, `trace-defects-and-later-integration`, `public-illustration-and-retained-evidence`, `limits-and-conclusion`

#### Reference / other RENDITION codes — `source-transcription-and-uncertainty / zh-Hans`

- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/STUDY.md') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'engineering/studies/review-corrections.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/checks/synthetic-base.txt') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/checks/uncertainty-projection-check.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/local-export-integration-report.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/public-projection-demonstration.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/replay_uncertainty_projection.py') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/structural-corpus-report.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/uncertainty-projection-source.json') x1`
  - `('Link', 'papers/constrained-transformations/PAPER.md') x1`
  - `('Link', 'papers/semantic-objects-and-context/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=18
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py') x1`
  - … and 13 more

#### RENDITION_REVISION_PIN — `source-transcription-and-uncertainty / zh-Hans`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_SECTION_MISSING`/parity, `RENDITION_REVISION_PIN`/pins

### `executable-projections-and-revision / ru`

- Rendition path: `translations/ru/engineering/studies/executable-projections-and-revision/STUDY.md`
- Sidecar source.revision: `e17d33711210331b1ab1377a92d728e58eb93c02`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=2d247a01d4dbd6a1d1491d2b54464336c6fef190`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `executable-projections-and-revision / ru`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md` | line 25: `../../../papers/retrieval-and-context-composition/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md` | line 25: `../../../papers/revision-and-governance/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/evidence-and-falsification/PAPER.md` | line 25: `../../../papers/evidence-and-falsification/PAPER.md` |
| 32 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json` | line 31: `evidence/historical-reader-study-source.json` |
| 34 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | line 33: `../source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` |
| 53 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json` | line 52: `evidence/reader-boundary-report.json` |
| 57 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json` | line 56: `evidence/targeted-revision-comparison.json` |
| 74 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | line 73: `evidence/addressability-study-source.json` |
| 88 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json` | line 87: `evidence/consumer-qualification-report.json` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json` | line 103: `evidence/agent-projection-results.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/origin.json` | line 115: `evidence/origin.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json` | line 115: `evidence/offline-projection-replay-report.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/historical-recovery-gaps.json` | line 117: `../historical-recovery-gaps.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md` | line 117: `../dependency-closure-and-package-delivery/STUDY.md` |
| 120 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json` | line 119: `evidence/projection-study-source.json` |
| 120 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 119: `../evidence-language-index.json` |
| 120 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | line 119: `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 123: `../../../reference/glossary/GLOSSARY.md` |

#### Section / structure codes — `executable-projections-and-revision / ru`

- No `RENDITION_SECTION_*` raised for this entry under the real sidecar (heading counts and mapped h2/h3 anchors align).

#### Reference / other RENDITION codes — `executable-projections-and-revision / ru`

- `RENDITION_REFERENCE_DROPPED`: RENDITION_REFERENCE_DROPPED: executable-projections-and-revision/ru: references or footnotes of the source are missing: ["('Link', 'engineering/studies/dependency-closure-and-package-delivery/STUDY.md')", "('Link', 'engineering/studies/evidence-language-index.json')", "('Link', 'engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json')", "('Link', 'engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json')", "('Link', 'engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json')"], footnotes 0 -> 0
- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/STUDY.md') x1`
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json') x1`
  - `('Link', 'engineering/studies/historical-recovery-gaps.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json') x1`
  - `('Link', 'papers/evidence-and-falsification/PAPER.md') x1`
  - `('Link', 'papers/retrieval-and-context-composition/PAPER.md') x1`
  - `('Link', 'papers/revision-and-governance/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=18
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json') x1`
  - … and 13 more

#### RENDITION_REVISION_PIN — `executable-projections-and-revision / ru`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_REFERENCE_DROPPED`/parity, `RENDITION_REVISION_PIN`/pins

### `executable-projections-and-revision / zh-Hans`

- Rendition path: `translations/zh-Hans/engineering/studies/executable-projections-and-revision/STUDY.md`
- Sidecar source.revision: `e17d33711210331b1ab1377a92d728e58eb93c02`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=2d247a01d4dbd6a1d1491d2b54464336c6fef190`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `executable-projections-and-revision / zh-Hans`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md` | line 25: `../../../papers/retrieval-and-context-composition/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md` | line 25: `../../../papers/revision-and-governance/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/evidence-and-falsification/PAPER.md` | line 25: `../../../papers/evidence-and-falsification/PAPER.md` |
| 32 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json` | line 31: `evidence/historical-reader-study-source.json` |
| 34 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | line 33: `../source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` |
| 53 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json` | line 52: `evidence/reader-boundary-report.json` |
| 57 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json` | line 56: `evidence/targeted-revision-comparison.json` |
| 74 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | line 73: `evidence/addressability-study-source.json` |
| 88 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json` | line 87: `evidence/consumer-qualification-report.json` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json` | line 103: `evidence/agent-projection-results.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/origin.json` | line 115: `evidence/origin.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json` | line 115: `evidence/offline-projection-replay-report.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/historical-recovery-gaps.json` | line 117: `../historical-recovery-gaps.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md` | line 117: `../dependency-closure-and-package-delivery/STUDY.md` |
| 120 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json` | line 119: `evidence/projection-study-source.json` |
| 120 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 119: `../evidence-language-index.json` |
| 120 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | line 119: `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` |
| 124 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 123: `../../../reference/glossary/GLOSSARY.md` |

#### Section / structure codes — `executable-projections-and-revision / zh-Hans`

- No `RENDITION_SECTION_*` raised for this entry under the real sidecar (heading counts and mapped h2/h3 anchors align).

#### Reference / other RENDITION codes — `executable-projections-and-revision / zh-Hans`

- `RENDITION_REFERENCE_DROPPED`: RENDITION_REFERENCE_DROPPED: executable-projections-and-revision/zh-Hans: references or footnotes of the source are missing: ["('Link', 'engineering/studies/dependency-closure-and-package-delivery/STUDY.md')", "('Link', 'engineering/studies/evidence-language-index.json')", "('Link', 'engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json')", "('Link', 'engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json')", "('Link', 'engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json')"], footnotes 0 -> 0
- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/studies/dependency-closure-and-package-delivery/STUDY.md') x1`
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json') x1`
  - `('Link', 'engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json') x1`
  - `('Link', 'engineering/studies/historical-recovery-gaps.json') x1`
  - `('Link', 'engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json') x1`
  - `('Link', 'papers/evidence-and-falsification/PAPER.md') x1`
  - `('Link', 'papers/retrieval-and-context-composition/PAPER.md') x1`
  - `('Link', 'papers/revision-and-governance/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=18
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json') x1`
  - … and 13 more

#### RENDITION_REVISION_PIN — `executable-projections-and-revision / zh-Hans`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_REFERENCE_DROPPED`/parity, `RENDITION_REVISION_PIN`/pins

### `reuse-admission-and-cost-controls / ru`

- Rendition path: `translations/ru/engineering/studies/reuse-admission-and-cost-controls/STUDY.md`
- Sidecar source.revision: `548abd01d089faf81570efaafd41ef873c693e47`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=67ab4b55faf9f42df2d6d7214bbbe4f30c143a8e`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `reuse-admission-and-cost-controls / ru`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md` | line 28: `../../../papers/controlled-knowledge-reuse/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/knowledge-utility/PAPER.md` | line 28: `../../../papers/knowledge-utility/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/reuse-properties-source.json` | line 28: `evidence/reuse-properties-source.json` |
| 40 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md` | line 42: `../../specifications/status-model/SPECIFICATION.md` |
| 57 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md` | line 59: `../../../papers/controlled-knowledge-reuse/PAPER.md` |
| 65 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#http-caching` | line 67: `../../../reference/bibliography/BIBLIOGRAPHY.md#http-caching` |
| 65 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses` | line 67: `../../../reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md` | line 106: `../editorial-skill-pilot/STUDY.md` |
| 108 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py` | line 110: `checks/check_admission_and_cost.py` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json` | line 116: `checks/admission-and-cost-check.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/replay_reuse_counterexamples.py` | line 116: `evidence/replay_reuse_counterexamples.py` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/public-reuse-counterexamples.json` | line 116: `evidence/public-reuse-counterexamples.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json` | line 116: `../review-corrections.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/origin.json` | line 118: `evidence/origin.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 118: `../evidence-language-index.json` |
| 122 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 122: `../../../reference/glossary/GLOSSARY.md` |

#### Section / structure codes — `reuse-admission-and-cost-controls / ru`

- `RENDITION_SECTION_MISSING`: RENDITION_SECTION_MISSING: reuse-admission-and-cost-controls/ru: section (preamble) has text in the source but none in the rendition
- Cause: English has a preamble historic-anchor block (`<!-- markdownlint-disable-next-line MD033 -->` plus `<a id="…legacy-anchor…"></a>` before the H1). The rendition places the legacy id on the H1 via `{#…}` and has an empty preamble, so parity reports preamble text in the source and none in the rendition.
- Source anchors in the sidecar map (h2/h3 only; preamble is implicit): `abstract`, `question-and-objects`, `admission-before-optimization`, `counterexamples-that-determine-the-design`, `time-concurrency-and-state`, `an-exact-cost-model`, `utility-and-double-counting`, `public-examples-and-claim-limits`, `conclusion`

#### Reference / other RENDITION codes — `reuse-admission-and-cost-controls / ru`

- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/specifications/status-model/SPECIFICATION.md') x1`
  - `('Link', 'engineering/studies/editorial-skill-pilot/STUDY.md') x1`
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/public-reuse-counterexamples.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/replay_reuse_counterexamples.py') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/reuse-properties-source.json') x1`
  - `('Link', 'engineering/studies/review-corrections.json') x1`
  - `('Link', 'papers/controlled-knowledge-reuse/PAPER.md') x2`
  - `('Link', 'papers/knowledge-utility/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#http-caching') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=15
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py') x1`
  - … and 10 more

#### RENDITION_REVISION_PIN — `reuse-admission-and-cost-controls / ru`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_SECTION_MISSING`/parity, `RENDITION_REVISION_PIN`/pins

### `reuse-admission-and-cost-controls / zh-Hans`

- Rendition path: `translations/zh-Hans/engineering/studies/reuse-admission-and-cost-controls/STUDY.md`
- Sidecar source.revision: `548abd01d089faf81570efaafd41ef873c693e47`
- Sidecar rendition.revision: `8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`
- Front matter: `source_commit=a0450428704fcd41b411203f2fc88c06c779610b`, `source_git_blob=67ab4b55faf9f42df2d6d7214bbbe4f30c143a8e`, `translation_status=author-draft`, `author=Pavel Valentov`
- `resolve_state`: `reviewed`

#### Absolute GitHub blob URLs — `reuse-admission-and-cost-controls / zh-Hans`

| Line | Rendition URL | English counterpart at same link index (or note) |
| ---: | --- | --- |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md` | line 28: `../../../papers/controlled-knowledge-reuse/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/knowledge-utility/PAPER.md` | line 28: `../../../papers/knowledge-utility/PAPER.md` |
| 26 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/reuse-properties-source.json` | line 28: `evidence/reuse-properties-source.json` |
| 40 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md` | line 42: `../../specifications/status-model/SPECIFICATION.md` |
| 57 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md` | line 59: `../../../papers/controlled-knowledge-reuse/PAPER.md` |
| 65 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#http-caching` | line 67: `../../../reference/bibliography/BIBLIOGRAPHY.md#http-caching` |
| 65 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses` | line 67: `../../../reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses` |
| 104 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md` | line 106: `../editorial-skill-pilot/STUDY.md` |
| 108 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py` | line 110: `checks/check_admission_and_cost.py` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json` | line 116: `checks/admission-and-cost-check.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/replay_reuse_counterexamples.py` | line 116: `evidence/replay_reuse_counterexamples.py` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/public-reuse-counterexamples.json` | line 116: `evidence/public-reuse-counterexamples.json` |
| 116 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json` | line 116: `../review-corrections.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/origin.json` | line 118: `evidence/origin.json` |
| 118 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json` | line 118: `../evidence-language-index.json` |
| 122 | `https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md` | line 122: `../../../reference/glossary/GLOSSARY.md` |

#### Section / structure codes — `reuse-admission-and-cost-controls / zh-Hans`

- `RENDITION_SECTION_MISSING`: RENDITION_SECTION_MISSING: reuse-admission-and-cost-controls/zh-Hans: section (preamble) has text in the source but none in the rendition
- Cause: English has a preamble historic-anchor block (`<!-- markdownlint-disable-next-line MD033 -->` plus `<a id="…legacy-anchor…"></a>` before the H1). The rendition places the legacy id on the H1 via `{#…}` and has an empty preamble, so parity reports preamble text in the source and none in the rendition.
- Source anchors in the sidecar map (h2/h3 only; preamble is implicit): `abstract`, `question-and-objects`, `admission-before-optimization`, `counterexamples-that-determine-the-design`, `time-concurrency-and-state`, `an-exact-cost-model`, `utility-and-double-counting`, `public-examples-and-claim-limits`, `conclusion`

#### Reference / other RENDITION codes — `reuse-admission-and-cost-controls / zh-Hans`

- Full missing reference multiset (English relative identity absent on the rendition side because links were rewritten to absolute GitHub blob URLs):
  - `('Link', 'engineering/specifications/status-model/SPECIFICATION.md') x1`
  - `('Link', 'engineering/studies/editorial-skill-pilot/STUDY.md') x1`
  - `('Link', 'engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/origin.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/public-reuse-counterexamples.json') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/replay_reuse_counterexamples.py') x1`
  - `('Link', 'engineering/studies/reuse-admission-and-cost-controls/evidence/reuse-properties-source.json') x1`
  - `('Link', 'engineering/studies/review-corrections.json') x1`
  - `('Link', 'papers/controlled-knowledge-reuse/PAPER.md') x2`
  - `('Link', 'papers/knowledge-utility/PAPER.md') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#http-caching') x1`
  - `('Link', 'reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses') x1`
  - `('Link', 'reference/glossary/GLOSSARY.md') x1`
- Extra/changed reference identities on the rendition side (absolute URLs counted as external):
  - count=15
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json') x1`
  - `('Link', 'https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py') x1`
  - … and 10 more

#### RENDITION_REVISION_PIN — `reuse-admission-and-cost-controls / zh-Hans`

- **Real sidecar:** `verify_pin` for source and rendition revisions succeeds against publication commit `2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`; mixed-pin check (source revision ancestor of rendition revision) succeeds.
- **Dry-run artifact:** `renditions_dry_run.py` synthesizes `source.revision=<publication HEAD>` and `rendition.revision=<commit that added the file>` (`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`), then reports `RENDITION_REVISION_PIN` because HEAD is not an ancestor of the earlier file commit. Message shape: `<work>/<lang>: the rendition revision predates the source revision it claims to render (mixed source/rendition pins)`. Compared pins in that audit: source.revision=`2ec7490b6c1fa9f95e6dbad49f6a6f44e6d17d2c`, rendition.revision=`8c8f2dc304e7db3a55e2b203d6ca3effadb77b91`.
- **Front-matter pin (translator content, not sidecar):** still `source_commit=a0450428704fcd41b411203f2fc88c06c779610b` with the old `source_git_blob`; dry-run `front_matter_pin_agrees=0` for every matched file.
- Dry-run failure rows for this path: `RENDITION_SECTION_MISSING`/parity, `RENDITION_REVISION_PIN`/pins

## Dry-run language totals

```json
{
  "ru": {
    "absent_documents": 26,
    "files_clean": 0,
    "files_found": 4,
    "files_with_a_failure": 4,
    "front_matter_pin_agrees": 0,
    "link_classes": {
      "document": 26,
      "document_fallback": 24,
      "document_shown": 2,
      "external": 47
    },
    "other_failures": {
      "RENDITION_REVISION_PIN": 4
    },
    "parity_failures": {
      "RENDITION_REFERENCE_DROPPED": 2,
      "RENDITION_SECTION_MISSING": 2
    },
    "path_matches": 4,
    "states": {
      "unreviewed": 4
    },
    "unmatched_paths": [],
    "unresolved_links": {}
  },
  "zh-Hans": {
    "absent_documents": 26,
    "files_clean": 0,
    "files_found": 4,
    "files_with_a_failure": 4,
    "front_matter_pin_agrees": 0,
    "link_classes": {
      "document": 26,
      "document_fallback": 24,
      "document_shown": 2,
      "external": 47
    },
    "other_failures": {
      "RENDITION_REVISION_PIN": 4
    },
    "parity_failures": {
      "RENDITION_REFERENCE_DROPPED": 2,
      "RENDITION_SECTION_MISSING": 2
    },
    "path_matches": 4,
    "states": {
      "unreviewed": 4
    },
    "unmatched_paths": [],
    "unresolved_links": {}
  }
}
```

## Build command used

```text
python3 -B scripts/build_publication.py \
  --source-dir /tmp/k8-worker-bdc939-knowledge-source \
  --roadmap-source-dir /tmp/k8-worker-bdc939-roadmap-source \
  --manifest /tmp/k8-worker-bdc939-publication-manifest.json
```

First build error: `RENDITION_REFERENCE_DROPPED` on `dependency-closure-and-package-delivery/ru` (absolute GitHub blob URLs). Per-entry `compile_entry(..., report=...)` was used afterward so all eight entries are covered even when the production build stops at the first refusal.

Record marker: `k8-first-admission-diagnostics-20261109-v1`.

## Iteration 2 (2026-11-09) — SCOPED PASS import

### Iteration 2 — Scope

Draft PR: [Arcanada-one/knowledge-contract#86](https://github.com/Arcanada-one/knowledge-contract/pull/86)
Branch head at report authorship: `c782f102e6370671e32008cd177bc133ae9cd64c` (bytes commit `690e6e3b6fdf1df2a771000933588cd7542521cc`; sidecar tip).
Translator corrections: PR76 commit `68a0b17ad766c189466fdf3e83cd0805388258ba`; record `reviews/renditions/k8-author-structural-corrections-20261109.md` (blob `b91dc0b0b8f877271f084ddb7a47117d9d986e67`).
Independent delta review: Agent-Brain comment 6742099993 (SCOPED PASS for four; CHANGES_REQUIRED for four).
Site compiler: `contract-place-site` `main` `b6d7532f48498d385171a41941cb864195a4fbc0` in a separate local checkout.
No rendition bytes were modified after import. No compiler changes.

Admitted (exact blobs):

| Work | Language | Source blob | Rendition blob | Rendition sha256 | resolve_state |
| --- | --- | --- | --- | --- | --- |
| `dependency-closure-and-package-delivery` | `ru` | `42294151076e662129a8716ea13a29dc2f967ec9` | `1a8f278cf6e179607f717999176962769187d982` | `09c0db6f99a849b66c5f7124244c06210c218622633f36a15303ca04aa9869af` | `reviewed` |
| `dependency-closure-and-package-delivery` | `zh-Hans` | `42294151076e662129a8716ea13a29dc2f967ec9` | `0c91fe6cce8b2a8e496b973b93e1bd278620b010` | `2798de80ffd73980ad248a70c817b9a886be8a86c27c5d2e5023116858c9ca32` | `reviewed` |
| `executable-projections-and-revision` | `ru` | `b2306980ba150d0a0841896b6123df5ff72fc319` | `e45ae5bfd7acb121aecded5907671b4c10aa8cd3` | `5d9be194925259f83dfc91944e1cb7a728c788ae109a6716679f3beee3a3b934` | `reviewed` |
| `executable-projections-and-revision` | `zh-Hans` | `b2306980ba150d0a0841896b6123df5ff72fc319` | `eea8b6e92e1a731aa0459a8b3ef3ec4bc4972f4f` | `8cfb892e196ab53a0996942b18c82a491e26f2dd79feacd22a23ec9eacb3336c` | `reviewed` |

Removed from PR86 (CHANGES_REQUIRED; later iteration): `source-transcription-and-uncertainty` and `reuse-admission-and-cost-controls` × `ru`/`zh-Hans` (files and sidecar entries).

### Iteration 2 — Outcome

`scripts/build_publication.py` against this head **refuses** every admitted entry on link classification. Review bind reaches `reviewed` (`resolve_state`), and `check_parity` with links set aside reports **OK** (section/structure/formula/code/reference multiset parity holds for these four). Native publish still blocked by English-depth relative hrefs that resolve under `translations/<lang>/` from the rendition file directory.

First build error: `RENDITION_LINK_UNPINNED` on `dependency-closure-and-package-delivery/ru` for `../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` → `translations/ru/reference/bibliography/BIBLIOGRAPHY.md`.

C5 / published-page checks: **not measured** — build did not produce rendition pages. No localized study page from these four entries is emitted; English fallback behaviour for missing/uncompiled locales therefore remains the site default, and noindex inventory for these routes was not produced by a successful compile.

Anchor/ID uniqueness on the four pages: **not measured on rendered HTML** (no compile). Source/rendition heading maps in the sidecar are unchanged from iteration 1 for these works; parity stage did not report `RENDITION_SECTION_*` or structure failures once link classification is collected separately.

### Iteration 2 — Ownership split

- **KC-Brain / translator content (must change rendition bytes + re-review):** every non-local-looking relative href that was written at English source depth (`../`, `../../../`, `evidence/...`, `checks/...`) must be rewritten so that a **literal** resolve from `translations/<lang>/engineering/studies/<study>/` reaches the same canonical English-tree path (example: English `../../../papers/X/PAPER.md` → `../../../../../papers/X/PAPER.md`). Same-language peer targets under `translations/<lang>/...` are only legal when that work/language is registered in the sidecar; today only these four studies are registered, so papers/glossary/bibliography/editorial-pilot peers are refused.
- **KC-SWE (this iteration, done without byte edits):** imported four SCOPED PASS blobs byte-exact; removed four CHANGES_REQUIRED files; added corrections ledger; repinned four sidecar entries with `author.identity=KC-Brain`, Agent-Brain composite review (comments 6735134008 + 6739674011 + 6742099993), source pin `2b5bcff544fea5d1752ff009933e4ce0305dad8b`, rendition revision `690e6e3b6fdf1df2a771000933588cd7542521cc`.

### Iteration 2 — `dependency-closure-and-package-delivery / ru`

- Rendition path: `translations/ru/engineering/studies/dependency-closure-and-package-delivery/STUDY.md`
- Sidecar source.revision: `2b5bcff544fea5d1752ff009933e4ce0305dad8b`
- Sidecar rendition.revision: `690e6e3b6fdf1df2a771000933588cd7542521cc`
- `resolve_state`: `reviewed`
- Compile failure codes: `RENDITION_LINK_TRANSLATION`, `RENDITION_LINK_UNPINNED`
- Parity with link classify set aside: `[{'parity': 'OK'}]`

#### Iteration 2 failing links (literal resolve from the rendition directory)

| Line | Literal href | Resolves to | Code | Href that reaches the English canonical target | Peer note |
| ---: | --- | --- | --- | --- | --- |
| 26 | `../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` | `translations/ru/reference/bibliography/BIBLIOGRAPHY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` | catalogue work `reference/bibliography/BIBLIOGRAPHY.md`; peer `translations/ru/reference/bibliography/BIBLIOGRAPHY.md` registered=False — peer only legal if sidecar-registered |
| 28 | `../../../papers/retrieval-and-context-composition/PAPER.md` | `translations/ru/papers/retrieval-and-context-composition/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/retrieval-and-context-composition/PAPER.md` | catalogue work `papers/retrieval-and-context-composition/PAPER.md`; peer `translations/ru/papers/retrieval-and-context-composition/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 28 | `../../../papers/constrained-transformations/PAPER.md` | `translations/ru/papers/constrained-transformations/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/constrained-transformations/PAPER.md` | catalogue work `papers/constrained-transformations/PAPER.md`; peer `translations/ru/papers/constrained-transformations/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 28 | `../../../papers/revision-and-governance/PAPER.md` | `translations/ru/papers/revision-and-governance/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/revision-and-governance/PAPER.md` | catalogue work `papers/revision-and-governance/PAPER.md`; peer `translations/ru/papers/revision-and-governance/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 52 | `evidence/finite-package-selftest.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json` | not a catalogue document path; not a legal peer |
| 54 | `../README.md#counting-and-interpretation` | `translations/ru/engineering/studies/README.md` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/README.md#counting-and-interpretation` | not a catalogue document path; not a legal peer |
| 60 | `evidence/dependency-graph.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json` | not a catalogue document path; not a legal peer |
| 60 | `evidence/replay_closure.py` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py` | not a catalogue document path; not a legal peer |
| 68 | `evidence/public-closure-replay.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json` | not a catalogue document path; not a legal peer |
| 72 | `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | `translations/ru/reference/bibliography/BIBLIOGRAPHY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | catalogue work `reference/bibliography/BIBLIOGRAPHY.md`; peer `translations/ru/reference/bibliography/BIBLIOGRAPHY.md` registered=False — peer only legal if sidecar-registered |
| 74 | `checks/check_closure_size_and_mutations.py` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py` | not a catalogue document path; not a legal peer |
| 74 | `checks/closure-size-and-mutation-check.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json` | not a catalogue document path; not a legal peer |
| 96 | `evidence/layout-preservation-report.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json` | not a catalogue document path; not a legal peer |
| 98 | `evidence/layout-conformance-report.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json` | not a catalogue document path; not a legal peer |
| 104 | `evidence/historical-package-replay.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json` | not a catalogue document path; not a legal peer |
| 104 | `evidence/historical-replay-environment.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json` | not a catalogue document path; not a legal peer |
| 122 | `../editorial-skill-pilot/STUDY.md` | `translations/ru/engineering/studies/editorial-skill-pilot/STUDY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../engineering/studies/editorial-skill-pilot/STUDY.md` | catalogue work `engineering/studies/editorial-skill-pilot/STUDY.md`; peer `translations/ru/engineering/studies/editorial-skill-pilot/STUDY.md` registered=False — peer only legal if sidecar-registered |
| 122 | `../../../reference/glossary/GLOSSARY.md` | `translations/ru/reference/glossary/GLOSSARY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/glossary/GLOSSARY.md` | catalogue work `reference/glossary/GLOSSARY.md`; peer `translations/ru/reference/glossary/GLOSSARY.md` registered=False — peer only legal if sidecar-registered |
| 124 | `evidence/origin.json` | `translations/ru/engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json` | not a catalogue document path; not a legal peer |
| 124 | `../evidence-language-index.json` | `translations/ru/engineering/studies/evidence-language-index.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/evidence-language-index.json` | not a catalogue document path; not a legal peer |
| 124 | `../review-corrections.json` | `translations/ru/engineering/studies/review-corrections.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/review-corrections.json` | not a catalogue document path; not a legal peer |

### Iteration 2 — `dependency-closure-and-package-delivery / zh-Hans`

- Rendition path: `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/STUDY.md`
- Sidecar source.revision: `2b5bcff544fea5d1752ff009933e4ce0305dad8b`
- Sidecar rendition.revision: `690e6e3b6fdf1df2a771000933588cd7542521cc`
- `resolve_state`: `reviewed`
- Compile failure codes: `RENDITION_LINK_TRANSLATION`, `RENDITION_LINK_UNPINNED`
- Parity with link classify set aside: `[{'parity': 'OK'}]`

#### Iteration 2 failing links (literal resolve from the rendition directory)

| Line | Literal href | Resolves to | Code | Href that reaches the English canonical target | Peer note |
| ---: | --- | --- | --- | --- | --- |
| 26 | `../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` | `translations/zh-Hans/reference/bibliography/BIBLIOGRAPHY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input` | catalogue work `reference/bibliography/BIBLIOGRAPHY.md`; peer `translations/zh-Hans/reference/bibliography/BIBLIOGRAPHY.md` registered=False — peer only legal if sidecar-registered |
| 28 | `../../../papers/retrieval-and-context-composition/PAPER.md` | `translations/zh-Hans/papers/retrieval-and-context-composition/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/retrieval-and-context-composition/PAPER.md` | catalogue work `papers/retrieval-and-context-composition/PAPER.md`; peer `translations/zh-Hans/papers/retrieval-and-context-composition/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 28 | `../../../papers/constrained-transformations/PAPER.md` | `translations/zh-Hans/papers/constrained-transformations/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/constrained-transformations/PAPER.md` | catalogue work `papers/constrained-transformations/PAPER.md`; peer `translations/zh-Hans/papers/constrained-transformations/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 28 | `../../../papers/revision-and-governance/PAPER.md` | `translations/zh-Hans/papers/revision-and-governance/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/revision-and-governance/PAPER.md` | catalogue work `papers/revision-and-governance/PAPER.md`; peer `translations/zh-Hans/papers/revision-and-governance/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 52 | `evidence/finite-package-selftest.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json` | not a catalogue document path; not a legal peer |
| 54 | `../README.md#counting-and-interpretation` | `translations/zh-Hans/engineering/studies/README.md` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/README.md#counting-and-interpretation` | not a catalogue document path; not a legal peer |
| 60 | `evidence/dependency-graph.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json` | not a catalogue document path; not a legal peer |
| 60 | `evidence/replay_closure.py` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py` | not a catalogue document path; not a legal peer |
| 68 | `evidence/public-closure-replay.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json` | not a catalogue document path; not a legal peer |
| 72 | `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | `translations/zh-Hans/reference/bibliography/BIBLIOGRAPHY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | catalogue work `reference/bibliography/BIBLIOGRAPHY.md`; peer `translations/zh-Hans/reference/bibliography/BIBLIOGRAPHY.md` registered=False — peer only legal if sidecar-registered |
| 74 | `checks/check_closure_size_and_mutations.py` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py` | not a catalogue document path; not a legal peer |
| 74 | `checks/closure-size-and-mutation-check.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json` | not a catalogue document path; not a legal peer |
| 96 | `evidence/layout-preservation-report.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json` | not a catalogue document path; not a legal peer |
| 98 | `evidence/layout-conformance-report.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json` | not a catalogue document path; not a legal peer |
| 104 | `evidence/historical-package-replay.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json` | not a catalogue document path; not a legal peer |
| 104 | `evidence/historical-replay-environment.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json` | not a catalogue document path; not a legal peer |
| 122 | `../editorial-skill-pilot/STUDY.md` | `translations/zh-Hans/engineering/studies/editorial-skill-pilot/STUDY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../engineering/studies/editorial-skill-pilot/STUDY.md` | catalogue work `engineering/studies/editorial-skill-pilot/STUDY.md`; peer `translations/zh-Hans/engineering/studies/editorial-skill-pilot/STUDY.md` registered=False — peer only legal if sidecar-registered |
| 122 | `../../../reference/glossary/GLOSSARY.md` | `translations/zh-Hans/reference/glossary/GLOSSARY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/glossary/GLOSSARY.md` | catalogue work `reference/glossary/GLOSSARY.md`; peer `translations/zh-Hans/reference/glossary/GLOSSARY.md` registered=False — peer only legal if sidecar-registered |
| 124 | `evidence/origin.json` | `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json` | not a catalogue document path; not a legal peer |
| 124 | `../evidence-language-index.json` | `translations/zh-Hans/engineering/studies/evidence-language-index.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/evidence-language-index.json` | not a catalogue document path; not a legal peer |
| 124 | `../review-corrections.json` | `translations/zh-Hans/engineering/studies/review-corrections.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/review-corrections.json` | not a catalogue document path; not a legal peer |

### Iteration 2 — `executable-projections-and-revision / ru`

- Rendition path: `translations/ru/engineering/studies/executable-projections-and-revision/STUDY.md`
- Sidecar source.revision: `2b5bcff544fea5d1752ff009933e4ce0305dad8b`
- Sidecar rendition.revision: `690e6e3b6fdf1df2a771000933588cd7542521cc`
- `resolve_state`: `reviewed`
- Compile failure codes: `RENDITION_LINK_TRANSLATION`, `RENDITION_LINK_UNPINNED`
- Parity with link classify set aside: `[{'parity': 'OK'}]`

#### Iteration 2 failing links (literal resolve from the rendition directory)

| Line | Literal href | Resolves to | Code | Href that reaches the English canonical target | Peer note |
| ---: | --- | --- | --- | --- | --- |
| 26 | `../../../papers/retrieval-and-context-composition/PAPER.md` | `translations/ru/papers/retrieval-and-context-composition/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/retrieval-and-context-composition/PAPER.md` | catalogue work `papers/retrieval-and-context-composition/PAPER.md`; peer `translations/ru/papers/retrieval-and-context-composition/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 26 | `../../../papers/revision-and-governance/PAPER.md` | `translations/ru/papers/revision-and-governance/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/revision-and-governance/PAPER.md` | catalogue work `papers/revision-and-governance/PAPER.md`; peer `translations/ru/papers/revision-and-governance/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 26 | `../../../papers/evidence-and-falsification/PAPER.md` | `translations/ru/papers/evidence-and-falsification/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/evidence-and-falsification/PAPER.md` | catalogue work `papers/evidence-and-falsification/PAPER.md`; peer `translations/ru/papers/evidence-and-falsification/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 32 | `evidence/historical-reader-study-source.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json` | not a catalogue document path; not a legal peer |
| 34 | `../source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | `translations/ru/engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | not a catalogue document path; not a legal peer |
| 53 | `evidence/reader-boundary-report.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json` | not a catalogue document path; not a legal peer |
| 57 | `evidence/targeted-revision-comparison.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json` | not a catalogue document path; not a legal peer |
| 74 | `evidence/addressability-study-source.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | not a catalogue document path; not a legal peer |
| 88 | `evidence/consumer-qualification-report.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json` | not a catalogue document path; not a legal peer |
| 104 | `evidence/agent-projection-results.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json` | not a catalogue document path; not a legal peer |
| 116 | `evidence/origin.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/origin.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/origin.json` | not a catalogue document path; not a legal peer |
| 116 | `evidence/offline-projection-replay-report.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json` | not a catalogue document path; not a legal peer |
| 118 | `../historical-recovery-gaps.json` | `translations/ru/engineering/studies/historical-recovery-gaps.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/historical-recovery-gaps.json` | not a catalogue document path; not a legal peer |
| 120 | `evidence/projection-study-source.json` | `translations/ru/engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json` | not a catalogue document path; not a legal peer |
| 120 | `../evidence-language-index.json` | `translations/ru/engineering/studies/evidence-language-index.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/evidence-language-index.json` | not a catalogue document path; not a legal peer |
| 120 | `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | `translations/ru/reference/bibliography/BIBLIOGRAPHY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | catalogue work `reference/bibliography/BIBLIOGRAPHY.md`; peer `translations/ru/reference/bibliography/BIBLIOGRAPHY.md` registered=False — peer only legal if sidecar-registered |
| 124 | `../../../reference/glossary/GLOSSARY.md` | `translations/ru/reference/glossary/GLOSSARY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/glossary/GLOSSARY.md` | catalogue work `reference/glossary/GLOSSARY.md`; peer `translations/ru/reference/glossary/GLOSSARY.md` registered=False — peer only legal if sidecar-registered |

### Iteration 2 — `executable-projections-and-revision / zh-Hans`

- Rendition path: `translations/zh-Hans/engineering/studies/executable-projections-and-revision/STUDY.md`
- Sidecar source.revision: `2b5bcff544fea5d1752ff009933e4ce0305dad8b`
- Sidecar rendition.revision: `690e6e3b6fdf1df2a771000933588cd7542521cc`
- `resolve_state`: `reviewed`
- Compile failure codes: `RENDITION_LINK_TRANSLATION`, `RENDITION_LINK_UNPINNED`
- Parity with link classify set aside: `[{'parity': 'OK'}]`

#### Iteration 2 failing links (literal resolve from the rendition directory)

| Line | Literal href | Resolves to | Code | Href that reaches the English canonical target | Peer note |
| ---: | --- | --- | --- | --- | --- |
| 26 | `../../../papers/retrieval-and-context-composition/PAPER.md` | `translations/zh-Hans/papers/retrieval-and-context-composition/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/retrieval-and-context-composition/PAPER.md` | catalogue work `papers/retrieval-and-context-composition/PAPER.md`; peer `translations/zh-Hans/papers/retrieval-and-context-composition/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 26 | `../../../papers/revision-and-governance/PAPER.md` | `translations/zh-Hans/papers/revision-and-governance/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/revision-and-governance/PAPER.md` | catalogue work `papers/revision-and-governance/PAPER.md`; peer `translations/zh-Hans/papers/revision-and-governance/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 26 | `../../../papers/evidence-and-falsification/PAPER.md` | `translations/zh-Hans/papers/evidence-and-falsification/PAPER.md` | `RENDITION_LINK_UNPINNED` | `../../../../../papers/evidence-and-falsification/PAPER.md` | catalogue work `papers/evidence-and-falsification/PAPER.md`; peer `translations/zh-Hans/papers/evidence-and-falsification/PAPER.md` registered=False — peer only legal if sidecar-registered |
| 32 | `evidence/historical-reader-study-source.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json` | not a catalogue document path; not a legal peer |
| 34 | `../source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | `translations/zh-Hans/engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json` | not a catalogue document path; not a legal peer |
| 53 | `evidence/reader-boundary-report.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json` | not a catalogue document path; not a legal peer |
| 57 | `evidence/targeted-revision-comparison.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json` | not a catalogue document path; not a legal peer |
| 74 | `evidence/addressability-study-source.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json` | not a catalogue document path; not a legal peer |
| 88 | `evidence/consumer-qualification-report.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json` | not a catalogue document path; not a legal peer |
| 104 | `evidence/agent-projection-results.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json` | not a catalogue document path; not a legal peer |
| 116 | `evidence/origin.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/origin.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/origin.json` | not a catalogue document path; not a legal peer |
| 116 | `evidence/offline-projection-replay-report.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json` | not a catalogue document path; not a legal peer |
| 118 | `../historical-recovery-gaps.json` | `translations/zh-Hans/engineering/studies/historical-recovery-gaps.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/historical-recovery-gaps.json` | not a catalogue document path; not a legal peer |
| 120 | `evidence/projection-study-source.json` | `translations/zh-Hans/engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json` | not a catalogue document path; not a legal peer |
| 120 | `../evidence-language-index.json` | `translations/zh-Hans/engineering/studies/evidence-language-index.json` | `RENDITION_LINK_TRANSLATION` | `../../../../../engineering/studies/evidence-language-index.json` | not a catalogue document path; not a legal peer |
| 120 | `../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | `translations/zh-Hans/reference/bibliography/BIBLIOGRAPHY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods` | catalogue work `reference/bibliography/BIBLIOGRAPHY.md`; peer `translations/zh-Hans/reference/bibliography/BIBLIOGRAPHY.md` registered=False — peer only legal if sidecar-registered |
| 124 | `../../../reference/glossary/GLOSSARY.md` | `translations/zh-Hans/reference/glossary/GLOSSARY.md` | `RENDITION_LINK_UNPINNED` | `../../../../../reference/glossary/GLOSSARY.md` | catalogue work `reference/glossary/GLOSSARY.md`; peer `translations/zh-Hans/reference/glossary/GLOSSARY.md` registered=False — peer only legal if sidecar-registered |


### Iteration 2 — knowledge-contract link-check (lychee)

Hosted CI `link-check` on head `8281ebeb40fb050b33b131bb38ffb0e176f93491` (run `42635137977`) reported **76** offline `File not found` errors, all under `translations/<lang>/…` from the four admitted SCOPED PASS blobs. This is the same English-depth relative-href problem as the site compiler; rendition bytes were not edited. Per-file counts from the job log:

| File | File not found |
| --- | ---: |
| `translations/ru/engineering/studies/dependency-closure-and-package-delivery/STUDY.md` | 21 |
| `translations/ru/engineering/studies/executable-projections-and-revision/STUDY.md` | 17 |
| `translations/zh-Hans/engineering/studies/dependency-closure-and-package-delivery/STUDY.md` | 21 |
| `translations/zh-Hans/engineering/studies/executable-projections-and-revision/STUDY.md` | 17 |
| **Total** | **76** |

`markdown-lint` MD024 duplicates on this diagnostics file are fixed in a follow-up tip; `link-check` remains red until new rendition-depth blobs arrive. PR stays draft.


### Iteration 2 — Dry-run language totals

```json
{
  "ru": {
    "absent_documents": 28,
    "files_clean": 0,
    "files_found": 2,
    "files_with_a_failure": 2,
    "front_matter_pin_agrees": 0,
    "link_classes": {
      "document_shown": 1,
      "peer": 1
    },
    "other_failures": {
      "RENDITION_REVISION_PIN": 2
    },
    "parity_failures": {},
    "path_matches": 2,
    "states": {
      "unreviewed": 2
    },
    "unmatched_paths": [],
    "unresolved_links": {
      "RENDITION_LINK_TRANSLATION": 26,
      "RENDITION_LINK_UNPINNED": 12
    }
  },
  "zh-Hans": {
    "absent_documents": 28,
    "files_clean": 0,
    "files_found": 2,
    "files_with_a_failure": 2,
    "front_matter_pin_agrees": 0,
    "link_classes": {
      "document_shown": 1,
      "peer": 1
    },
    "other_failures": {
      "RENDITION_REVISION_PIN": 2
    },
    "parity_failures": {},
    "path_matches": 2,
    "states": {
      "unreviewed": 2
    },
    "unmatched_paths": [],
    "unresolved_links": {
      "RENDITION_LINK_TRANSLATION": 26,
      "RENDITION_LINK_UNPINNED": 12
    }
  }
}
```

Dry-run notes: `RENDITION_REVISION_PIN` rows are the known dry-run artifact (synthetic source.revision=HEAD vs earlier/mixed pins). `front_matter_pin_agrees=0` remains because dry-run compares front-matter pins in its own way; the admitted blobs now name current main source blobs (`42294151…` / `b2306980…`) at commit `2b5bcff`.

### Iteration 2 — Build command used

```text
python3 -B scripts/build_publication.py \
  --source-dir /tmp/k8-iter2-knowledge-source \
  --roadmap-source-dir /tmp/k8-iter2-roadmap-source \
  --manifest /tmp/k8-iter2-publication-manifest.json
```

Record marker: `k8-first-admission-diagnostics-20261109-v2`.
