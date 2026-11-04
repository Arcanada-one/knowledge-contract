---
name: "bibliography"
title: "Primary Sources and Research Foundations"
artifact: "bibliography"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Named primary sources and the exact conceptual or technical role each plays in the current edition."
---

# Primary Sources and Research Foundations

**Publication edition:** 1.0 · **Bibliographic verification:** 4 November 2026

The entries below identify the primary sources actually used by the current edition. They distinguish established results and external formats from this project's own synthesis. A cited source supplies the stated conceptual or technical foundation; it does not endorse Knowledge Contract or establish the effectiveness of its implementation. No third-party book text or source-page images are reproduced in this publication.

## Provenance

Luc Moreau and Paolo Missier, editors. **PROV-DM: The PROV Data Model.** W3C Recommendation, 30 April 2013. [Dated specification](https://www.w3.org/TR/2013/REC-prov-dm-20130430/).

Used for the distinction among entities, activities and agents in provenance, and for the separation of provenance from a judgment about content. The project adds task-specific applicability and admission obligations; those are not claims made by PROV-DM on its behalf.

## SKOS

Alistair Miles and Sean Bechhofer, editors. **SKOS Simple Knowledge Organization System Reference.** W3C Recommendation, 18 August 2009. [Dated specification](https://www.w3.org/TR/2009/REC-skos-reference-20090818/).

Used for concepts, labels and knowledge-organization relations. A shared label or concept relation is not a proof of semantic equivalence or truth.

## Partial correctness

C. A. R. Hoare. **An Axiomatic Basis for Computer Programming.** *Communications of the ACM* 12(10), 1969, 576–580, 583. [DOI: 10.1145/363235.363259](https://doi.org/10.1145/363235.363259). [Author's institutional bibliography](https://www.cs.ox.ac.uk/people/publications/title/Tony.Hoare.html).

Used for the established idea of reasoning about programs through preconditions, postconditions and inference rules. The transformation paper adapts conditional preservation reasoning to its explicitly defined relations. Its composition argument is not presented as a novel replacement for program logic or a proof of termination.

## Submodular maximization

George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher. **An Analysis of Approximations for Maximizing Submodular Set Functions—I.** *Mathematical Programming* 14, 1978, 265–294. [DOI: 10.1007/BF01588971](https://doi.org/10.1007/BF01588971).

Used for the classical greedy approximation result under normalized, monotone submodular value and a cardinality limit. The context-composition paper states those assumptions and explains why complementary knowledge units can violate submodularity. The guarantee is not transferred to arbitrary budgets, penalties or semantic quality functions.

## Retrieval-augmented generation

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel and Douwe Kiela. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** *Advances in Neural Information Processing Systems* 33, 2020. [Conference publication](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). [Author manuscript](https://arxiv.org/abs/2005.11401).

Used as the primary reference for generation conditioned on retrieved material. The context-composition paper studies explicit coverage and preservation obligations; it does not claim to have replicated the cited experiments or surpassed their models.

## Computational complexity

Richard M. Karp. **Reducibility among Combinatorial Problems.** In *Complexity of Computer Computations*, 1972, 85–103. [DOI: 10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9).

Used as the primary source for the classical complexity context of set cover. The current paper gives its own explicit mapping from a finite covering problem to a restricted context-selection instance. This does not imply that every practical instance is hard or that finite exact search is impossible.

## Causal inference

Judea Pearl. **Causal Inference in Statistics: An Overview.** *Statistics Surveys* 3, 2009, 96–146. [DOI: 10.1214/09-SS057](https://doi.org/10.1214/09-SS057). [Author's institutional copy](https://escholarship.org/uc/item/1sv6k47m).

Used for the distinction between observed association and causal conclusions under assumptions about interventions and confounding. The utility paper therefore distinguishes measured task scores from identified causal benefits and does not treat a small exploratory comparison as a population estimate.

## HTTP caching

Roy T. Fielding, Mark Nottingham and Julian Reschke, editors. **HTTP Caching.** RFC 9111, Internet Standard, June 2022. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html).

Used as a reference for HTTP cache controls and freshness concepts. Knowledge applicability, semantic dependency closure and action authorization remain additional project obligations.

## Stale HTTP responses

Mark Nottingham. **HTTP Cache-Control Extensions for Stale Content.** RFC 5861, Informational, May 2010. [RFC 5861](https://www.rfc-editor.org/rfc/rfc5861.html).

Used as a clearly limited analogy for stale-while-revalidate and stale-if-error behavior. This document is informational, and its HTTP mechanisms do not authorize reuse of revoked knowledge or actions.

## Requirement language

Scott Bradner. **Key Words for Use in RFCs to Indicate Requirement Levels.** RFC 2119, BCP 14, March 1997. [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html).

Barry Leiba. **Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words.** RFC 8174, BCP 14, May 2017. [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html).

Engineering specifications use capitalized MUST, MUST NOT, SHOULD, SHOULD NOT and MAY in this sense. Their force concerns conformance to the stated project specification; it is not a claim that the specification is an IETF standard.

## Agent artifact formats

Agent Skills maintainers. **Agent Skills Specification.** [Official specification](https://agentskills.io/specification), consulted 4 November 2026.

Used for skill-directory naming, the required `SKILL.md` file, its `name` and `description` metadata, and supported extension metadata. The project defines its own additional reading structure while preserving compatibility with that format.

AGENTS.md maintainers. **AGENTS.md.** [Official format description](https://agents.md/), consulted 4 November 2026.

Used for repository instructions to coding agents. The format is ordinary Markdown and does not prescribe a universal schema for agent identities, competencies, roles or blueprints. The project's formats for those artifacts are explicitly its own conventions.

## Experimental source books

These books identify the historical materials used by the engineering studies. They are not sources for a new scientific theorem and their practical advice is not endorsed by this publication. The retained export identities, rather than the catalogue pages alone, identify the actual inputs that were processed.

- **Книга о вкусной и здоровой пище** (*The Book of Tasty and Healthy Food*). Ministry of Food Industry of the USSR. Moscow: Pishchepromizdat, 1952. [National Electronic Library record](https://rusneb.ru/catalog/000199_000009_005811805/). Used as the cooking export in the [transcription study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md).
- **Навигация, лоция и мореходная астрономия** (*Navigation, Pilotage, and Nautical Astronomy*). G. I. Fain. Moscow: Transport, 1977. [National Electronic Library record](https://rusneb.ru/catalog/000199_000009_007594442/). Used as the navigation export; the [retained corpus audit](../../engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json) identifies the processed representation.
- **Сто схемных задач по автоматике** (*One Hundred Circuit Problems in Automation*). V. A. Timofeev. Leningrad: Sudostroenie, 1964. The [retained corpus audit](../../engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json) identifies the automation export. The historical engineering tasks examine representations and preservation, not modern operational certification.

### Editorial input

Maxim Ilyakhov and Lyudmila Sarycheva. **Пиши, сокращай: Как создавать сильный текст** (*Write and Shorten: How to Create Strong Text*). Alpina Publisher. [Publisher's listing](https://alpinabook.ru/catalog/book-pishi-sokrashchay-2025/).

The [editorial pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) used the project's skills derived from a supplied OCR representation of this work. The source record describes the OCR bibliographic line as fourth edition, Moscow 2024, 400 printed pages; the supplied filename uses “2025,” and the digital input contains 427 physical page entries. These are retained input descriptors, not a claim that page counts or filenames prove the edition. The publisher's current listing identifies the work but does not authenticate the exact privately supplied file. The publication distributes the pilot's own texts and evaluations, not the book or the private source-derived toolkit.

## Project sources and evidence

Pavel Valentov. **Knowledge Contract and Meaning Management: earlier publication corpus.** Repository snapshot [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60).

The [source map](../../appendices/source-map/APPENDIX.md) records the migration from fourteen earlier paper files and ten specifications to the current reading structure. The [engineering evidence index](../../engineering/studies/evidence-index.json) binds individual empirical or analytical claims to their supporting records. Each study describes what can be rerun publicly, what is available only as a retained report, and what remains unmeasured.
