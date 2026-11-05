---
name: "bibliography"
title: "Primary Sources and Research Foundations"
artifact: "bibliography"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Named primary sources and the exact conceptual or technical role each plays in the current edition."
---

# Primary Sources and Research Foundations

**Publication edition:** 1.1 · **Bibliographic verification:** 4 November 2026

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

## Program slicing

Mark Weiser. **Program Slicing.** *IEEE Transactions on Software Engineering* SE-10(4), 1984, 352–357. [Original article](https://faculty.cc.gatech.edu/~harrold/6340/cs6340_fall2009/Readings/Weiser.Slicing.TSE.pdf).

Used in [semantic objects and context](../../papers/semantic-objects-and-context/PAPER.md) to identify the established behavior-preservation problem behind a backward slice. The paper gives a restricted acyclic model; it does not introduce a new general slicing algorithm or infer semantic preservation for arbitrary text.

## Truth maintenance

Jon Doyle. **A Truth Maintenance System.** *Artificial Intelligence* 12(3), 1979, 231–272. [Publisher record](https://www.sciencedirect.com/science/article/pii/0004370279900080). [MIT report version, AI Memo 521](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a).

Used in [revision and governance](../../papers/revision-and-governance/PAPER.md) as prior work on recording reasons and revising beliefs as assumptions change. The project's reachability argument identifies potentially affected assessments; it is not an implementation of Doyle's system.

## Build systems

Andrey Mokhov, Neil Mitchell and Simon Peyton Jones. **Build Systems à la Carte.** *Proceedings of the ACM on Programming Languages* 2(ICFP), article 79, 2018, 1–29. [DOI: 10.1145/3236774](https://doi.org/10.1145/3236774). [Author's article](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf).

Used in [controlled knowledge reuse](../../papers/controlled-knowledge-reuse/PAPER.md) for the established distinction between scheduling and rebuilding, and for correctness relative to declared dependencies. Agreement with build dependencies does not establish a source's truth, a new task's semantic requirements or current authority.

## Views and complements

François Bancilhon and Nicolas Spyratos. **Update Semantics of Relational Views.** *ACM Transactions on Database Systems* 6(4), 1981, 557–575. [Original article](https://cs.uwaterloo.ca/~david/cs848s18/constant-complement.pdf).

Used in [constrained transformations](../../papers/constrained-transformations/PAPER.md) as a prior construction in which a view and retained complement determine database state and constrain update translation. The analogy motivates retaining residual information; the project does not claim those view-update laws for natural-language projections.

## Theory change

Carlos E. Alchourrón, Peter Gärdenfors and David Makinson. **On the Logic of Theory Change: Partial Meet Contraction and Revision Functions.** *The Journal of Symbolic Logic* 50(2), 1985, 510–530. [DOI: 10.2307/2274239](https://doi.org/10.2307/2274239). [Publisher record](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/on-the-logic-of-theory-change-partial-meet-contraction-and-revision-functions/7ED837BAD5FB6D9A7C77906D73527F9C).

Used in [revision and governance](../../papers/revision-and-governance/PAPER.md) to distinguish logical contraction and revision from versioned artifacts and adoption decisions. The current model neither defines an AGM revision operator nor claims to satisfy the AGM postulates.

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

## JSON exchange and schemas

Tim Bray, editor. **The JavaScript Object Notation (JSON) Data Interchange Format.** RFC 8259, Internet Standard, December 2017. [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259).

Austin Wright, Henry Andrews, Ben Hutton and Greg Dennis, editors. **JSON Schema: A Media Type for Describing JSON Documents.** Draft 2020-12. [Official core specification](https://json-schema.org/draft/2020-12/json-schema-core).

Used for the exchange syntax and JSON Schema dialect of the bounded observation, dependency-change, book-package and index-receipt profiles. A schema validates the declared data shape and constraints; it does not authenticate an observation or perform every cross-record semantic check. The exact-byte hash profile does not imply JSON value canonicalization.

## Agent artifact formats

Agent Skills maintainers. **Agent Skills Specification.** [Official specification](https://agentskills.io/specification), consulted 4 November 2026.

Used for skill-directory naming, the required `SKILL.md` file, its `name` and `description` metadata, and supported extension metadata. The project defines its own additional reading structure while preserving compatibility with that format.

AGENTS.md maintainers. **AGENTS.md.** [Official format description](https://agents.md/), consulted 4 November 2026.

Used for repository instructions to coding agents. The format is ordinary Markdown and does not prescribe a universal schema for agent identities, competencies, roles or blueprints. The project's formats for those artifacts are explicitly its own conventions.

## Evaluation methods

The following sources explain methodological distinctions used in the studies. They do not authenticate the historical runs, supply missing fixtures or turn same-session reviews into independent replication.

Brian A. Nosek, Charles R. Ebersole, Alexander C. DeHaven and David T. Mellor. **The Preregistration Revolution.** *Proceedings of the National Academy of Sciences* 115(11), 2018, 2600–2606. [DOI: 10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114). [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/). The [editorial pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) distinguishes a protocol fixed before its retained outputs from an analysis composed after results were known. Its local recorded protocol was not registered in an external public registry.

Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez and Ion Stoica. **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.** *Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track*, 2023. [Author manuscript](https://arxiv.org/abs/2306.05685). Used for the need to examine judge biases and the limits of agreement. The editorial and [projection](../../engineering/studies/executable-projections-and-revision/STUDY.md) studies use their own coarse rubrics and masking; they do not inherit the cited benchmark's agreement or validation results.

Richard A. DeMillo, Richard J. Lipton and Frederick G. Sayward. **Hints on Test Data Selection: Help for the Practicing Programmer.** *Computer* 11(4), April 1978, 34–41. [Publisher record](https://ieeexplore.ieee.org/abstract/document/1646911). [Institutional bibliographic record](https://www.cerias.purdue.edu/apps/reports_and_papers/view/919). This is historical background for deliberate program mutation. The project reports its declared mutants and whether they are distinguished; a finite mutation result is not general test adequacy.

Alfred Tarski. **A Lattice-Theoretical Fixpoint Theorem and Its Applications.** *Pacific Journal of Mathematics* 5(2), 1955, 285–309. [Publisher's original article](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p11-s.pdf). This supplies general fixed-point background. The [dependency study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) computes the least closure by finite monotone iteration on the power set of a declared graph; its proof and implementation checks do not establish that every semantic dependency was recorded.

National Institute of Standards and Technology. **SCLITE Scoring Package: Alignment and Scoring Documentation.** [Official SCTK documentation](https://github.com/usnistgov/SCTK/blob/master/doc/sclite.htm), consulted 4 November 2026. Used for reference–hypothesis alignment and substitution, deletion and insertion counts underlying word-error reporting. The [transcription study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md) states its character- and word-unit definitions explicitly; it reports no measured CER or WER because the required reference and protocol are unavailable.

## Experimental source books

These books identify the historical materials used by the engineering studies. They are not sources for a new scientific theorem and their practical advice is not endorsed by this publication. The retained export identities, rather than the catalogue pages alone, identify the actual inputs that were processed.

- **Книга о вкусной и здоровой пище** (*The Book of Tasty and Healthy Food*). Ministry of Food Industry of the USSR. Moscow: Pishchepromizdat, 1952. [National Electronic Library record](https://rusneb.ru/catalog/000199_000009_005811805/). Used as the cooking export in the [transcription study](../../engineering/studies/source-transcription-and-uncertainty/STUDY.md). The retained export key `molchanova` and Russian label “Молчанова” identify that input in project reports; they are not a claim of sole authorship. The cited catalogue identifies the Ministry, and this edition does not infer an editor's identity from an export key.
- **Навигация, лоция и мореходная астрономия** (*Navigation, Pilotage, and Nautical Astronomy*). G. I. Fain. Moscow: Transport, 1977. [National Electronic Library record](https://rusneb.ru/catalog/000199_000009_007594442/). Used as the navigation export; the [retained corpus audit](../../engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json) identifies the processed representation.
- **Сто схемных задач по автоматике** (*One Hundred Circuit Problems in Automation*). V. A. Timofeev. Leningrad: Sudostroenie, 1964. These are the bibliographic descriptors recorded for the automation export in the [retained corpus audit](../../engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json). An independently verified stable catalogue record for this exact edition was not established in this review; the project audit is input provenance, not external bibliographic confirmation. The historical engineering tasks examine representations and preservation, not modern operational certification.

### Editorial input

Maxim Ilyakhov and Lyudmila Sarycheva. **Пиши, сокращай: Как создавать сильный текст** (*Write and Shorten: How to Create Strong Text*). 4th ed. Moscow: Alpina Publisher, 2024, 400 printed pages, **as declared in the supplied OCR bibliographic line**. [Publisher's work listing](https://alpinabook.ru/catalog/book-pishi-sokrashchay-2025/). No independently verified ISBN for the supplied edition is asserted.

The [editorial pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) used the project's skills derived from a supplied OCR representation of this work. The same derived package is examined in the [dependency-closure study](../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md), whose [layout preservation report](../../engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json) and [dependency graph](../../engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json) retain the source's record names and dependency metadata.

The supplied filename uses “2025,” and the digital input contains 427 physical page entries. These descriptors differ from the OCR bibliographic line and do not authenticate an edition. The publisher's current listing identifies the work but does not authenticate the exact privately supplied file. The publication distributes the pilot's own texts, evaluations and package metadata, not the book or the private source-derived toolkit.

## Project sources and evidence

Pavel Valentov. **Knowledge Contract and Meaning Management: earlier publication corpus.** Repository snapshot [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60).

The [source map](../../appendices/source-map/APPENDIX.md) records the migration from fourteen earlier paper files and ten specifications to the current reading structure. The [engineering evidence index](../../engineering/studies/evidence-index.json) binds individual empirical or analytical claims to their supporting records. Each study describes what can be rerun publicly, what is available only as a retained report, and what remains unmeasured.
