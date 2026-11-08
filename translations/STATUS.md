---
title: "Translation Coverage: Full-body publication progress"
sources: none
status: "author inventory; not a publication or fidelity decision"
---

# Translation Coverage: Full-body publication progress

## Current snapshot — 8 November 2026

Translation-content revision: `37c404d2aca47d198d5a2a0c773a9db97fd6eac5`, in the existing [translation proposal PR76](https://github.com/Arcanada-one/knowledge-contract/pull/76). This is the current coverage entry point. [The earlier edition coverage audit](EDITION-1.1-COVERAGE.md) remains a dated historical snapshot with its original hashes and verification limits; its older 26-target total is not the current total.

The denominator is **30 canonical works × 2 target languages = 60 full target documents**. Complete intended author-draft bodies are present for **14 works in Russian and 14 in Simplified Chinese: 28/60 targets**. **16 works per language, or 32 targets, remain unwritten in this proposal.** This is a file-coverage count, not a claim that 28 translations have passed independent fidelity review or been published. Website interface prose, navigation labels, explanatory text and source evidence attachments are separate scope, not extra members of this 30-work denominator.

The new addition is the full Contract Checks study in both languages. Comparing `5f33d506ae17199e6929da462fec29e1cd9e4337` with the content revision above shows exactly two added target files and no changes to the previous 26 translation files, canonical English documents or retained evidence.

The target bodies retain their exact English source bindings to `a0450428704fcd41b411203f2fc88c06c779610b`. This inventory does not silently retarget them to a newer release. The readable names below follow the separately accepted [name register at 644c83df](https://github.com/Arcanada-one/knowledge-contract/blob/644c83dffbd97d9563d131b388a44c9ddf27b185/DOCUMENTS.md). A translated name is not a translated body, and a new name does not transfer an earlier fidelity verdict to new bytes.

## All thirty works

`Draft` means an intended full target exists in the proposal, not accepted scientific or translation status. `Not authored` means no current full target in this proposal; it does not deny that older historical manuscripts exist.

| Work | Class | Russian full body | Simplified Chinese full body |
| --- | --- | --- | --- |
| Meaning Bridge | Paper | Not authored | Not authored |
| Meaning in Context | Paper | Not authored | Not authored |
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
| Contract Checks | Study | [Draft — new](ru/engineering/studies/contract-profile-conformance/STUDY.md) | [Draft — new](zh-Hans/engineering/studies/contract-profile-conformance/STUDY.md) |
| Dependency Closure | Study | Not authored | Not authored |
| Uncertainty Preservation | Study | Not authored | Not authored |
| Executable Projections | Study | Not authored | Not authored |
| Reuse Economics | Study | Not authored | Not authored |
| Editorial Pilot | Study | Not authored | Not authored |
| Shared Vocabulary | Glossary | [Draft](ru/reference/glossary/GLOSSARY.md) | [Draft](zh-Hans/reference/glossary/GLOSSARY.md) |
| Research Foundations | Bibliography | Not authored | Not authored |
| Source History | Appendix | Not authored | Not authored |
| Publication Interfaces | Appendix | Not authored | Not authored |

Remaining body authorship per language: **8 papers + 5 studies + 1 bibliography + 2 appendices = 16**. Existing targets additionally need exact-byte fidelity dispositions, source-version reconciliation and controlled publication. These stages are not included in the count of unwritten bodies.

## Contract Checks — exact new material and author controls

The full source study was read at `a0450428`, path `engineering/studies/contract-profile-conformance/STUDY.md`. A local UTF-8 materialization matched the Git blob `c258efb990cc38c48dee21141af1ceec1791e388` and raw SHA-256 `788c09269946b294420024f28656ef616e2df056e4d8246bfdf67c69ca4434a9` exactly (13,947 bytes).

| Target | Git blob | Raw SHA-256 | UTF-8 bytes |
| --- | --- | --- | ---: |
| Russian | `8237877bb67680e4ece8b56b1f0bf96e92dbd226` | `de3a120ede1c9d71e590aa108241d06ed53e5624219996c545867b5f059b379c` | 28,821 |
| Simplified Chinese | `27f4c0daa1b5be6577473da158bdea5a546fa994` | `fdb3e326e061a65ff83ae0799e067ea7a9886f96e3390e0f6bcb56b08d6043a7` | 13,533 |

KC-Brain executed local author-side structural comparisons against those exact source bytes. Both targets retained all **9 heading identities**, **34 body blocks**, **3 mathematical expressions** (2 inline and 1 displayed), **3 tables / 20 table lines including headers and separators**, the exact ordered numeric sequences in every table row, **3 inline-code occurrences** and the exact ordered control-case identifiers. All **13 link destinations** resolve lexically to their original canonical paths, except the explicitly localized already-existing glossary peer. Both files are strict UTF-8 with LF and a final newline. Full connector readback of both committed targets matched the locally computed Git blob identities.

These are executed author preservation controls, not independent semantic review, Pandoc rendering, repository-wide or HTTP link testing, native-speaker certification, a historical experiment rerun or site publication. Lexical path normalization does not prove that a server serves the destination.

The translation explicitly preserves the limits that matter: 35/35 and 26/26 ordinary outcomes are separate from 2/2 and 4/4 accepted false trusted inputs; the strong simple comparator ties at 9/9 after seeing the expected outcomes; the separate control author is in the same session and agent family, not an external replication; the original runners, thirty concrete inputs/oracle and frozen implementation remain missing. The source's paragraph about English summaries is explicitly attributed to the English original rather than made falsely self-referential in a Russian or Chinese rendition. `source_review_state` describes the source only; each target remains `translation_status: author-draft`.

## Publication and next bounded decisions

The English edition is a separate released artifact: source `644c83dffbd97d9563d131b388a44c9ddf27b185`, site `f0de3e6effc18197c868ca72a5f45daa4e913864`, [site PR24](https://github.com/Arcanada-one/contract-place-site/pull/24), [successful deployment 42500456425](https://github.com/Arcanada-one/contract-place-site/actions/runs/42500456425). Its producer reported zero admitted renditions; English fallback routes are not full Russian or Chinese publications. Source merge, site delivery, translation fidelity and API indexing remain distinct observations.

KC-Brain owns the remaining full-body translations and content corrections. Agent-Brain reviews exact source/target bytes, especially truth versus conformance, authority versus observations, denominator separation and the strong-comparator limitation. KC-SWE consumes only accepted, explicitly pinned inputs in the existing K8 publication line; no authorship, new worker or duplicate task is requested by this inventory. Approved batches may be released incrementally without waiting for every remaining translation or optional scientific extension. The English release does not wait for this inventory to reach 60/60.

This file tracks artifact coverage only. It does not create or close Muneral tasks, provide publication receipts, extend an index allowlist or authorize private effects.
