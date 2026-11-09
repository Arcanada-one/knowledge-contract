---
title: "Four engineering studies: source-currency delta and review handoff"
sources: none
status: "KC-Brain author-side analysis; NOT a rendition admission or independent fidelity review"
updated: 2026-11-09
---

# Four engineering studies — source-currency comparison for RU and zh-Hans

**Scope:** the eight full KC-Brain-authored translations in PR76 at target head `34405422aad944fab20f96bcecd863f7bad7cd59`, reviewed by Agent-Brain against English a0450428704fcd41b411203f2fc88c06c779610b. The four English sources now accepted at 660874393f740c07f5f4bac6a1627bda1921a119 do not have the same Git blobs. This is a source-currency handoff, not a silent transfer of a previous review, site publication, sidecar, or authority to merge. English and translation rights remain the original project's; no external material is reproduced here.

**Evidence:** [actual Git comparison](https://github.com/Arcanada-one/knowledge-contract/compare/a0450428704fcd41b411203f2fc88c06c779610b...660874393f740c07f5f4bac6a1627bda1921a119) filtered to the four named `engineering/studies/*/STUDY.md` paths, and [Agent-Brain's independent exact-pair fidelity decision](https://github.com/Arcanada-one/knowledge-contract/pull/76#issuecomment-6735134008), made 2026-11-09T08:00:47Z. The reviewer personally read all four complete earlier English bodies and eight complete target bodies, preserving limitations, but did not certify the changed current-source bytes as a newly reviewed pair.

| Study / path stem | Earlier reviewed English blob | Current accepted English blob | RU target blob | zh-Hans target blob |
| --- | --- | --- | --- | --- |
| `dependency-closure-and-package-delivery` | `63078110074e82b47f76a8f132a3cfdcbfb555b1` | `42294151076e662129a8716ea13a29dc2f967ec9` | `5aa9ee44986a68c0e47d99c801ec11a2fe1ddd9e` | `6d78e14dd29bbe751e5d7699a8ff76383395dc62` |
| `source-transcription-and-uncertainty` | `5f19fc3d33fa0e185c34056188ce7742bee87` | `8ca885fc3f144d89e95e4813868fd953450f1f71` | `4a8e7b8d986c3eb846cb6ea381dcc1b0685755d1` | `1be23f4f57ae705870149cc61964c3bb2c1d3784` |
| `executable-projections-and-revision` | `2d247a01d4dbd6a1d1491d2b54464336c6fef190` | `b2306980ba150d0a0841896b6123df5ff72fc319` | `f9361172e1fe559e90aac4be615f19474dc7a941` | `346d23b860650abbebfe55e3f7d9f90e85dcedd2` |
| `reuse-admission-and-cost-controls` | `67ab4b55faf9f42df2d6d7214bbbe4f30c143a8e` | `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac` | `90bca419fac0c0834fe4bce4513772812958bbec` | `1c3cbeff2939888d2a95414ec3315b2671cb46f0` |

All paths use `engineering/studies/<stem>/STUDY.md`; targets use `translations/ru/` or `translations/zh-Hans/` as prefixes. The target blobs are historical exact subjects of the Agent-Brain review, not evidence that new source pins are accepted.

## Actual English difference

Across these four files, the exact comparison has **no changes to the Abstract or later scientific paragraphs, equations, tables, measured denominators, interpretations or adverse outcomes**. It changes each front-matter `title`, adds `short_title`, `subtitle` and `previous_title`, and changes the H1 display name. Two studies additionally insert an explicit historic H1 anchor plus a Markdown-lint exception: Uncertainty Preservation and Reuse Economics. Each first-published title remains in `previous_title`.

The earlier reviewed translations already have localized short-name H1s and historical source heading anchors. This supports a **bounded delta review**, not wholesale rewriting of the scientific bodies. It does *not* automatically prove anchor parity of every rendition against the newer source, navigation behavior, or current-source review. The source-title and section-anchor changes must be checked on the actual paired files and in the compiler's structural/link parity gate. Keep valid historical links and previously checked equations untouched.

## Publication gate: concrete pending inputs

1. **Reviewer delta.** Agent-Brain should verify only the changed front matter/H1/anchors against the eight unchanged target blobs and record a new exact-source-delta decision. Do not misattribute this author-side comparison to the independent reviewer. The full original review remains historically valid at its own source blobs and has not been invalidated retroactively.
2. **Source pin and lineage.** Current RU and zh-Hans front matter still records `source_commit: a0450428704fcd41b411203f2fc88c06c779610b` and the earlier source blobs. Those fields must not be silently replaced to make K8 look current. After exact-source delta approval, retain the original provenance in the review record and set verifiable new source pin metadata through an explicit, reviewed commit. The sidecar v2's source/rendition revision ancestry constraints must be tested against the *actual merged publication graph*; a proposal-branch commit predating the accepted main source revision must not masquerade as a post-source reviewed rendition.
3. **In-repository independent evidence.** Source comments are linked here faithfully, but this file is **KC-Brain's authored delta inventory**, not an Agent-Brain-signed independent review receipt. The separately authored Agent-Brain review, its actual method/limitations, exact new source and target blobs, and reviewed full/partial scope need to be recorded by an attributable follow-up evidence artifact. Only then may an engineer mechanically construct a closed `review` object in `publication-renditions.json`.
4. **Separate rendition decision and engineering.** KC-Brain must name admitted pairs and scope explicitly; KC-SWE only assembles the sidecar, performs exact-source compiler/parity checks, passes required CI/review/merge and executes the established site build, deployment and served-body readback. Until then: draft, not approved, and English fallback is not a translated page.

The comparison is a read-only source-delta analysis. **No K8 sidecar, content source-pins, catalogue/index allowlist, Muneral state, deployment or live source-admission gate is changed here.** The eight existing target files are unchanged by this evidence-only addition. The current author-inventory 50/60 in PR76 is not a release or served-language count.

Review handoff marker: `kc-brain-four-studies-source-currency-delta-20261109-v1`.
