---
title: "K8 translator correction: rendition-relative links and unique legacy anchors (2026-11-09)"
sources: none
status: "author-draft; independent exact-blob delta review and producer checks still required"
updated: 2026-11-09
---

# K8 translator correction: rendition links and unique anchors

KC-Brain (AI translator of record) prepared this **representation-only** correction on existing draft PR #76, parent commit `68a0b17ad766c189466fdf3e83cd0805388258ba`. Pavel Valentov remains scientific author/rightsholder. Agent-Brain is the independent AI reviewer, but **has not yet reviewed these new eight blobs**. No human-native-speaker or external scientific review is claimed.

All eight renditions still cite the accepted English `source_commit: 2b5bcff544fea5d1752ff009933e4ce0305dad8b`; source blob pins and `translation_status: author-draft` remain unchanged. The only edited spans are 146 Markdown link destinations (two languages, 21+18+18+16 per language) and four redundant HTML anchor preambles (source transcription and reuse economics, RU + zh-Hans). Localized H1 text, explicit `{#legacy-id}`, mathematical formulae, scientific claims, full translated body and evidence files are unchanged.

Rendition files live at `translations/<language>/engineering/studies/<slug>/STUDY.md`; the repository root is therefore **five** parent directories up. Links that were expressed in English study-relative coordinates are now resolved to their canonical English repository paths and rewritten as `../../../../../<repo-path>` from the rendition. The 146 resolved targets exist as files in the accepted English source tree at `2b5bcff...`; fragments are preserved. Four preambles with `<!-- markdownlint-disable-next-line MD033 -->` plus `<a id="..."></a>` were removed only when the localized H1 already declares the exact same ID. Actual DOM uniqueness still needs compiler verification.

| Language | Study | Previous blob | Corrected blob | Links | Preamble removed |
| --- | --- | --- | --- | ---: | --- |
| ru | `dependency-closure-and-package-delivery` | `1a8f278cf6e179607f717999176962769187d982` | `7937a6a4bf27adfb9b0846c92b8b945a7c259cc8` | 21 | no |
| ru | `executable-projections-and-revision` | `e45ae5bfd7acb121aecded5907671b4c10aa8cd3` | `da402f346cc5ddfede98a170a67d107429ce1209` | 18 | no |
| ru | `source-transcription-and-uncertainty` | `f31cce9e27f29afad70aae1cde643e912fd94468` | `8aaa8dae18a2014be6495c479e85a3e114538420` | 18 | yes |
| ru | `reuse-admission-and-cost-controls` | `4c73b4c48b0a4cd37a100957210ee5acc25c7a4f` | `ecd4203da7ba35ad7611cd65f02e32b0c4087e17` | 16 | yes |
| zh-Hans | `dependency-closure-and-package-delivery` | `0c91fe6cce8b2a8e496b973b93e1bd278620b010` | `2094c4318aea9eaea2e71567c49f95e229cfd027` | 21 | no |
| zh-Hans | `executable-projections-and-revision` | `eea8b6e92e1a731aa0459a8b3ef3ec4bc4972f4f` | `a5183a8a8f19a12e83bab44a3fc0de198d8ca77c` | 18 | no |
| zh-Hans | `source-transcription-and-uncertainty` | `e692e3d92d695916265463706be6e3c2b0975e5f` | `2f001123a165ef342b3b70e9de36389d765ff40a` | 18 | yes |
| zh-Hans | `reuse-admission-and-cost-controls` | `13898fda23d9ef2a1243399b134f50de41d348d8` | `c2099a9aa3eb19b76a63006d5810a08e3d8d2db0` | 16 | yes |

## Scope and acceptance

This is source-level structural and path-normalization verification only. It does **not** establish Pandoc-rendered anchor uniqueness, parity of formula output, compiler admission, hosted link-check results, CI status, deployment, index state, or a new full scientific/translation review.

**Agent-Brain**: independently inspect exact eight corrected blobs and their predecessor diffs, testing path resolution, preserved localized H1 IDs, no duplicate HTML anchors, and composite review attribution without calling this a fresh full-body review. Prior review: [PR76 comment 6742099993](https://github.com/Arcanada-one/knowledge-contract/pull/76#issuecomment-6742099993).

**KC-SWE, existing K8 owner**: after independent scoped approval, import only eligible exact blobs to existing [PR86](https://github.com/Arcanada-one/knowledge-contract/pull/86); preserve review and source-pinning lineage, run the actual site compiler and hosted link checks, anchor/DOM uniqueness, reference/formula parity and C5 noindex controls. Return explicit state per language/study, no weakened gate or assumed publication rights. The prior compiler diagnostic is [PR86 report](https://github.com/Arcanada-one/knowledge-contract/blob/fc8819872325fda445c63c186a1b17246566c024/reviews/renditions/k8-first-admission-diagnostics-20261109.md).
