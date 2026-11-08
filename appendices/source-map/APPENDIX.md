---
name: "source-map"
title: "Source History: Source Map, Earlier Editions, and Protocol Compatibility"
short_title: "Source History"
subtitle: "Source Map, Earlier Editions, and Protocol Compatibility"
previous_title: "Source Map, Earlier Editions, and Protocol Compatibility"
artifact: "appendix"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "The migration from the earlier corpus, immutable history, evidence provenance and explicit protocol compatibility boundaries."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="source-map-earlier-editions-and-protocol-compatibility"></a>

# Source History: Source Map, Earlier Editions, and Protocol Compatibility

**Publication edition:** 1.1 · **Source audit date:** 4 November 2026

## 1. What this edition changes

The earlier repository contained fourteen short English paper entry pages, fourteen much longer Russian manuscripts, ten English specification entries and ten Russian specification texts. The long texts combined scientific arguments, domain studies, iteration notes and references to supporting records outside the public release.

This edition reorganizes those materials into eight complete English scientific papers, eleven engineering specifications, six engineering studies, a common glossary and bibliography, and two supporting appendices. Scientific results, normative requirements and observations are now separately identifiable. The prior iteration histories remain recoverable at an immutable repository revision instead of appearing as repeated handoff sections in the current reading path.

The exact prior publication snapshot is [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60). The prior site snapshot is [64ddd981296cb65390beecd802f1682618a7f080](https://github.com/Arcanada-one/contract-place-site/tree/64ddd981296cb65390beecd802f1682618a7f080). These references are historical evidence, not aliases for the mutable main branches.

The independent review addressed published edition 1.0 at [ed2e188c89a1a50a187f3d55bf32baab54c87f7e](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e). Corrections are made from that immutable base. Historical evidence and its origin hashes remain unchanged; corrected interpretations and new finite checks have their own records. The current documents identify the stronger premises needed by the formal results, the actual scope of the observations, and the breaking book-package profile described below.

## 2. Scientific crosswalk

| Earlier manuscript | Current scientific home | Material separated into engineering |
| --- | --- | --- |
| Introduction | [Semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) | [Publication inventory](../../publication-catalog.json) and [API interface boundaries](../api-integration/APPENDIX.md#2-documented-public-interface); no inventory establishes implementation conformance |
| Semantic objects and extraction | [Semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) | [Source transcription and uncertainty](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) |
| Context and applicability | [Semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) | [Declared dependency graphs and finite delivery checks](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) |
| Transformations and transfer | [Constrained transformations](../../papers/constrained-transformations/PAPER.md) | [Executable projections and revision](../../engineering/studies/executable-projections-and-revision/STUDY.md) |
| Query, retrieval and coverage | [Retrieval and context composition](../../papers/retrieval-and-context-composition/PAPER.md) | [Coverage and delivery requirements](../../engineering/specifications/context-package/SPECIFICATION.md); no finite retrieval-search performance study is claimed |
| Budgeted context composition | [Retrieval and context composition](../../papers/retrieval-and-context-composition/PAPER.md) | [Delivered record counts and fault controls](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md#delivered-record-counts-and-fault-controls); these are graph records, not measured token or byte costs |
| Dialogue and learning | [Interaction and memory](../../papers/interaction-and-memory/PAPER.md) | [Operation and task bindings](../../engineering/specifications/contract-family/SPECIFICATION.md#2-common-contract-record) and [targeted revision cases](../../engineering/studies/executable-projections-and-revision/STUDY.md#targeted-revision-and-a-strong-alternative); no longitudinal dialogue or learning study |
| Reasoning and evidence | [Evidence and falsification](../../papers/evidence-and-falsification/PAPER.md) | [Checker trust boundaries and counterexamples](../../engineering/studies/contract-profile-conformance/STUDY.md#counterexamples-and-the-comparator) |
| Documents and memory | [Interaction and memory](../../papers/interaction-and-memory/PAPER.md) | [Readable projection audit](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) and [single-section editorial pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) |
| Work, roles, skills and Knowledge Contract | [Controlled knowledge reuse](../../papers/controlled-knowledge-reuse/PAPER.md) and [revision and governance](../../papers/revision-and-governance/PAPER.md) | [Core](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md), [artifact registry](../../engineering/specifications/artifact-registry/SPECIFICATION.md) and [profile conformance](../../engineering/studies/contract-profile-conformance/STUDY.md) |
| Revision and canon | [Revision and governance](../../papers/revision-and-governance/PAPER.md) | [Versioned-rule requirements](../../engineering/specifications/knowledge-evolution/SPECIFICATION.md) and [bounded addressed revision observations](../../engineering/studies/executable-projections-and-revision/STUDY.md#targeted-revision-and-a-strong-alternative) |
| Evaluation and falsification | [Evidence and falsification](../../papers/evidence-and-falsification/PAPER.md) | [Claim–evidence index](../../engineering/studies/evidence-index.json), [ordinary versus boundary counts](../../engineering/studies/README.md#counting-and-interpretation), and [comparator tie](../../engineering/studies/contract-profile-conformance/STUDY.md#counterexamples-and-the-comparator) |
| Compilation, caching and reuse | [Controlled knowledge reuse](../../papers/controlled-knowledge-reuse/PAPER.md) | [Compiled-artifact requirements](../../engineering/specifications/compiled-artifact-contract/SPECIFICATION.md), [invalidation](../../engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) and [reuse policy](../../engineering/specifications/reuse-policy/SPECIFICATION.md); no deployed generation or idempotence experiment |
| Knowledge utility and resource economics | [Knowledge utility](../../papers/knowledge-utility/PAPER.md) | [Synthetic admission checks and analytical costs](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md); no measured production cost benefit |

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

The additional [book-package specification](../../engineering/specifications/book-package/SPECIFICATION.md) originated with the schema, validator and synthetic fixtures added in upstream revision [570f76b6d9a189295c3229254821c30748383965](https://github.com/Arcanada-one/knowledge-contract/tree/570f76b6d9a189295c3229254821c30748383965). Edition 1.0 preserved those upstream bytes. The current correction defines the breaking **`book-package/2`** profile and **`KCBook*/v2`** records: review results bind to their actual subject, scope and criteria; rights classification constrains permissible licensing and export; readiness follows the complete declared state rules. This is an explicit format change, not a silent reinterpretation of historical `v1` records.

The last reviewed `v1` implementation remains available at [ed2e188c89a1a50a187f3d55bf32baab54c87f7e](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e). A consumer MUST identify the profile and schema versions it accepts. Conversion to `v2` requires a new identified record and any missing assessment evidence; renaming a schema token MUST NOT turn an old review, rights assertion or status into a newly established fact. No automatic reassessment or corpus-admission change is performed by publishing these documents.

Engineering studies contain the practical domain material, including the historical cooking, navigation and electrical examples. They distinguish publicly replayable procedures from inspectable retained reports and unavailable third-party source corpora. The [evidence index](../../engineering/studies/evidence-index.json) records claim-level support and limits; a navigational link alone is not an empirical justification.

## 4. Protocol compatibility

Publication edition **1.0** identifies the original reviewed set of documents; the current publication's edition is stated in its catalogue and metadata. Neither is a renamed runtime protocol. The following identifiers are preserved where historical records need them. Capitalized requirements use [BCP 14](../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language).

| Identifier | Actual scope | Compatibility statement |
| --- | --- | --- |
| `3.0.0-draft.1` | Earlier target Knowledge Contract architecture | No stable protocol release is inferred from the editorial edition |
| `kc-synthesis/0.1` | Bounded interpreted-JSON core/profile implementation | Its retained results do not implement all requirements of the current architecture |
| `mm-envelope/0.1` | Common carrier used by the historical registry and examples | The carrier and its 34 artifact types are neither an exhaustive taxonomy of knowledge nor a limit on later contracts |
| `i16-compiled-artifact/0.1` | Bounded compiled-artifact representation | Original observations retain their original profile and validator scope |
| `i17-reuse-policy/0.1` | Bounded time and reuse-policy model | Interval calculations do not constitute production authorization or distributed atomic serving |
| `knowledge-evolution-metadata/0.2-proposal` | Earlier evolution metadata proposal | Publication of architectural requirements does not claim a deployed migration service |
| Knowledge Contract admission runtime | Service that decides admission under its explicitly advertised profiles and policies | No stable deployed runtime version is established by this publication; an operator MUST supply its actual implementation and profile identities when claiming conformance |
| `kc2_admission` | Legacy book-record field name | It is not a runtime or protocol version. Its presence does not establish admission, and the publication does not rename it to imply a new runtime |
| `KCBook*/v1` | Book records in the immutable edition-1.0 base | Historical schema behavior remains auditable at `ed2e188c89a1a50a187f3d55bf32baab54c87f7e`; conversion does not retroactively validate it |
| `book-package/2`, `KCBook*/v2` | Current corrected book representation and validator profile | Breaking fields and decisions require explicit migration and fresh evidence where absent; they do not identify the admission runtime |

An implementation claiming this edition MUST state which requirements it satisfies and link corresponding evidence. A change of schema, field semantics or wire version requires its own migration and compatibility record. The publication process MUST NOT rewrite retained raw evidence merely to remove historical development labels.

## 5. Provenance and rights

Each study's `evidence/origin.json` identifies the origin, exact output hash and transformation status of its evidence files. An exact recovered JSON is distinguished from a readable prose view reconstructed from retained HTML. The latter does not claim to reproduce unavailable original Markdown bytes.

Third-party books, page images and OCR corpora are not redistributed here. The current arguments are self-contained; publicly runnable examples use original synthetic data or metadata-only graphs. Restricted source access limits independent reproduction of the corresponding historical experiments, and the studies state that limit at the claim it affects.

Project text remains [CC BY 4.0](../../LICENSE); code remains [Apache-2.0](../../LICENSE-CODE). The current [source register](../../SOURCES.md) replaces the earlier catch-all description for the new edition with named primary works and explicit document coverage.

## 6. Reading and citation

Cite a paper by its human-readable title, author, publication edition and immutable revision or released DOI when one actually exists. No DOI is invented for this edition. Use the paper for its argument, the specification for a requirement, and the study or exact evidence record for an observation. The [glossary](../../reference/glossary/GLOSSARY.md) resolves shared terms without repeating the full definitions in every article.

## 7. Internal review and verification

The [publication review](../../reviews/publication-integrity/REVIEW.md) records the actual scientific and evidence reviews, exact input identities, integration corrections, local checks and unperformed release checks. It distinguishes internal content acceptance from external peer review and from the separate repository, website and corpus-admission outcomes.
