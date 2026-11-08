---
title: "Translation Coverage: Full-body publication progress"
sources: none
status: "author inventory; not a publication or fidelity decision"
---

# Translation Coverage: Full-body publication progress

## Current snapshot — 8 November 2026

Translation-content revision: `19b83712decdef7ef1cb8e7a37487f247d979c4c`, in the existing [translation proposal PR76](https://github.com/Arcanada-one/knowledge-contract/pull/76). Both locale trees were read completely with `truncated=false`: Russian tree `6910d3ea54feda507a5cc01536df4b282c12a5da` and Simplified Chinese tree `4acfae8a68b9181c2ffb8b4d6368bc93ffdea1eb`. This is the current coverage entry point. [The earlier edition coverage audit](EDITION-1.1-COVERAGE.md) remains a dated historical snapshot with its original hashes and verification limits; its older 26-target total is not the current total.

The denominator is **30 canonical works × 2 target languages = 60 full target documents**. Complete intended author-draft bodies are present for **15 works in Russian and 15 in Simplified Chinese: 30/60 targets**. **15 works per language, or 30 targets, remain unwritten in this proposal.** This is a file-coverage count, not a claim that all 30 translations have passed separate fidelity review or been published. Website interface prose, navigation labels, explanatory text and source evidence attachments are separate scope, not extra members of this 30-work denominator.

The previous 28-target count described content revision `37c404d2aca47d198d5a2a0c773a9db97fd6eac5`, where KC-Brain added the full Contract Checks study in both languages. Comparing `5f33d506ae17199e6929da462fec29e1cd9e4337` with that revision shows exactly those two added target files and no changes to the previous 26 translation files, canonical English documents or retained evidence. Agent-Brain subsequently added both full Meaning in Context translations in `cf200652fd0bf5c96fd29a002b311b618984a59f`. They are already present in the inspected current tree alongside the Contract Checks pair. The earlier STATUS/PR description failed to count that concurrent addition; this inventory correction does not add, restore, rewrite or re-author any manuscript.

The target bodies retain their exact English source bindings to `a0450428704fcd41b411203f2fc88c06c779610b`. This inventory does not silently retarget them to a newer release. The readable names below follow the separately accepted [name register at 644c83df](https://github.com/Arcanada-one/knowledge-contract/blob/644c83dffbd97d9563d131b388a44c9ddf27b185/DOCUMENTS.md). A translated name is not a translated body, and a new name does not transfer an earlier fidelity verdict to new bytes.

## All thirty works

`Draft` means an intended full target exists in the proposal, not a published rendition. A separately scoped fidelity finding is linked below and does not promote all other targets. `Not authored` means no current full target in this proposal; it does not deny that older historical manuscripts exist.

| Work | Class | Russian full body | Simplified Chinese full body |
| --- | --- | --- | --- |
| Meaning Bridge | Paper | Not authored | Not authored |
| Meaning in Context | Paper | [Draft; scoped fidelity pass](ru/papers/semantic-objects-and-context/PAPER.md) | [Draft; scoped fidelity pass](zh-Hans/papers/semantic-objects-and-context/PAPER.md) |
| Knowledge Transformations | Paper | Not authored | Not authored |
| Context Assembly | Paper | Not authored | Not authored |
| Interaction and Memory | Paper | Not authored | Not authored |
| Evidence and Falsification | Paper | Not authored | Not authored |
| Knowledge Revision | Paper | [Draft](ru/papers/revision-and-governance/PAPER.md) | [Draft](zh-Hans/papers/revision-and-governance/PAPER.md) |
| Knowledge Reuse | Paper | Not authored | Not authored |
| Knowledge Utility | Paper | Not authored | Not authored |
| Contract Core | Specification | [Draft](ru/engineering/specifications/knowledge-contract-core/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/knowledge-contract-core/SPECIFICATION.md) |
| Knowledge Operations | Specification | [Draft](ru/engineering/specifications/contract-family/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/contract-family/SPECIFICATION.md) |
| Semantic Types | Specification | [Draft](ru/engineering/specifications/semantic-types/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/semantic-types/SPECIFICATION.md) |
| Context Package | Specification | [Draft](ru/engineering/specifications/context-package/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/context-package/SPECIFICATION.md) |
| Compiled Knowledge | Specification | [Draft](ru/engineering/specifications/compiled-artifact-contract/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/compiled-artifact-contract/SPECIFICATION.md) |
| Artifact Registry | Specification | [Draft](ru/engineering/specifications/artifact-registry/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/artifact-registry/SPECIFICATION.md) |
| Status Model | Specification | [Draft](ru/engineering/specifications/status-model/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/status-model/SPECIFICATION.md) |
| Cache Validity | Specification | [Draft](ru/engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) |
| Reuse Policy | Specification | [Draft](ru/engineering/specifications/reuse-policy/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/reuse-policy/SPECIFICATION.md) |
| Knowledge Evolution | Specification | [Draft](ru/engineering/specifications/knowledge-evolution/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/knowledge-evolution/SPECIFICATION.md) |
| Book Packages | Specification | [Draft](ru/engineering/specifications/book-package/SPECIFICATION.md) | [Draft](zh-Hans/engineering/specifications/book-package/SPECIFICATION.md) |
| Contract Checks | Study | [Draft](ru/engineering/studies/contract-profile-conformance/STUDY.md) | [Draft](zh-Hans/engineering/studies/contract-profile-conformance/STUDY.md) |
| Dependency Closure | Study | Not authored | Not authored |
| Uncertainty Preservation | Study | Not authored | Not authored |
| Executable Projections | Study | Not authored | Not authored |
| Reuse Economics | Study | Not authored | Not authored |
| Editorial Pilot | Study | Not authored | Not authored |
| Shared Vocabulary | Glossary | [Draft](ru/reference/glossary/GLOSSARY.md) | [Draft](zh-Hans/reference/glossary/GLOSSARY.md) |
| Research Foundations | Bibliography | Not authored | Not authored |
| Source History | Appendix | Not authored | Not authored |
| Publication Interfaces | Appendix | Not authored | Not authored |

Remaining body authorship per language: **7 papers + 5 studies + 1 bibliography + 2 appendices = 15**. Existing targets additionally need their applicable exact-byte fidelity dispositions, source-version reconciliation and controlled publication. These stages are not included in the count of unwritten bodies.

## Meaning in Context — separate exact-body review

Agent-Brain authored the [Russian](ru/papers/semantic-objects-and-context/PAPER.md) and [Simplified Chinese](zh-Hans/papers/semantic-objects-and-context/PAPER.md) targets and the [alignment record](SEMANTIC-OBJECTS-AND-CONTEXT-2026-11-08.md). KC-Brain then read the complete source, both complete targets and that record and published the separate [SCOPED PASS](https://github.com/Arcanada-one/knowledge-contract/pull/76#issuecomment-6724788904).

| Subject | Exact Git blob |
| --- | --- |
| English source at `a0450428:papers/semantic-objects-and-context/PAPER.md` | `7f8ff0bbf965275e17fb8b8ee664972b2a4bd89e` |
| Russian target | `9b292621d95bd986e8bef68f6b47552004343592` |
| Simplified Chinese target | `8800544b98e363ea2602b8b2bb2bf580c7ad3bfa` |
| Translator's alignment record | `6209485399917a2a4245a421aac79663a8f7472d` |

The review found no blocking loss, reversal or strengthening of the substantive claims. It checks attribution versus truth, quantified negation and obligations, justified exemptions and empty requirements, all five proofs and their hypotheses, finite/cyclic closure versus executable acyclicity, unchanged shared assessment semantics, nonempty readings with a fixed consequence relation, complete deterministic backward slices, delivery and empirical limitations. Two Chinese language-polish suggestions are nonblocking because the adjacent formulas and qualifications preserve the intended meaning. This is a separate internal source-reading review, not external peer review, native-speaker certification, a validator/CI run, a K8 admission decision, a merged rendition or a site release.

The targets still carry the older pinned-source title. Reconciliation with the accepted short-name register must identify the narrow title/anchor delta and preserve the reviewed body; it must not silently transfer this verdict to newer English scientific content. There is no need to repeat a full semantic review of byte-identical bodies merely because their surrounding proposal head changes.

## Contract Checks — exact material and retained author controls

The full source study was read at `a0450428`, path `engineering/studies/contract-profile-conformance/STUDY.md`. A local UTF-8 materialization matched the Git blob `c258efb990cc38c48dee21141af1ceec1791e388` and raw SHA-256 `788c09269946b294420024f28656ef616e2df056e4d8246bfdf67c69ca4434a9` exactly (13,947 bytes).

| Target | Git blob | Raw SHA-256 | UTF-8 bytes |
| --- | --- | --- | ---: |
| Russian | `8237877bb67680e4ece8b56b1f0bf96e92dbd226` | `de3a120ede1c9d71e590aa108241d06ed53e5624219996c545867b5f059b379c` | 28,821 |
| Simplified Chinese | `27f4c0daa1b5be6577473da158bdea5a546fa994` | `fdb3e326e061a65ff83ae0799e067ea7a9886f96e3390e0f6bcb56b08d6043a7` | 13,533 |

KC-Brain executed local author-side structural comparisons against those exact source bytes. Both targets retained all **9 heading identities**, **34 body blocks**, **3 mathematical expressions** (2 inline and 1 displayed), **3 tables / 20 table lines including headers and separators**, the exact ordered numeric sequences in every table row, **3 inline-code occurrences** and the exact ordered control-case identifiers. All **13 link destinations** resolve lexically to their original canonical paths, except the explicitly localized already-existing glossary peer. Both files are strict UTF-8 with LF and a final newline. Full connector readback of both committed targets matched the locally computed Git blob identities.

These are retained author preservation controls from the earlier Contract Checks increment, not newly executed tests in this inventory correction, independent semantic review, Pandoc rendering, repository-wide or HTTP link testing, native-speaker certification, a historical experiment rerun or site publication. Lexical path normalization does not prove that a server serves the destination.

The translation explicitly preserves the limits that matter: 35/35 and 26/26 ordinary outcomes are separate from 2/2 and 4/4 accepted false trusted inputs; the strong simple comparator ties at 9/9 after seeing the expected outcomes; the separate control author is in the same session and agent family, not an external replication; the original runners, thirty concrete inputs/oracle and frozen implementation remain missing. The source's paragraph about English summaries is explicitly attributed to the English original rather than made falsely self-referential in a Russian or Chinese rendition. `source_review_state` describes the source only; each target remains `translation_status: author-draft`.

## Publication and next bounded decisions

The English edition is a separate released artifact: source `644c83dffbd97d9563d131b388a44c9ddf27b185`, site `f0de3e6effc18197c868ca72a5f45daa4e913864`, [site PR24](https://github.com/Arcanada-one/contract-place-site/pull/24), [successful deployment 42500456425](https://github.com/Arcanada-one/contract-place-site/actions/runs/42500456425). Its producer reported zero admitted renditions; English fallback routes are not full Russian or Chinese publications. Source merge, site delivery, translation fidelity and API indexing remain distinct observations.

The canonical trilingual glossary was separately merged through [PR80](https://github.com/Arcanada-one/knowledge-contract/pull/80) as `0b284c6cd971566e7fe38d572c86b164c28b27c5`. That resolves the earlier source-merge wait, not the separate deployed-site or full translated-glossary acceptance questions.

KC-Brain owns the remaining full-body translations and content corrections. A reviewer separate from the translator examines exact source/target bytes: Agent-Brain reviews KC-Brain-authored work, and KC-Brain reviews the identified Agent-Brain contribution. KC-SWE consumes only accepted, explicitly pinned inputs in the existing K8 publication line; no authorship, new worker or duplicate task is requested by this inventory. Approved batches may be released incrementally without waiting for every remaining translation or optional scientific extension. The English release does not wait for this inventory to reach 60/60.

This file tracks artifact coverage only. It does not create or close Muneral tasks, provide publication receipts, extend an index allowlist or authorize private effects.
