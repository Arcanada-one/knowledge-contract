---
title: "Edition 1.1 translation coverage: hash-pinned author snapshot"
sources: none
status: "producer coverage audit; not independent semantic acceptance"
---

# Edition 1.1 translation coverage — source-pinned working snapshot

This is a **producer-authored inventory** of exactly the thirty canonical works in publication catalogue 1.1. English is the authoritative source for each entry in this snapshot; earlier Russian manuscripts cannot silently replace the corrected English revision. The source pin is `a0450428704fcd41b411203f2fc88c06c779610b`. The source SHA-256 values below are transcribed from the **already deployed** `contract-place-site/public/content-provenance.json` at site commit `21a15a65be8b7ce2544aac1eb43a929d2043b114`; they are not new tests of GitHub blobs. The snapshot of translation paths is PR #76 at head `c8200b4b90af353ec376b60da3eb34a0a0481704`, inspected on 2026-11-07 UTC. A later PR head requires refreshing this coverage record before any release decision.

Every `author-draft` means: a complete intended target file was present in the proposal branch, its front matter asserted the pinned original, and **no independent semantic acceptance, merge, build, live publication or index admission is established** by that label. It is not a statement of flawless translation. `absent` means the target was absent from that exact proposal snapshot, not that a former edition lacked translations. The source paper `human-meaning-and-computable-knowledge` separately retains `research-draft` status; translation does not promote it.

**Denominators:** 9 papers, 11 specifications, 6 studies, 1 glossary, 1 bibliography and 2 appendices = **30** canonical documents. The inspected PR held **12/30 author-draft target files in each language (24 target files)**: all eleven specifications and the glossary. The other **18/30 per language** had no current target file. Ancillary public prose (home pages, SEO, explanatory/reader text) is a separate tracked scope, **not counted within 30**. English serves as the immutable comparison source, not an additional translated target.

| # | Class | Canonical English work | Source SHA-256 (raw file) | Russian `ru` | Chinese `zh-Hans` |
| ---: | --- | --- | --- | --- | --- |
| 1 | `paper` | [`human-meaning-and-computable-knowledge`](../../papers/human-meaning-and-computable-knowledge/PAPER.md) | `f5cdf5856b230cd8d406fc3aea584d33e81f06ef14a36ebabd238825b3526af7` | absent | absent |
| 2 | `paper` | [`semantic-objects-and-context`](../../papers/semantic-objects-and-context/PAPER.md) | `6e466fed142538a5b147568e3a9e3aa017018083af0a1c3ac33afa48758c4c84` | absent | absent |
| 3 | `paper` | [`constrained-transformations`](../../papers/constrained-transformations/PAPER.md) | `6377a15c2d46ba82472342da4d77267c47aae5b1be1d7964f8edd373fa3b0eea` | absent | absent |
| 4 | `paper` | [`retrieval-and-context-composition`](../../papers/retrieval-and-context-composition/PAPER.md) | `e457fadcb17424e15083504a2babb2646aedc8aec7370048cd77854a8c7af64f` | absent | absent |
| 5 | `paper` | [`interaction-and-memory`](../../papers/interaction-and-memory/PAPER.md) | `6bf13bff5230129c4f077515015f2926c65f6fb2d97f3e1d61e5eaa6b584a2c8` | absent | absent |
| 6 | `paper` | [`evidence-and-falsification`](../../papers/evidence-and-falsification/PAPER.md) | `926b29d227f9c576bc69834ae6f8a72d514fc3b5916bf66c966df5aee5a2ce28` | absent | absent |
| 7 | `paper` | [`revision-and-governance`](../../papers/revision-and-governance/PAPER.md) | `20079132357dc2e4e651cde78d528b37712ecdef030af3934ebd2e8048e3f78a` | absent | absent |
| 8 | `paper` | [`controlled-knowledge-reuse`](../../papers/controlled-knowledge-reuse/PAPER.md) | `aadd6e7ecfb43e5fa912ec81adb5f367ee167397b5ce603d2fd0848d89d21ea4` | absent | absent |
| 9 | `paper` | [`knowledge-utility`](../../papers/knowledge-utility/PAPER.md) | `e807eacfe0c69620457232e00a1f09edb1e9753493e5f5478f8bdfa7e05c73e1` | absent | absent |
| 10 | `specification` | [`knowledge-contract-core`](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md) | `81cb01a8326eaeb0c14e929609c52cc85e5a344c61f3744d2e0def228cdc60d5` | author-draft | author-draft |
| 11 | `specification` | [`contract-family`](../../engineering/specifications/contract-family/SPECIFICATION.md) | `310cd3f151275739a2391d2c8d8b7c23ad64b46f4c1a56717f7f0975866f60c8` | author-draft | author-draft |
| 12 | `specification` | [`semantic-types`](../../engineering/specifications/semantic-types/SPECIFICATION.md) | `4428c3cdacfe5e8bcf00b8d9100a79f5ce9691edecd914063698bfb3f97e8f6f` | author-draft | author-draft |
| 13 | `specification` | [`context-package`](../../engineering/specifications/context-package/SPECIFICATION.md) | `5bba82777b44dc0cf6b1b0c218292c1476c0271806acef195db6c3b8a9448e41` | author-draft | author-draft |
| 14 | `specification` | [`compiled-artifact-contract`](../../engineering/specifications/compiled-artifact-contract/SPECIFICATION.md) | `2cc5e781565136b5ad9fdbb2facae47d58564b1e300173d0a91a2c6cf16d5a82` | author-draft | author-draft |
| 15 | `specification` | [`artifact-registry`](../../engineering/specifications/artifact-registry/SPECIFICATION.md) | `ec6584f97c5160fd3c8b17a5036aaeb8d302bf86dd61e567f2c5d858e9159470` | author-draft | author-draft |
| 16 | `specification` | [`status-model`](../../engineering/specifications/status-model/SPECIFICATION.md) | `2f66342472fc4198eba573d7d1eda5d58d5bae9de904f901f5094037dd628d0a` | author-draft | author-draft |
| 17 | `specification` | [`cache-identity-and-invalidation`](../../engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) | `742982eabd0d797ccc5bba4c8472d25a4236c84baed21281f13a7601a4ce2f39` | author-draft | author-draft |
| 18 | `specification` | [`reuse-policy`](../../engineering/specifications/reuse-policy/SPECIFICATION.md) | `be75f0191414c07a113dafb0c983cd1d1e73834be0b670e0d610b4354f37ecd2` | author-draft | author-draft |
| 19 | `specification` | [`knowledge-evolution`](../../engineering/specifications/knowledge-evolution/SPECIFICATION.md) | `4662bdd76c5716cb7d9b55c1b99e00dda626b34c3565e2f03ceecb61fe15685a` | author-draft | author-draft |
| 20 | `specification` | [`book-package`](../../engineering/specifications/book-package/SPECIFICATION.md) | `1ce2ce4fa9e0e2647b3472f1da0a250fa3abae00c78b7518d3497f106c09722c` | author-draft | author-draft |
| 21 | `study` | [`contract-profile-conformance`](../../engineering/studies/contract-profile-conformance/STUDY.md) | `788c09269946b294420024f28656ef616e2df056e4d8246bfdf67c69ca4434a9` | absent | absent |
| 22 | `study` | [`dependency-closure-and-package-delivery`](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) | `0012f1506d1c9e95b29e7f8916952d2278e791bc2a7f7153e8c3c5980928f66a` | absent | absent |
| 23 | `study` | [`source-transcription-and-uncertainty`](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) | `6119790ada666b76782c0952e12e47799c51893a85f71a7e36f72d9ac44f3fe0` | absent | absent |
| 24 | `study` | [`executable-projections-and-revision`](../../engineering/studies/executable-projections-and-revision/STUDY.md) | `6242027572df695e1907e77d55588ea3b3a64741407b6922b87f0612de956ed8` | absent | absent |
| 25 | `study` | [`reuse-admission-and-cost-controls`](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) | `fa5494d6609d15a61ce071eb39c3a87fa0b982c61f756f3308276c127ae8484a` | absent | absent |
| 26 | `study` | [`editorial-skill-pilot`](../../engineering/studies/editorial-skill-pilot/STUDY.md) | `59066d54a219c13214a113037b0f3257378d77c83105b755bc80251db51ae0d5` | absent | absent |
| 27 | `glossary` | [`glossary`](../../reference/glossary/GLOSSARY.md) | `5147262a4739b194cd1712d04f3b205ad701c77f7c214ba7cfb68094d12ddabb` | author-draft | author-draft |
| 28 | `bibliography` | [`bibliography`](../../reference/bibliography/BIBLIOGRAPHY.md) | `bbfc162fcb52b74abefad92d0cda0f72cacc77ff1a697dfc685d5380b8cf457d` | absent | absent |
| 29 | `appendix` | [`source-map`](../../appendices/source-map/APPENDIX.md) | `eca6631650eb303aa5451eb3f173ce82cd06d73c2184ed460abe65188c61f25c` | absent | absent |
| 30 | `appendix` | [`api-integration`](../../appendices/api-integration/APPENDIX.md) | `2e1c800cf2bb1c61696e34d516b23db1f3f65fa7c58f983bf3124c17854cefe3` | absent | absent |

## Translation workflow and decision boundaries

1. **Author:** KC-Brain. Translate complete original work: title, abstract, metadata, claims, premises, qualifications, proofs, tables, captions, annexes, references and all substantive paragraphs. Keep exact BCP 14 modality, negation, quantification, exception and uncertainty. Preserve the original mathematical expressions, code/schema identifiers, requirement IDs, units and numbers. Explicitly bind each target to the original path, commit and blob. Keep original English bibliography titles recoverable.
2. **Structural checks:** compare source and target section mapping, heading anchors, table-row cardinalities, requirement IDs, literal code tokens, formulas, reference targets, anchors and non-translatable keys. Detect skipped/duplicated body segments and stale pins; these checks cannot establish semantic equivalence by themselves. A fallback to English must be visibly labelled and must not masquerade as full translation.
3. **Scientific review:** Agent-Brain independently examines the exact translation bytes against the pinned original, paying particular attention to necessary versus sufficient conditions, quantifier scope, exception tails, proof dependencies, and retained claims of NOT_MEASURED. A machine consistency PASS is not external peer review or native-speaker certification.
4. **Publication:** KC-SWE implements separately reviewed, versioned source/rendition admission through the existing K8 work item `b2ffbd14-85c6-4ff7-a183-b7e411a6cdb2`. The source and review mapping remain in `knowledge-contract`; `contract-place-site` consumes an exact approved commit and derives localized HTML and provenance. Preserve byte-identical current output when no accepted renditions exist; keep publication, index admission and executable authority separate.
5. **Link resolution is not finished in this snapshot.** Mirrored Markdown currently retains source relative links (e.g. `../../../schemas/book-package.schema.json` inside `translations/ru/engineering/specifications/book-package/`). Such a target can resolve under `translations/ru/schemas/` instead of the canonical `schemas/`. Likewise links to yet-untranslated sibling texts may not resolve. The site compiler or the authored source paths must distinguish invariant repository artifacts from localized sibling-document routes; until explicit link validation this is an **open defect**, not a link-check PASS. Do not blindly prepend traversal to links meant for a translated sibling.

## First bounded scientific manuscript pilot

Choose the already merged `papers/revision-and-governance/PAPER.md`, source SHA-256 `20079132357dc2e4e651cde78d528b37712ecdef030af3934ebd2e8048e3f78a`, as the first **scientific-paper** fidelity pilot. Its scoped English review is recorded in [PR #73](https://github.com/Arcanada-one/knowledge-contract/pull/73) at original head `08a7e5b89ae0806bdf23abb7c68e0949d62a069e`; neither that review nor the 12 already drafted translations is an independent review of new RU/zh-Hans scientific text. Preserve all four proposition premises, five-event distinctions, finite-model limitations and high-level PROV/AGM/Doyle comparisons. No paper translation is delivered by this coverage note.

## Evidence and explicit nonclaims

- [Accepted source](https://github.com/Arcanada-one/knowledge-contract/commit/a0450428704fcd41b411203f2fc88c06c779610b) and [publication provenance](https://github.com/Arcanada-one/contract-place-site/blob/21a15a65be8b7ce2544aac1eb43a929d2043b114/public/content-provenance.json).
- [Current translation proposal #76](https://github.com/Arcanada-one/knowledge-contract/pull/76). The twenty-four draft files and their source pins were inspected at the stated head; for the book-package, knowledge-contract-core and status-model source/target pairs, the producer checked heading counts, table-row counts, requirement identifiers, inline math, code spans and original Markdown target strings, with no missing counts in those limited comparisons. **Original target-string identity does not prove that relative links resolve from a new nested translation path.** Semantic truth, complete current corpus, native-speaker review and site live-reading in translated languages were not measured.

This inventory is a working research/publishing record under the repository text licence, not a new article, adoption decision, allowlist, index snapshot, cross-language independent evidence source or authorization to act.
