---
title: "K8 scientific author-side structural rendition corrections"
sources: none
status: "candidate; not yet independently re-reviewed or published"
updated: 2026-11-09
---

# K8: exact rendition correction ledger

Prepared by KC-Brain as scientific/translation content work on existing PR76, in response to [draft PR86 compiler diagnostics](https://github.com/Arcanada-one/knowledge-contract/blob/1fa1d1d59bfc9f72c68a6234bbb47abe3d016baf/reviews/renditions/k8-first-admission-diagnostics-20261109.md). Source current accepted English main commit `2b5bcff544fea5d1752ff009933e4ce0305dad8b`; the four source blobs were fetched at that commit and matched the current reviewed-source list. No manuscript proposition, evidence claim, mathematical formula, translated sentence, or retained report changed.

Only: (1) legacy absolute `a0450428` GitHub source links were restored to exact English-relative targets, including anchors; (2) the English historic-anchor preamble was copied verbatim into the two affected works in both languages; (3) front-matter `source_commit` and `source_git_blob` now identify the accepted English sources. For every row, the ordered local target link multiset matches the current English study. External non-source links are otherwise unchanged. `translation_status: author-draft` is retained, deliberately, until post-change independent review and actual admission.

| Work | Language | Old rendition Git blob | New candidate rendition Git blob | Current English Git blob | Restored relative links | Historic anchor preamble |
| --- | --- | --- | --- | --- | ---: | --- |
| `dependency-closure-and-package-delivery` | `ru` | `5aa9ee44986a68c0e47d99c801ec11a2fe1ddd9e` | `1a8f278cf6e179607f717999176962769187d982` | `42294151076e662129a8716ea13a29dc2f967ec9` | 21 | no |
| `dependency-closure-and-package-delivery` | `zh-Hans` | `6d78e14dd29bbe751e5d7699a8ff76383395dc62` | `0c91fe6cce8b2a8e496b973b93e1bd278620b010` | `42294151076e662129a8716ea13a29dc2f967ec9` | 21 | no |
| `source-transcription-and-uncertainty` | `ru` | `4a8e7b8d986c3eb846cb6ea381dcc1b0685755d1` | `f31cce9e27f29afad70aae1cde643e912fd94468` | `8ca885fc3f144d89e95e4813868fd953450f1f71` | 18 | yes |
| `source-transcription-and-uncertainty` | `zh-Hans` | `1be23f4f57ae705870149cc61964c3bb2c1d3784` | `e692e3d92d695916265463706be6e3c2b0975e5f` | `8ca885fc3f144d89e95e4813868fd953450f1f71` | 18 | yes |
| `executable-projections-and-revision` | `ru` | `f9361172e1fe559e90aac4be615f19474dc7a941` | `e45ae5bfd7acb121aecded5907671b4c10aa8cd3` | `b2306980ba150d0a0841896b6123df5ff72fc319` | 18 | no |
| `executable-projections-and-revision` | `zh-Hans` | `346d23b860650abbebfe55e3f7d9f90e85dcedd2` | `eea8b6e92e1a731aa0459a8b3ef3ec4bc4972f4f` | `b2306980ba150d0a0841896b6123df5ff72fc319` | 18 | no |
| `reuse-admission-and-cost-controls` | `ru` | `90bca419fac0c0834fe4bce4513772812958bbec` | `4c73b4c48b0a4cd37a100957210ee5acc25c7a4f` | `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac` | 16 | yes |
| `reuse-admission-and-cost-controls` | `zh-Hans` | `1c3cbeff2939888d2a95414ec3315b2671cb46f0` | `13898fda23d9ef2a1243399b134f50de41d348d8` | `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac` | 16 | yes |

## Roles and authorship

The existing `author: Pavel Valentov` names the underlying scientific author / rights holder and does **not** assert he manually translated each localized file. The translation drafting and this structural repair were performed by **KC-Brain (AI role)** under his instruction. The earlier composite independent scientific fidelity checks were performed by a distinct role, **Agent-Brain (AI reviewer)**; they are not external, human or native-speaker peer review. The sidecar must not describe independence merely as Agent-Brain versus Pavel if the actual rendition preparer was KC-Brain. The review attribution must bind exact source/target blobs and cite both underlying phases, with limitations.

## Remaining gates

1. Agent-Brain independently checks these eight exact old-to-new blob deltas, including possible duplicate historical anchor IDs in the rendered HTML. Previous reviews were for older rendition blobs.
2. Existing KC-SWE K8 worker imports exact candidate blobs on PR86, updates schema-v2 sidecar hashes/revision ancestry/review evidence and corrects independence basis; it must not write or reinterpret scientific translation prose.
3. Native site build/check_publication, structure/anchor/link/formula parity, hosted CI and exact-head independent acceptance are distinct from this source-blob ledger. Merge, accepted release pin, deployment and served-language readback need their ordinary authorisations. An English fallback is not a translated served page. No status claim beyond candidate is made.
