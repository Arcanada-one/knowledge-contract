---
title: "Clear Names: Document and Roadmap Naming Canon"
sources: none
status: editorial-policy
updated: 2026-11-09
---

# Clear Names: Document and Roadmap Naming Canon

This canon implements Pavel Valentov's naming directions of 8 and 9 November 2026. It governs reader-facing titles of scientific papers, specifications, studies, reference documents, verification packages, roadmap deliverables and public progress reports. An editorial name does not certify a scientific result, an implementation or a deployment.

## Short name and explanatory subtitle

A full document title has the form **Short Name: Explanatory Subtitle**. The short name is one to three ordinary words in English or Russian and identifies the actual subject, not a code, slogan or claim of superiority. The subtitle states the scope, method or important limit. The first colon is the separator. When an earlier title already begins with the short label, remove the duplicated lead: use “Book Packages: Source Identity, Semantic Layers, and Validation”, not “Book Packages: Book Packages: …”. Preserve the exact earlier title in the name register. An inherited explanatory clause may contain another colon.

Chinese uses a compact natural phrase and the full-width separator `：`; do not insert artificial spaces to imitate an English word count. Russian and Chinese subtitles must not mechanically repeat the complete short name. Retain the informative remainder and necessary qualifications. A translated title is not a translated body.

Examples: **Meaning Bridge: From Human Meaning to Contract-Governed Knowledge**; **Мост смысла: От человеческого смысла к знаниям, управляемым контрактом**; **意义桥接：从人类意义到受契约约束的知识**.

Prefer established vocabulary: meaning, context, evidence, transformation, reuse. A title must not turn an illustration into an experiment, a hypothesis into a theorem, or a specification into an implemented guarantee. Short names are unique within the publication catalogue. An unexplained acronym or F/RM/G/S/N identifier must never be the primary reading title.

## Canonical representation

The catalogue `title`, source front-matter `title` and single H1 agree exactly. `short_title` and `subtitle` are editorial metadata, not a new publication edition or runtime protocol. The [document name register](names.json) records English, Russian and Simplified Chinese names. [All document names](../../DOCUMENTS.md) provides the complete reading list and old-title crosswalk. The [reading guide](../../READING.md) explains where to start.

Use the short name in compact navigation when type and destination are clear. Use the full title in document headers, catalogue entries, bibliographic entries and first public introductions. Citations still identify author, edition, canonical path and immutable revision. Renaming today's display does not retroactively rename an earlier cited version.

## Verification packages and scenarios

A verification package is not named after a range of case identifiers. Use **Knowledge Checks: Mandatory Requirements and Evidence Assessment**, not “S01–S22”, for the finite evidence-assessment package. Use **Execution Checks: Authorization, Budget and Result Integrity** for its distinct native-integration checks. [Check names](CHECKS.md) gives all 22 finite-scenario names and all six native-scenario names in English, Russian and Simplified Chinese, with links to their original specification and implementation proposal.

A case has a meaningful short name and a precise expected result under stated premises. Its legacy code is a secondary locator, not a replacement for either. For example: **Joint Evidence — missing part of a conjunctive rule** (technical locator `S03`). A list of prepared scenarios is not a count of executed tests. A specification review does not approve an implementation, and a finite synthetic pass does not authorize execution.

For an engineer-facing exact reference, the code may follow the name in parentheses or a technical-ID column. For public summaries and announcements, lead with the package name and explain the scope in ordinary language. Do not publish a sentence consisting only of opaque ranges such as “G05/P12, S01–S22 approved”. State what was assessed and whether the evidence concerns a specification, code, a finite run or a deployed service.

## Stable identity and compatible links

Renaming a reading title does not rename its slug, folder, canonical filename, requirement ID, claim ID, case ID, task ID or wire token. Preserve old source revisions and their attestations, old heading anchors used by links, and roadmap compatibility anchors. Do not edit retained raw evidence, historical reviews, corpus decisions or allowlists merely to make their names agree with current wording.

Update the text of current links, cards, contents lists, breadcrumbs, download labels and search result titles from the name register. Keep an old label as a searchable alias, pointing to the same logical work rather than a duplicate document. A human name must be the visible link text; the existing canonical URL or anchor may remain technical internally. New readable anchors may be added as aliases, never by deleting cited anchors.

Title edits change bytes. Old SHA-256 values certify only old bytes. For a title-only change, compare the complete unchanged scientific body and record the exact old/new mapping; do not equate such a comparison with a new scientific review. Generated pages, downloads and search metadata need their own exact-source build and readback before being called updated. Backend indexing remains subject to its separate admission policy.

## Roadmap language

Readers encounter **Claim Atlas**, **Meaning Bridge** and **Russian and Chinese Editions**, not an isolated `RM-01` or `F01`. Every work package gives a readable name, intended output, starting evidence, acceptance boundary, dependencies by name, content owner and any separate integration owner. A link uses the name while retaining the established target anchor. Codes remain secondary compatibility metadata.

Keep artifact existence, review/publication state and Muneral execution state separate. A file in a proposal is not a completed task. Drafted, reviewed, merged, deployed and indexed are different observations. Future research does not make an accepted finite publication permanently unfinished.

## Translation fidelity

Russian and Chinese titles preserve English scope, negations and epistemic strength. Use the [shared trilingual glossary](../glossary/GLOSSARY.md#multilingual-terminology-policy). A concise alias does not rename a technical type or weaken its definition. A localized title is not a full-text translation and does not inherit review of a different source.

Do not silently repin a translation when the English title changes. Record the old/new source and target identities, distinguish title/anchor/link adaptation from changes to scientific prose, and review the actual changed scope. Earlier full-body findings remain bound to their original pairs. A versioned rendition entry must make the current source, exact target, evidence and scope inspectable.

## Review checklist

Check subject accuracy, brevity, uniqueness, natural language, non-overclaiming, catalogue/front-matter/H1 agreement, stable slugs and anchors, title-only body preservation, link targets and truthful review/publication states. Check that public summaries do not substitute a case range for the package name. Naming checks complement ordinary source, licence, DCO, link and publication checks; they do not bypass them.

KC-Brain authors names and manuscripts; separate reviewers assess their substantive changes. Pavel's 9 November instruction authorizes progression of the prepared public-reading release through the existing review, CI, merge and deployment process. The earlier engineering-pause wording is not a blanket prohibition on that publication lane. This does not resume unrelated experiments, grant runtime permissions or declare a deployment completed.
