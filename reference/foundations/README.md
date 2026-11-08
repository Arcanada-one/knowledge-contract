---
sources: none
---

# Foundations and corpus relations

This reading and terminology supplement integrates [From Human Meaning to Contract-Governed Knowledge](../../papers/human-meaning-and-computable-knowledge/PAPER.md) with the existing corpus. Its status is a content proposal, not an independent review, a new released edition or an indexing decision. The baseline is the 29 documents at `717c43deb514adc5b40f76837e7ee0fb2da37102`; the proposed catalogue adds one actual manuscript, not placeholders for future works.

## Reading order and relation semantics

Start with the [human-to-computational foundation](../../papers/human-meaning-and-computable-knowledge/PAPER.md), then [semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md), [transformations](../../papers/constrained-transformations/PAPER.md) and [retrieval and context composition](../../papers/retrieval-and-context-composition/PAPER.md). The remaining papers supply evidence, revision, interaction, reuse and resource-accounting boundaries. Specifications state obligations; studies report their own bounded observations.

The introduction explains interfaces, not the truth of all connected claims. **Uses-definition** relies on a target concept; **explains-interface** is explanatory; **operationalized-by** names a specification, not an implemented guarantee; **bounded-example-in** points to a study without expanding its scope. **Terminology-index** and **source-index** are navigation links. A reading cycle is not a circular proof, and none of these edges grants runtime authority. [relations.json](relations.json) contains the same directed map.

## Typed connections

| Source in the foundation | Relation | Target | Boundary |
| --- | --- | --- | --- |
| [Section 4](../../papers/human-meaning-and-computable-knowledge/PAPER.md#4-a-bounded-semantic-bridge) | uses-definition | [Semantic objects, Section 2](../../papers/semantic-objects-and-context/PAPER.md#2-objects-interpretations-and-grounds) | Existing source, interpretation, attribution and grounds definitions are retained. |
| [Section 5.1](../../papers/human-meaning-and-computable-knowledge/PAPER.md#51-more-demanding-uses-need-stronger-preservation) | explains-interface | [Mandatory strengthening](../../papers/semantic-objects-and-context/PAPER.md#proposition-3-mandatory-strengthening-narrows-certified-applicability) | Enlarging observations and requirements are different fixed-semantics comparisons. |
| [Section 5.2](../../papers/human-meaning-and-computable-knowledge/PAPER.md#52-uncertainty-and-conservative-answers) | uses-definition | [Common consequences](../../papers/semantic-objects-and-context/PAPER.md#proposition-4-additional-readings-narrow-common-consequences) | Retained readings are nonempty; their completeness is not established. |
| [Section 6](../../papers/human-meaning-and-computable-knowledge/PAPER.md#6-algebra-and-geometry-have-different-jobs) | explains-interface | [Constrained transformations](../../papers/constrained-transformations/PAPER.md) | Adequate representation and operation-preservation obligations remain distinct. |
| [Section 6](../../papers/human-meaning-and-computable-knowledge/PAPER.md#6-algebra-and-geometry-have-different-jobs) | explains-interface | [Retrieval and context](../../papers/retrieval-and-context-composition/PAPER.md) | Ranking is not coverage, complete delivery or authority. |
| [Section 8](../../papers/human-meaning-and-computable-knowledge/PAPER.md#8-integration-with-the-scientific-and-engineering-corpus) | explains-interface | [Interaction and memory](../../papers/interaction-and-memory/PAPER.md) | Clarification and changed context can alter an interpretation. |
| [Section 9](../../papers/human-meaning-and-computable-knowledge/PAPER.md#9-what-would-challenge-the-framework) | explains-interface | [Evidence and falsification](../../papers/evidence-and-falsification/PAPER.md) | Deduction, illustration and empirical assessment support different conclusions. |
| [Section 3.3](../../papers/human-meaning-and-computable-knowledge/PAPER.md#33-truth-endorsement-and-use) | uses-definition | [Revision and governance](../../papers/revision-and-governance/PAPER.md) | Content identity is not normative adoption. |
| [Section 7](../../papers/human-meaning-and-computable-knowledge/PAPER.md#7-a-worked-rule-from-expression-to-bounded-use) | explains-interface | [Controlled reuse](../../papers/controlled-knowledge-reuse/PAPER.md) | Preparation does not discharge current-use conditions. |
| [Section 8](../../papers/human-meaning-and-computable-knowledge/PAPER.md#8-integration-with-the-scientific-and-engineering-corpus) | explains-interface | [Knowledge utility](../../papers/knowledge-utility/PAPER.md) | Adequacy is not a demonstrated benefit or cost advantage. |
| [Section 4.3](../../papers/human-meaning-and-computable-knowledge/PAPER.md#43-one-bridge-record-several-kinds-of-evidence) | operationalized-by | [Semantic types](../../engineering/specifications/semantic-types/SPECIFICATION.md) | Reuses existing facets; no new wire schema. |
| [Section 7](../../papers/human-meaning-and-computable-knowledge/PAPER.md#7-a-worked-rule-from-expression-to-bounded-use) | operationalized-by | [Core contract](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md) | Source content is separate from admission requirements. |
| [Section 7](../../papers/human-meaning-and-computable-knowledge/PAPER.md#7-a-worked-rule-from-expression-to-bounded-use) | operationalized-by | [Artifact registry](../../engineering/specifications/artifact-registry/SPECIFICATION.md) | Role, Skill, Competency, Blueprint and Constraint do not certify capability. |
| [Section 7](../../papers/human-meaning-and-computable-knowledge/PAPER.md#7-a-worked-rule-from-expression-to-bounded-use) | operationalized-by | [Context packages](../../engineering/specifications/context-package/SPECIFICATION.md) | Required dependencies and usable representations must reach the recipient. |
| [Section 8](../../papers/human-meaning-and-computable-knowledge/PAPER.md#8-integration-with-the-scientific-and-engineering-corpus) | bounded-example-in | [Transcription and uncertainty](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) | Loss of a field is not validation of unrestricted interpretation. |
| [Section 8](../../papers/human-meaning-and-computable-knowledge/PAPER.md#8-integration-with-the-scientific-and-engineering-corpus) | bounded-example-in | [Closure and delivery](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) | Closure depends on the supplied edges, not automatic discovery of meaning. |
| [Section 3](../../papers/human-meaning-and-computable-knowledge/PAPER.md#3-what-is-meant-by-meaning-in-this-framework) | terminology-index | [Shared glossary](../glossary/GLOSSARY.md) | Existing definitions remain authoritative; new local terms are indexed below. |
| [References](../../papers/human-meaning-and-computable-knowledge/PAPER.md#references) | source-index | [Source register](../../SOURCES.md#human-meaning-foundations-supplement) | Attribution is not endorsement or independent validation. |

## Bounded terminology supplement

The [shared glossary](../glossary/GLOSSARY.md) remains the reference for Semantic object, Interpretation, Context, Ground, Applicability, Constraint, Skill, Competency, Capability, Authority and Admission. New terms below point to their actual definitions, not to a second normative schema. Russian and Simplified Chinese equivalents follow the [multilingual terminology policy](../glossary/GLOSSARY.md#multilingual-terminology-policy); they do not broaden the linked English definitions.

| Term | Russian equivalent | Chinese equivalent (zh-Hans) | Definition location and boundary |
| --- | --- | --- | --- |
| Human meaning | Человеческий смысл | 人类意义 | [Section 3.1](../../papers/human-meaning-and-computable-knowledge/PAPER.md#31-working-distinctions-not-a-complete-psychology): contextual expression, understanding and intention; not a scalar or complete computational object. |
| Communicative intention | Коммуникативное намерение | 交际意图 | [Section 3.1](../../papers/human-meaning-and-computable-knowledge/PAPER.md#31-working-distinctions-not-a-complete-psychology): attributed purpose with grounds, not direct access to a mental state. |
| Operationalization | Операционализация | 操作化 | [Section 3.2](../../papers/human-meaning-and-computable-knowledge/PAPER.md#32-from-a-human-abstraction-to-an-operational-criterion): a declared criterion whose relation to the intended concept needs justification. |
| Semantic bridge | Смысловой переход | 语义桥接 | [Section 4](../../papers/human-meaning-and-computable-knowledge/PAPER.md#4-a-bounded-semantic-bridge): source–interpretation–representation–use relationship, not a deployed service. |
| Protected observation | Сохраняемое наблюдение | 受保护观察 | [Section 4.2](../../papers/human-meaning-and-computable-knowledge/PAPER.md#42-representation-profile-and-protected-observations): a function answering a selected question under a fixed model. |
| Representation adequacy | Адекватность представления | 表示充分性 | [Section 4.2](../../papers/human-meaning-and-computable-knowledge/PAPER.md#42-representation-profile-and-protected-observations): recovery of selected observations, not all human meaning. |
| Encoding collision | Совпадение кодировок разных случаев | 编码碰撞 | [Proposition 1](../../papers/human-meaning-and-computable-knowledge/PAPER.md#proposition-1-exact-adequacy-is-equivalent-to-preserving-the-required-distinctions): material loss when merged cases require different observations. |

## Primary-source supplement

The foundation's [eight reference entries](../../papers/human-meaning-and-computable-knowledge/PAPER.md#references) supply its bibliography. Section 2 states what each contributes and what is not inferred. Five newly registered works extend [SOURCES.md](../../SOURCES.md#human-meaning-foundations-supplement): Grice, Shannon, the Cousots, the OWL 2 primer and Bender–Koller. Hoare, PROV-DM and SKOS were already registered. No third-party article text or scan is imported.

The existing [primary bibliography](../bibliography/BIBLIOGRAPHY.md) retains its historical entries and verification date. This linked supplement makes the new references discoverable without presenting all older entries as newly verified. Later consolidation must retain their original scopes and provenance.

## Integration boundary

F01 is a complete manuscript proposed in the reading catalogue. Its anchors and relations can be mechanically checked; its argument needs substantive review. The existing article, specification and study bodies are unchanged. Pending editorial changes in the semantic-object and reuse papers must be reconciled on merge, not reset to the baseline.

The expansion requires the publication-count guard and its tests to recognize nine papers and 30 catalogue documents through the authorized implementation workflow; no check is to be disabled. Decisions, allowlists and deployment remain separate. The site must render the accepted source and actual review status.

[Scientific papers](../../papers/README.md) · [Reference](../README.md) · [Publication home](../../README.md)
