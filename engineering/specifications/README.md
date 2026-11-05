---
sources: none
---

# Engineering Specifications

Eleven specifications define architectural obligations and bounded implemented profiles. The book-package/2 schema and the observation/change-event exchange subset are executable formats. The remaining architecture requires an explicit implementation profile before two systems can claim wire interoperability. Normative requirements, actual test coverage and historical wire versions remain separate.

| Document | Subject |
| --- | --- |
| [Knowledge Contract: Core Model and Admission Requirements](knowledge-contract-core/SPECIFICATION.md) | The nine core groups, first-class constraints, profiles, admission and execution requirements. |
| [Contracts for Knowledge Operations](contract-family/SPECIFICATION.md) | Common preconditions, invariants, postconditions, effects and evidence for knowledge operations. |
| [Semantic Types, Attribution, and Representations](semantic-types/SPECIFICATION.md) | Semantic facets, attribution, scoped operators, ambiguous readings and multimodal representations. |
| [Context Packages: Coverage, Dependencies, and Delivery](context-package/SPECIFICATION.md) | Requirements for selected context, coverage, mandatory dependencies, budgets and observed delivery. |
| [Compiled Knowledge Artifacts and Reproducible Derivation](compiled-artifact-contract/SPECIFICATION.md) | Saved derivatives with exact inputs, recipes, dependency manifests, templates and output evidence. |
| [Artifact Registry, Readable Names, and Document Formats](artifact-registry/SPECIFICATION.md) | Readable artifact names, canonical Markdown formats, identity rules and professional artifact distinctions. |
| [Assessment, Execution, and Publication States](status-model/SPECIFICATION.md) | Independent assessment, execution, effect, freshness, publication and review states. |
| [Cache Identity, Dependency Tracking, and Invalidation](cache-identity-and-invalidation/SPECIFICATION.md) | Content, build and lookup identity, dependency changes and guarded publication and serving. |
| [Reuse Policy: Time, Authorization, and Decision Outcomes](reuse-policy/SPECIFICATION.md) | Temporal modes, conservative deadlines, authorization, decision outcomes and retention boundaries. |
| [Knowledge Evolution and Versioned Rules](knowledge-evolution/SPECIFICATION.md) | Versioned creation rules, adoption, impact analysis, reassessment, migration and coherent publication. |
| [Book Packages: Source Identity, Semantic Layers, and Validation](book-package/SPECIFICATION.md) | Source binding, reversible conversion, semantic layers, rights and implemented synthetic conformance checks. |

[Publication home](../../README.md) · [Shared glossary](../../reference/glossary/GLOSSARY.md)

The [requirement register](requirements.json) identifies each capitalized requirement with a stable ID, document location and available verification reference. An empty automated-test list means the requirement still needs implementation-specific evidence; it is not a passed check.
