---
name: "artifact-registry"
title: "Artifact Registry: Artifact Registry, Readable Names, and Document Formats"
short_title: "Artifact Registry"
subtitle: "Artifact Registry, Readable Names, and Document Formats"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Readable artifact names, canonical Markdown formats, identity rules and professional artifact distinctions."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="artifact-registry-readable-names-and-document-formats"></a>

# Artifact Registry: Artifact Registry, Readable Names, and Document Formats

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

The registry gives humans and agents a predictable way to find, interpret and revise artifacts. It separates the identity of an object from its title, revision, file representation and current assessment. A new technical term does not automatically require a new database table or service.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). The formats below are project conventions except where an external format is explicitly named. They do not claim to be universal standards for competencies, roles or blueprints.

## 2. Names, identity and revisions

**REG-R001.** Every current artifact MUST live in a uniquely named directory within its type collection.

**REG-R002.** Directory names use meaningful lowercase words separated by single hyphens; a reader MUST be able to infer the topic without looking up an internal number.

Names such as `r1`, `r10` or `p09` are not valid titles or current canonical slugs.

**REG-R003.** Historical identifiers MAY remain in provenance and migration maps.

The main file has a predictable name determined by type. A rename preserves provenance and provides a compatibility map when an old path was published. An immutable revision identifies a particular content state. A mutable “current” pointer is a selection governed by a separate decision, not a new identity for every request.

## 3. Publication formats

| Collection | Main file | Required content |
| --- | --- | --- |
| `papers/<topic>/` | `PAPER.md` | Abstract, question and contribution, definitions, argument or results, counterexamples, limitations, references to engineering evidence |
| `engineering/specifications/<topic>/` | `SPECIFICATION.md` | Purpose, conformance, model, requirements, failure handling, acceptance cases, compatibility, evidence |
| `engineering/studies/<topic>/` | `STUDY.md` | Question, materials and rights, method, actual results, adverse cases, reproducibility, limitations, links to claims |
| `reference/glossary/` | `GLOSSARY.md` | Preferred terms, definitions, distinctions, aliases and language mapping |
| `reference/bibliography/` | `BIBLIOGRAPHY.md` | Identified works, primary URLs or DOIs, and the role of each source |
| `appendices/<topic>/` | `APPENDIX.md` | A named supporting subject, its scope, references and relationship to the main documents |

**REG-R004.** Current publications MUST appear in `publication-catalog.json`.

The catalogue records type, slug, path, title, summary, language and edition. It is a reading manifest, not an authorization to index or execute the content.

**REG-R005.** Each main Markdown file MUST have YAML front matter with `name`, `title`, `artifact`, `edition`, `author`, `language`, `license`, and a nonempty `description`.

Sources are registered through the repository source register.

**REG-R006.** It MUST contain one descriptive H1.

**REG-R007.** Version and machine identifiers belong in metadata, compatibility notes or provenance; they MUST NOT dominate the reading title.

Relative links connect the current edition. Historical claims link to pinned revisions.

## 4. Constraints and professional artifacts

The professional profile extends the same folder convention. Collections are created when actual artifacts exist; empty speculative directories are unnecessary.

| Artifact | Main file | Meaning and required sections |
| --- | --- | --- |
| Role | `ROLE.md` | Responsibility; scope; permitted decisions; required skills or competencies; interfaces; accountability |
| Skill | `SKILL.md` | A reusable procedure; when to use it; inputs; steps; checks; constraints; outputs; supporting resources |
| Competency | `COMPETENCY.md` | An ability requirement or assessed claim; subject; performance criteria; assessed conditions; evidence; validity limits |
| Blueprint | `BLUEPRINT.md` | A solution structure or process; intended result; components or steps; dependencies; choices; constraints; acceptance |
| Constraint | `CONSTRAINT.md` | Subject; scope; normative rule or condition; origin/authority; enforcement/check; exceptions; failure behavior |
| Work Item | `WORK_ITEM.md` | Goal; requirements revision; inputs; assignments; constraints; plan; result criteria; attempts and outcomes |

A competency definition says what ability would count. A competency assessment binds evidence to a particular executor and conditions. Neither a role nor a skill file certifies that ability. A blueprint organizes work; it does not supply authorization. Constraints are linked directly from all artifacts to which they apply, not buried in a general note or mistaken for optional advice.

For skills, the external [Agent Skills specification](https://agentskills.io/specification) governs the `SKILL.md` filename and required `name` and `description` front matter. This project uses its supported `metadata` map for extra project fields rather than inventing incompatible required top-level keys. The skill name matches its directory. Supporting code, references and assets remain inside that skill's directory. The document-body headings above are a project convention, not mandatory headings imposed by Agent Skills.

Repository instructions use [AGENTS.md](https://agents.md/), a plain Markdown instruction file. It is not a universal serialization format for a role or an agent identity.

**REG-R008.** Provider-specific executable agent configurations MUST have an explicit adapter and remain distinct from the human-readable role definition.

## 5. Registry obligations

**REG-R009.** Each registered revision MUST identify its kind, representation profile, identity, revision, license or disclosure restriction, provenance, required dependencies and applicable observations.

**REG-R010.** A reader MUST distinguish known, unknown, not applicable and withheld information.

**REG-R011.** Required references MUST resolve to the intended revision or report an unresolved dependency.

Historical registration of 34 artifact types describes one example registry; it does not establish 34 exhaustive kinds of knowledge. Its common envelope is a carrier for those examples, not a restriction on all future contracts. The [source map](../../../appendices/source-map/APPENDIX.md) preserves that compatibility context outside the scientific argument.

## 6. Acceptance and migration

**REG-R012.** Registry checks MUST reject duplicate canonical names, missing required main files, incompatible front matter, broken current links and silent identity reuse.

**REG-R013.** A rename test MUST show where the previous path leads and how a cited immutable revision remains recoverable.

Unknown required extensions block use; preserving unknown optional data does not establish that it was interpreted.

**REG-R014.** Migration MUST preserve source identity and original revisions, record the mapping, and disclose fields that could not be translated.

**REG-R015.** It MUST NOT infer a capability, grant or successful execution from the presence of an artifact.

The [revision paper](../../../papers/revision-and-governance/PAPER.md) explains these distinctions; the [editorial study](../../studies/editorial-skill-pilot/STUDY.md) records an actual bounded use of skills and a blueprint without claiming superiority from their existence.
