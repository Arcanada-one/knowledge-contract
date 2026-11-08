---
title: "Clear Names: Document and Roadmap Naming Canon"
sources: none
status: editorial-policy-proposal
updated: 2026-11-08
---

# Clear Names: Document and Roadmap Naming Canon

This canon implements the author's explicit naming direction of 8 November 2026. It governs reader-facing titles of scientific papers, specifications, studies, reference documents and roadmap deliverables. Adoption of this editorial proposal does not certify scientific claims or publish a website.

## Short name and explanatory subtitle

A full document title has the form **Short Name: Explanatory Subtitle**. The short name is one to three ordinary words in English or Russian and identifies the actual subject, not a code, slogan or claim of superiority. The subtitle states the document's scope, method or important limit. The first colon is the separator. When the previous title already begins with the same short label, do not repeat that label: for example, keep “Book Packages: Source Identity, Semantic Layers, and Validation”, not “Book Packages: Book Packages: …”. The explanatory wording is retained after removing that duplicated lead; the exact old title is stored separately. An inherited explanatory clause can contain its own colon. Chinese uses a compact natural phrase and the full-width separator `：`; artificial spaces are not introduced to imitate English word counts. Chinese and Russian explanatory subtitles must not begin with a mechanical repetition of the complete short name. Keep the informative remainder and all necessary qualifiers. A translated title is not a full-text translation.

Examples: **Meaning Bridge: From Human Meaning to Contract-Governed Knowledge**; **Мост смысла: От человеческого смысла к знаниям, управляемым контрактом**; **意义桥接：从人类意义到受契约约束的知识**.

Prefer established vocabulary: meaning, context, evidence, transformation, reuse. A title must not turn an illustrative result into an experiment, a hypothesis into a theorem, or a specification into an implemented guarantee. Short names are unique within the publication catalogue. No unexplained acronym or F/RM/G identifier may be the primary reading title. Contextual identifiers remain useful in machine records and historical correspondence.

## Canonical representation

The publication catalogue's `title`, the source front matter `title` and its single H1 agree exactly. `short_title` and `subtitle` are editorial metadata; they do not change the publication edition or any runtime protocol. The [name register](names.json) records the selected English, Russian and Simplified Chinese names. [DOCUMENTS.md](../../DOCUMENTS.md) provides the complete cross-language reading list and old-title crosswalk.

Use the short name in compact navigation when the document type and destination are clear. Use the full title in a document header, catalogue, bibliography entry and first public introduction. A citation should still identify the author, edition, canonical path and immutable revision. A new display title does not retroactively rename an old cited version.

## Stable identity and compatible links

Renaming a reading title does not rename the slug, folder, canonical filename, requirement ID, claim ID, task ID or wire token. Keep old source revisions and their attestations. Preserve any prior heading anchor used by links; preserve roadmap compatibility anchors. Do not edit retained raw evidence, historical review receipts, corpus decisions or allowlists merely to make their displayed titles agree with today's wording.

Title edits change file bytes. Old SHA-256 values remain valid only for the old bytes. When a scientific body is unchanged, a mechanical body comparison can establish that limited fact; it is not a new scientific review. Rendered pages and downloadable artifacts need a new source pin and their own checks before being called updated.

## Roadmap language

Readers encounter **Claim Atlas**, **Meaning Bridge** or **Russian and Chinese Editions**, not an isolated `RM-01` or `F01`. Every work package exposes a clear name, intended output, starting evidence, acceptance boundary, dependencies by name, owner of the content and any separate integration owner. The technical code is secondary compatibility metadata. A link uses the human name while retaining the established target anchor.

Keep three dimensions separate: existence of an artifact; its review/publication state; execution state in Muneral. A document in a branch is not a completed task. `planned`, `drafted`, `reviewed`, `merged`, `deployed` and `indexed` describe different observations. A pause applies to engineering execution, not automatically to reading or authoring theory.

## Translation fidelity

Russian and Chinese titles express the same scope, negations and epistemic strength as English. A localized name is not a full document translation and does not inherit independent review. Existing source-pinned translation branches are not silently rebased or overwritten by a naming change. They need an explicit old/new title mapping, fresh target hashes and scoped review of any altered text. Body translation, title adaptation and site integration remain separate deliverables.

## Review checklist

A reviewer checks brevity, subject accuracy, uniqueness, natural language, non-overclaiming, catalogue/front-matter/H1 agreement, preserved slugs and anchors, body preservation for title-only changes, and truthful translation and publication states. A rejected title is replaced without inventing a new scientific work. Name checks complement, and never bypass, the repository's ordinary source, licence, DCO, link and publication checks.

No engineer is assigned to write the titles or translate the manuscripts. KC-Brain authors them; a separate reviewer evaluates them. Website deployment is deferred during the engineering pause.
