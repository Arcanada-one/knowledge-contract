# Knowledge Contract Arcana

Read [all 30 document names](DOCUMENTS.md), the [complete roadmap](ROADMAP.md), the [Russian roadmap](roadmap/ROADMAP.ru.md), and the [naming canon](reference/document-naming/NAMING.md). Short names precede explanatory subtitles; established paths and historical revisions remain stable. Engineering execution is currently paused; the roadmap separates authoring from later site integration.

**Formal foundations, engineering specifications, and evidence for using knowledge under explicit conditions.**

Knowledge Contract connects a body of knowledge to its intended use, sources, dependencies, constraints and assessment. It helps a person or agent distinguish what a source says, what is supported, what applies to the task, and what may be done with it.

## Read the publication

Publication edition **1.1** contains English scientific and engineering documents with a shared vocabulary and traceable supporting records. It incorporates the review of edition 1.0; the [correction record](reviews/edition-corrections/REVIEW.md) identifies the changes, verification and remaining limits.

| Section | Contents | Start here |
| --- | --- | --- |
| Science | Eight baseline papers plus the proposed foundations introduction: models, conditional results, proofs, counterexamples and limits | [Scientific papers](papers/README.md) |
| Engineering specifications | Eleven specifications defining obligations and conformance boundaries | [Specifications](engineering/specifications/README.md) |
| Engineering studies | Six studies with actual results, adverse cases and public reproduction procedures | [Studies and evidence](engineering/studies/README.md) |
| Reference | Preferred terms, Russian and Simplified Chinese equivalents, and primary sources | [Shared Vocabulary](reference/glossary/GLOSSARY.md) · [Research Foundations](reference/bibliography/BIBLIOGRAPHY.md) |
| Appendices | Source migration, earlier editions, protocol compatibility and API integration | [Appendices](appendices/README.md) |

The [website](https://contract.place/) is the reading surface. This repository provides the source, evidence and history. Its [publication catalogue](publication-catalog.json) proposes 30 reading entries: the 29 baseline documents and the new foundations research draft; short files at earlier addresses preserve citation continuity. The full earlier Russian manuscripts remain available at the immutable revisions in the [Source History](appendices/source-map/APPENDIX.md).

## Start with the human-to-computational foundation

[Meaning Bridge](papers/human-meaning-and-computable-knowledge/PAPER.md) explains the passage from a contextual expression to a representation, an artifact and a particular permitted use. It includes an ordinary rule-and-exception example, an exact representation-adequacy argument and explicit limitations. The [foundations map](reference/foundations/README.md) connects its sections to existing definitions, specifications and evidence, with a terminology and source supplement.

The new manuscript is a **research draft proposed for integration**. Its catalogue entry does not assert independent review, a new released edition, deployment or corpus-index admission. Existing publication and raw-evidence histories remain unchanged.

## What the work establishes

The scientific papers give explicit models and conditional arguments for preserving meaning, composing context, keeping assessments tied to their subjects, and controlling reuse. The engineering studies report what was actually observed on finite inputs. They preserve false trusted-input acceptances, baseline ties and unmeasured quantities rather than concealing them behind a global success claim.

Four retained public Python procedures reproduce the edition-1.0 examples and checks within their recorded scope. Three separately identified corrected procedures test dependency-closure sizes and implementation mutations, projection against actual source bytes, and every mandatory admission gate with complete cost accounting. The [study correction register](engineering/studies/review-corrections.json) explains the difference. These procedures do not reconstruct missing historical model runs. The [claim–evidence index](engineering/studies/evidence-index.json) links 24 specific claims to records, counterarguments and limitations; the [historical recovery inventory](engineering/studies/historical-recovery-gaps.json) records the exact recovered input and the programs and fixtures still missing.

This evidence does not establish universal extraction accuracy, general agent superiority, or production readiness of every specified operation. Internal agent review and external peer review are different forms of assessment; review records state which was performed. A complete publication can make a bounded result precise without claiming that every empirical question is settled.

## Constraints and agent artifacts

Constraints are explicit contract obligations, separate from output acceptance criteria and current authority. The [Contract Core](engineering/specifications/knowledge-contract-core/SPECIFICATION.md#3-constraints-are-first-class-obligations) defines their role. The [Artifact Registry](engineering/specifications/artifact-registry/SPECIFICATION.md) specifies readable folders and canonical files for roles, skills, competencies, blueprints, constraints and Work Items. [AGENTS.md](AGENTS.md) tells current coding agents where the canonical documents live and how to verify changes.

## Service and publication versions

The API and MCP surface provides machine access to the project. The [Publication Interfaces](appendices/api-integration/APPENDIX.md) distinguishes the documented read interfaces from the requirements for delivering a ready task-specific contract. Document edition, wire profile, service build and index snapshot have separate identities. The site is built from an exact source commit and shows when a search result belongs to a different indexed revision.

The reading catalogue does not bypass the [corpus publication decisions and allowlist](corpus/README.md). New content, its admission decision and index promotion retain their separate checks. [Publishing instructions](PUBLISHING.md) describe the concrete release sequence and readback requirements.

## Use, cite and contribute

The project is authored by **Pavel Valentov**. Cite the specific paper, specification or study title, edition and immutable source revision; see [CITATION.cff](CITATION.cff) and [attribution](ATTRIBUTION.md).

Text and documentation use [CC BY 4.0](LICENSE). Code and schemas use [Apache-2.0](LICENSE-CODE). Third-party works retain their own rights and are identified in [SOURCES.md](SOURCES.md). The API backend remains private under the established [openness policy](OPENNESS.md).

Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md), including source credit, substantive review and DCO sign-off. Report security concerns through [SECURITY.md](SECURITY.md).
