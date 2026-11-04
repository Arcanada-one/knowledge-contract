---
name: "source-map"
title: "Source Map, Earlier Editions, and Protocol Compatibility"
artifact: "appendix"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "The migration from the earlier corpus, immutable history, evidence provenance and unchanged protocol versions."
---

# Source Map, Earlier Editions, and Protocol Compatibility

**Publication edition:** 1.0 · **Source audit date:** 4 November 2026

## 1. What this edition changes

The earlier repository contained fourteen short English paper entry pages, fourteen much longer Russian manuscripts, ten English specification entries and ten Russian specification texts. The long texts combined scientific arguments, domain studies, iteration notes and references to supporting records outside the public release.

This edition reorganizes those materials into eight complete English scientific papers, eleven engineering specifications, six engineering studies, a common glossary and bibliography, and two supporting appendices. Scientific results, normative requirements and observations are now separately identifiable. The prior iteration histories remain recoverable at an immutable repository revision instead of appearing as repeated handoff sections in the current reading path.

The exact prior publication snapshot is [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60). The prior site snapshot is [64ddd981296cb65390beecd802f1682618a7f080](https://github.com/Arcanada-one/contract-place-site/tree/64ddd981296cb65390beecd802f1682618a7f080). These references are historical evidence, not aliases for the mutable main branches.

## 2. Scientific crosswalk

| Earlier manuscript | Current scientific home | Material separated into engineering |
| --- | --- | --- |
| Introduction | [Semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) | Publication and implementation inventory |
| Semantic objects and extraction | [Semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) | Source transcription and uncertainty |
| Context and applicability | [Semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) | Dependency graphs and delivery checks |
| Transformations and transfer | [Constrained transformations](../../papers/constrained-transformations/PAPER.md) | Executable projections and revision |
| Query, retrieval and coverage | [Retrieval and context composition](../../papers/retrieval-and-context-composition/PAPER.md) | Package coverage and finite search behavior |
| Budgeted context composition | [Retrieval and context composition](../../papers/retrieval-and-context-composition/PAPER.md) | Actual package sizes and closure replays |
| Dialogue and learning | [Interaction and memory](../../papers/interaction-and-memory/PAPER.md) | Task and revision bindings |
| Reasoning and evidence | [Evidence and falsification](../../papers/evidence-and-falsification/PAPER.md) | Checker trust boundaries and counterexamples |
| Documents and memory | [Interaction and memory](../../papers/interaction-and-memory/PAPER.md) | Readable projections and editorial pilot |
| Work, roles, skills and Knowledge Contract | [Controlled knowledge reuse](../../papers/controlled-knowledge-reuse/PAPER.md) and [revision and governance](../../papers/revision-and-governance/PAPER.md) | Core, artifact registry and contract-profile conformance |
| Revision and canon | [Revision and governance](../../papers/revision-and-governance/PAPER.md) | Versioned rules and executable revision studies |
| Evaluation and falsification | [Evidence and falsification](../../papers/evidence-and-falsification/PAPER.md) | Full retained results, adverse cases and comparator ties |
| Compilation, caching and reuse | [Controlled knowledge reuse](../../papers/controlled-knowledge-reuse/PAPER.md) | Compiled artifacts, invalidation and reuse policy |
| Knowledge utility and resource economics | [Knowledge utility](../../papers/knowledge-utility/PAPER.md) | Reuse-admission and cost controls |

The numerical filenames of the earlier edition are retained only as compatibility links. They lead to the current scientific home and to their exact earlier English and Russian texts. Consolidation is topical: it does not silently convert an untested historical proposal into a proved claim. A historical claim not supported by the present argument or evidence remains a historical proposal, accessible in the source snapshot.

## 3. Engineering crosswalk

The ten earlier specification subjects map one-to-one to these current files:

| Earlier subject | Current specification |
| --- | --- |
| Knowledge Contract v3 | [Core model and admission](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md) |
| Contract family | [Knowledge operations](../../engineering/specifications/contract-family/SPECIFICATION.md) |
| Semantic types | [Semantic types and representations](../../engineering/specifications/semantic-types/SPECIFICATION.md) |
| Context package | [Coverage, dependencies and delivery](../../engineering/specifications/context-package/SPECIFICATION.md) |
| Compiled artifact contract | [Compiled artifacts and derivation](../../engineering/specifications/compiled-artifact-contract/SPECIFICATION.md) |
| Artifact registry | [Readable names and document formats](../../engineering/specifications/artifact-registry/SPECIFICATION.md) |
| Status model | [Assessment, execution and publication states](../../engineering/specifications/status-model/SPECIFICATION.md) |
| Cache identity and invalidation | [Identity and invalidation](../../engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) |
| Reuse policy | [Time, authorization and outcomes](../../engineering/specifications/reuse-policy/SPECIFICATION.md) |
| Knowledge evolution contract | [Versioned rules](../../engineering/specifications/knowledge-evolution/SPECIFICATION.md) |

The additional [book-package specification](../../engineering/specifications/book-package/SPECIFICATION.md) incorporates the schema, validator and synthetic fixtures added in upstream revision [570f76b6d9a189295c3229254821c30748383965](https://github.com/Arcanada-one/knowledge-contract/tree/570f76b6d9a189295c3229254821c30748383965), which is the integration base of this edition. Its implemented checks and remaining unmeasured properties are stated separately. All upstream schema, validator and fixture bytes are preserved.

Engineering studies contain the practical domain material, including the historical cooking, navigation and electrical examples. They distinguish publicly replayable procedures from inspectable retained reports and unavailable third-party source corpora. The [evidence index](../../engineering/studies/evidence-index.json) records claim-level support and limits; a navigational link alone is not an empirical justification.

## Protocol compatibility

Publication edition **1.0** identifies this set of documents. It is not a renamed runtime protocol. The following identifiers are preserved where historical records need them:

| Identifier | Actual scope | Compatibility statement |
| --- | --- | --- |
| `3.0.0-draft.1` | Earlier target Knowledge Contract architecture | No stable protocol release is inferred from the editorial edition |
| `kc-synthesis/0.1` | Bounded interpreted-JSON core/profile implementation | Its retained results do not implement all requirements of the current architecture |
| `mm-envelope/0.1` | Common carrier used by the historical registry and examples | The carrier and its 34 artifact types are neither an exhaustive taxonomy of knowledge nor a limit on later contracts |
| `i16-compiled-artifact/0.1` | Bounded compiled-artifact representation | Original observations retain their original profile and validator scope |
| `i17-reuse-policy/0.1` | Bounded time and reuse-policy model | Interval calculations do not constitute production authorization or distributed atomic serving |
| `knowledge-evolution-metadata/0.2-proposal` | Earlier evolution metadata proposal | Publication of architectural requirements does not claim a deployed migration service |

An implementation claiming this edition MUST state which requirements it satisfies and link corresponding evidence. A change of schema, field semantics or wire version requires its own migration and compatibility record. The publication process MUST NOT rewrite retained raw evidence merely to remove historical development labels.

## 5. Provenance and rights

Each study's `evidence/origin.json` identifies the origin, exact output hash and transformation status of its evidence files. An exact recovered JSON is distinguished from a readable prose view reconstructed from retained HTML. The latter does not claim to reproduce unavailable original Markdown bytes.

Third-party books, page images and OCR corpora are not redistributed here. The current arguments are self-contained; publicly runnable examples use original synthetic data or metadata-only graphs. Restricted source access limits independent reproduction of the corresponding historical experiments, and the studies state that limit at the claim it affects.

Project text remains [CC BY 4.0](../../LICENSE); code remains [Apache-2.0](../../LICENSE-CODE). The current [source register](../../SOURCES.md) replaces the earlier catch-all description for the new edition with named primary works and explicit document coverage.

## 6. Reading and citation

Cite a paper by its human-readable title, author, publication edition and immutable revision or released DOI when one actually exists. No DOI is invented for this edition. Use the paper for its argument, the specification for a requirement, and the study or exact evidence record for an observation. The [glossary](../../reference/glossary/GLOSSARY.md) resolves shared terms without repeating the full definitions in every article.

## 7. Internal review and verification

The [publication review](../../reviews/publication-integrity/REVIEW.md) records the actual scientific and evidence reviews, exact input identities, integration corrections, local checks and unperformed release checks. It distinguishes internal content acceptance from external peer review and from the separate repository, website and corpus-admission outcomes.
