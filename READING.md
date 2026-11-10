---
title: "Start Reading: Knowledge Contract for People and Agents"
sources: ["Knowledge Contract project corpus and publication edition"]
status: public reading guide
updated: 2026-11-09
---

# Start Reading: Knowledge Contract for People and Agents

[Русский](guides/READING.ru.md) · [简体中文](guides/READING.zh-Hans.md) · [All document names](DOCUMENTS.md) · [Roadmap](ROADMAP.md)

Knowledge Contract connects knowledge to the conditions under which it can be interpreted, checked and used. A source quotation is not automatically true; a relevant passage is not necessarily sufficient context; a successful check is not permission to act. The project makes those differences explicit for human readers and AI agents.

## Choose a reading path

| Your question | Start with | Continue with |
| --- | --- | --- |
| What is the project about? | [Meaning Bridge](papers/human-meaning-and-computable-knowledge/PAPER.md), explicitly a research draft | [Meaning in Context](papers/semantic-objects-and-context/PAPER.md) |
| How does knowledge survive processing? | [Knowledge Transformations](papers/constrained-transformations/PAPER.md) | [Context Assembly](papers/retrieval-and-context-composition/PAPER.md) |
| How do we inspect and revise a claim? | [Evidence and Falsification](papers/evidence-and-falsification/PAPER.md) | [Knowledge Revision](papers/revision-and-governance/PAPER.md) |
| What must an implementation check? | [Contract Core](engineering/specifications/knowledge-contract-core/SPECIFICATION.md) | [Knowledge Operations](engineering/specifications/contract-family/SPECIFICATION.md), [Status Model](engineering/specifications/status-model/SPECIFICATION.md) |
| How should representations be compared? | [Meaning Geometry](papers/geometry-of-semantic-representations/PAPER.md), a research draft with bounded mathematical review | [Meaning in Context](papers/semantic-objects-and-context/PAPER.md); proximity is not logical entailment or authorization |
| What was actually observed? | [Engineering studies](engineering/studies/README.md) | [Claim–evidence index](engineering/studies/evidence-index.json), including limitations and negative results |
| How can an agent access the publication? | [Publication Interfaces](appendices/api-integration/APPENDIX.md) | [Context Package](engineering/specifications/context-package/SPECIFICATION.md), [Reuse Policy](engineering/specifications/reuse-policy/SPECIFICATION.md) |

The [complete document register](DOCUMENTS.md) lists all 31 proposed catalogue works with readable names. They comprise ten scientific papers, eleven specifications, six studies, a glossary, a bibliography and two appendices. The foundations introduction is identified as a research draft; a catalogue entry is not a claim of external peer review or production readiness.

## Read, inspect and obtain the source

The [website](https://contract.place/) is the reading surface. This repository is the source and version history. Follow each document's Markdown link for its full text; GitHub's raw-file control provides that exact Markdown. For a reproducible collection, use a pinned Git commit or GitHub's repository archive at that revision. Do not treat a moving branch name as an immutable citation.

The website's language selector and the language of a manuscript are separate. A Russian or Chinese interface must not be counted as a translated manuscript when its body is English. Versioned translations have explicit source, review and fallback states. The source repository's [translation proposal](https://github.com/Arcanada-one/knowledge-contract/pull/76) is a work-in-progress record, not a list of served locale pages.

## Understand the kinds of evidence

A paper can give a conditional proof. A specification states requirements. A finite study reports its observed cases. A deployment record identifies what was actually served. These are useful together, but none silently replaces the others. Negative results, comparator ties, uncertainty and unresolved questions remain part of the publication.

Names such as [Knowledge Checks](reference/document-naming/CHECKS.md#knowledge-checks-mandatory-requirements-and-evidence-assessment) identify a verification package. Technical case labels are locators inside it, not names of scientific papers. [Execution Checks](reference/document-naming/CHECKS.md#execution-checks-authorization-budget-and-result-integrity) have a different scope from finite synthetic checks.

## Contribute a checkable improvement

Read [Contributing](CONTRIBUTING.md). Humans and agents can report a precise objection, propose a counterexample, reproduce a bounded test, improve an explanation or submit a translation. Identify the document and exact revision, the relevant section, the claim or expected behavior, and the evidence supporting the correction. Distinguish a mathematical refutation satisfying every premise from an example outside the premise set.

Reviews are assessed on their substance, not on the number of agreeing agents. Author checks, internal cross-role agent review, external peer review and native-speaker language review are different observations. Do not invent one from another. Follow the [security reporting route](SECURITY.md) for sensitive findings instead of publishing secrets or private data.

A release is a finite, inspectable state of this continuing research. The [roadmap](ROADMAP.md) describes what comes next; it is not a requirement that every future investigation finish before people can read an accepted edition.
