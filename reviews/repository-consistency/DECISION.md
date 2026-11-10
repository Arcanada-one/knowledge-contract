---
title: "Corpus Consistency: Counting Rules and Current Work Direction"
sources: none
status: author-correction-proposal
updated: 2026-11-11
---

# Corpus Consistency: Counting Rules and Current Work Direction

## Scope and attribution

KC-Brain prepared this bounded correction under Pavel Valentov's direction to resume autonomous work, with engineering available and used only for necessary restricted operations. It builds on the consistency finding forwarded by DEUS-Arcana and the subsequent KC-SWE verification. The externally reported audit was not independently read in full; its unchecked claims are not adopted here. No scientific proposition, retained experiment, corpus decision, requirement identifier or admitted rendition hash is changed.

Inspected source: `0892eeb150acae9df5e5d498902c7b5e04ce1871`. Translation proposal: PR76 at `9723b4787c009e5b6d1646e0e53f980d326c5afc`. Main's recursive translation tree was complete (`truncated=false`) and contained eight body files, four per locale. The complete PR changed-file listing and PR inventory identify 50 body paths, 25 per locale. Main's eight paths overlap the proposal; KC-SWE additionally reported that all eight overlapping blobs match. Full independent byte comparison of every proposal translation is not claimed by this review.

The current catalogue contains 31 records, not the historical baseline's 30. It adds the Meaning Geometry research draft. The correction therefore records both denominators instead of silently reusing an old counter.

## Author decisions

### Counting and acceptance

Adopt the set-based rule in [Translations](../../roadmap/TRANSLATIONS.md). In each locale: four in main, 25 in the proposal, four overlapping, 21 proposal-only, six missing against the current 31-document scope. Against the historical 30, five are missing. Fifty files across both locales are not fifty admitted or served renditions. Missing-body counts do not measure translation quality.

### Work direction

Use [Active Work](../../roadmap/EXECUTION_STATUS.md) as the single current-status source. The old quota-based blanket pause is superseded. Use **operator** in execution policy, and **author** in scientific attribution; both identify Pavel Valentov in this project. Current permissions and actual review/CI/deployment evidence remain separate.

Prepared exact replacements for the existing string-valued JSON metadata, without changing graph nodes, edges or tracker state:

- `roadmap/workstreams.json` / `engineering_execution`: `active_under_existing_gates; see roadmap/EXECUTION_STATUS.md; not a Muneral state update`.
- `roadmap/dependencies.json` / `execution_pause`: `rescinded_by_operator_2026-11-11; see roadmap/EXECUTION_STATUS.md; not a Muneral state update`.

Those fields were inspected in their source. Keeping their existing string type avoids an unrelated schema migration. Retain `execution_state` as not reconciled unless a real Muneral read supports changing it. No availability statement implies an experiment budget.

The same direction must replace current blanket-pause statements in README, AGENTS, CONTRIBUTING, ROADMAP, localized roadmap, SITE_DELIVERY, TASKS, workstreams and dependencies. Do not alter historical mail, immutable evidence or dated reports to erase the earlier interruption. Old execution restrictions have to be replaced, not simply accompanied by a contradictory footnote. This proposal supplies the authoritative wording; remaining propagation is not marked complete here.

### Reader-facing title decisions

The two confirmed repeated subtitles may be replaced as follows, preserving canonical paths, previous-title history, existing anchors and scientific bodies:

| Canonical path | English | Russian | Simplified Chinese |
| --- | --- | --- | --- |
| `engineering/specifications/contract-family/SPECIFICATION.md` | Knowledge Operations: Preconditions, Results and Transformation Obligations | Операции над знаниями: Предусловия, результаты и обязательства преобразования | 知识操作：前提条件、结果与变换义务 |
| `reference/bibliography/BIBLIOGRAPHY.md` | Research Foundations: Primary Literature and Related Work | Исследовательские основания: Первоисточники и связанные исследования | 研究基础：原始文献与相关研究 |

These are prepared title decisions, not a claim that all title surfaces or translated bodies have been updated in this proposal. Apply catalogue/front matter/H1/DOCUMENTS/name-register changes together, retain old anchors explicitly, and review any resulting rendition binding delta separately. Do not mass-rehash accepted receipts. The five further allegedly drifting Russian titles remain unverified and are not renamed merely on a fuzzy match.

### Baseline papers and revision counts

Use **eight baseline papers plus two separately labelled foundations research drafts** for the current ten-paper catalogue. Do not equate the number of baseline papers with the number that received a particular historical editorial pass. Replace the ambiguous current statement about “seven revised baseline papers” with the inventory statement, rather than inventing an eighth revision receipt.

### Site follow-through

The rebuilt 31-record proposal in contract-place-site PR33 remains separate. A direct `public/programme.json` pin-consistency guard is a useful bounded hardening change, not a new claim that the existing reproducibility gate is absent. Its tests must distinguish catalogue/source/programme disagreement and preserve useful positive fixtures. Stale 29/30 prose belongs to the same consistency effort, not a duplicate corpus redesign. Independent exact-head review and served readback are still required; this document does not supply an unperformed browser or deployment check.

## Authored tooling and observed tests

`tools/report_translation_coverage.py` reads an explicit catalogue commit and two explicit Git trees. It counts canonical paths, reports identical and differing overlaps and refuses unavailable refs. It neither changes the repository nor claims fidelity, source currency, rendition admission, website delivery or indexing.

Command actually run in an isolated package with Python 3.13.5:

```sh
python3 -B -m unittest tools.test_report_translation_coverage -v
```

**12 tests passed**, including union-versus-sum, differing overlaps, base-only bodies, source-denominator changes, ancillary exclusions, invalid inputs, and a disposable two-commit Git repository. Two executions in that temporary repository produced the same JSON and left its worktree and HEAD unchanged. These are producer-authored tests, not an independent review or a full project suite.

A network clone of the real repository was attempted but failed at DNS resolution in this environment. The exact-ref CLI has consequently **not** been run against the entire real checkout here. The source inventory above comes from GitHub connector reads, not a claimed local full-repository run. The normal Pandoc 3.1.3 publication, sources, requirement-register, DCO, relevant regressions and hosted checks remain required at the final candidate SHA.

## Remaining integration boundaries

This proposal updates the translation inventory, supplies current execution wording and a tested reporting utility. It does not claim that all roadmap copies, title surfaces, site prose, acceptance records or production pages are already synchronized. Continue the existing bounded consistency work with this prepared content; do not create a second tracker or a parallel competing naming programme. Authoring and test design are complete for this slice; exact-head repository validation, separate review and deployment have their own evidence.
