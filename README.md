# Knowledge Contract Arcana

**Formal foundations, engineering specifications, and evidence for using knowledge under explicit conditions.**

Knowledge Contract connects a body of knowledge to its intended use, sources, dependencies, constraints and assessment. It helps a person or agent distinguish what a source says, what is supported, what applies to the task, and what may be done with it.

## Read the publication

Publication edition **1.0** contains complete English scientific and engineering documents with a shared vocabulary and traceable supporting records.

| Section | Contents | Start here |
| --- | --- | --- |
| Science | Eight papers: models, conditional results, proofs, counterexamples and limits | [Scientific papers](papers/README.md) |
| Engineering specifications | Eleven specifications defining obligations and conformance boundaries | [Specifications](engineering/specifications/README.md) |
| Engineering studies | Six studies with actual results, adverse cases and public reproduction procedures | [Studies and evidence](engineering/studies/README.md) |
| Reference | Preferred terms, Russian equivalents and primary sources | [Glossary](reference/glossary/GLOSSARY.md) · [Bibliography](reference/bibliography/BIBLIOGRAPHY.md) |
| Appendices | Source migration, earlier editions, protocol compatibility and API integration | [Appendices](appendices/README.md) |

The [website](https://contract.place/) is the reading surface. This repository provides the source, evidence and history. Its [publication catalogue](publication-catalog.json) identifies the 29 canonical documents; short files at earlier addresses preserve citation continuity. The full earlier Russian manuscripts remain available at the immutable revisions in the [source map](appendices/source-map/APPENDIX.md).

## What the work establishes

The scientific papers give explicit models and conditional arguments for preserving meaning, composing context, keeping assessments tied to their subjects, and controlling reuse. The engineering studies report what was actually observed on finite inputs. They preserve false trusted-input acceptances, baseline ties and unmeasured quantities rather than concealing them behind a global success claim.

Four public Python procedures reproduce a finite dependency-closure calculation, a synthetic uncertainty-loss counterexample, reuse-admission and cost counterexamples, and structural checks on an editorial pilot. Retained historical reports remain distinguishable from those public replays. The [claim–evidence index](engineering/studies/evidence-index.json) links 24 specific claims to records, counterarguments and limitations.

This evidence does not establish universal extraction accuracy, general agent superiority, or production readiness of every specified operation. Internal agent review and external peer review are different forms of assessment; review records state which was performed. A complete publication can make a bounded result precise without claiming that every empirical question is settled.

## Constraints and agent artifacts

Constraints are explicit contract obligations, separate from output acceptance criteria and current authority. The [core specification](engineering/specifications/knowledge-contract-core/SPECIFICATION.md#3-constraints-are-first-class-obligations) defines their role. The [artifact registry](engineering/specifications/artifact-registry/SPECIFICATION.md) specifies readable folders and canonical files for roles, skills, competencies, blueprints, constraints and Work Items. [AGENTS.md](AGENTS.md) tells current coding agents where the canonical documents live and how to verify changes.

## Service and publication versions

The API and MCP surface provides machine access to the project. The [API integration appendix](appendices/api-integration/APPENDIX.md) distinguishes the documented read interfaces from the requirements for delivering a ready task-specific contract. Document edition, wire profile, service build and index snapshot have separate identities. The site is built from an exact source commit and shows when a search result belongs to a different indexed revision.

The reading catalogue does not bypass the [corpus publication decisions and allowlist](corpus/README.md). New content, its admission decision and index promotion retain their separate checks. [Publishing instructions](PUBLISHING.md) describe the concrete release sequence and readback requirements.

## Use, cite and contribute

The project is authored by **Pavel Valentov**. Cite the specific paper, specification or study title, edition and immutable source revision; see [CITATION.cff](CITATION.cff) and [attribution](ATTRIBUTION.md).

Text and documentation use [CC BY 4.0](LICENSE). Code and schemas use [Apache-2.0](LICENSE-CODE). Third-party works retain their own rights and are identified in [SOURCES.md](SOURCES.md). The API backend remains private under the established [openness policy](OPENNESS.md).

Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md), including source credit, substantive review and DCO sign-off. Report security concerns through [SECURITY.md](SECURITY.md).
