---
title: "Russian and Chinese Editions: Coverage and Remaining Work"
sources: none
status: source-pinned-file-inventory
updated: 2026-11-11
---

# Russian and Chinese Editions: Coverage and Remaining Work

This inventory separates files integrated into the source branch, files in the translation proposal, their overlap, missing authoring, fidelity review and actual website delivery. File presence is not a new semantic acceptance or a complete-translation verdict.

## Snapshots and counting rule

The source catalogue and integrated-tree snapshot are [0892eeb1](https://github.com/Arcanada-one/knowledge-contract/tree/0892eeb150acae9df5e5d498902c7b5e04ce1871), with **31 source documents**: eight baseline papers, two research drafts (Meaning Bridge and Meaning Geometry), eleven specifications, six studies, a glossary, a bibliography and two appendices.

The translation proposal is [PR76](https://github.com/Arcanada-one/knowledge-contract/pull/76), head `9723b4787c009e5b6d1646e0e53f980d326c5afc`. Count one canonical body path per work and locale, `translations/<locale>/<canonical path>`. Exclude translated titles, status notes, review files and public-interface prose.

Let A be the work paths present in the pinned main snapshot and D the work paths present in the proposal. Authored file coverage is **A union D**, not the sum of their sizes. A path in both sets is counted once. Equal blobs need no content choice when integrating main; different blobs require reconciliation. This arithmetic does not establish that a draft is faithful to the current English source or accepted for release.

## Current 31-document scope

Each pair in the table is **Russian / Simplified Chinese**. The same counts currently apply to both locales.

| Kind | Source documents | Present in main | Present in PR76 | Overlap | Proposal only | Missing from both |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Scientific papers | 10 | 0 / 0 | 4 / 4 | 0 / 0 | 4 / 4 | 6 / 6 |
| Engineering specifications | 11 | 0 / 0 | 11 / 11 | 0 / 0 | 11 / 11 | 0 / 0 |
| Engineering studies | 6 | 4 / 4 | 6 / 6 | 4 / 4 | 2 / 2 | 0 / 0 |
| Glossary | 1 | 0 / 0 | 1 / 1 | 0 / 0 | 1 / 1 | 0 / 0 |
| Bibliography | 1 | 0 / 0 | 1 / 1 | 0 / 0 | 1 / 1 | 0 / 0 |
| Appendices | 2 | 0 / 0 | 2 / 2 | 0 / 0 | 2 / 2 | 0 / 0 |
| **Total** | **31** | **4 / 4** | **25 / 25** | **4 / 4** | **21 / 21** | **6 / 6** |

Thus the current source catalogue has **62 work-locale slots**, **50 distinct authored body files** across the two snapshots, and **12 missing body files**. Of those 50 files, eight are already in main and 42 are proposal-only. These are file-inventory counts, not 50 accepted or served translations.

The four works already present on main in both locales are **Dependency Closure**, **Executable Projections**, **Reuse Economics** and **Uncertainty Preservation**. Their accepted rendition records retain their own exact source and target bindings. This inventory does not refresh those bindings or rewrite review history.

The four paper drafts in PR76 are **Meaning in Context**, **Knowledge Revision**, **Knowledge Transformations** and **Context Assembly**. The six remaining paper bodies per locale are **Meaning Bridge**, **Interaction and Memory**, **Evidence and Falsification**, **Knowledge Reuse**, **Knowledge Utility**, and **Meaning Geometry**.

## Historical 30-document scope and the future target

The earlier baseline [a0450428](https://github.com/Arcanada-one/knowledge-contract/tree/a0450428704fcd41b411203f2fc88c06c779610b) had 30 documents. Against that fixed scope, the same 25 files per locale leave **five per locale, ten in total**, missing. That is the meaning of the earlier **50/60** statement. Adding the two Meaning Geometry translations creates the difference between the historical and current denominators; it does not erase an old result or turn ten into twelve for the same scope.

The programme's target of **34 materials** is a third scope, not a count of already completed canonical works. Do not mix it with either 30 or 31. Recompute from a newly pinned catalogue when its actual membership changes.

## Reproduce the file inventory

Fetch the exact commits into a permitted local repository first. The reporter itself is read-only and does not access the network:

```sh
python3 -B tools/report_translation_coverage.py --repo . --source-ref 0892eeb150acae9df5e5d498902c7b5e04ce1871 --base-ref 0892eeb150acae9df5e5d498902c7b5e04ce1871 --draft-ref 9723b4787c009e5b6d1646e0e53f980d326c5afc
```

For the historical denominator, change only `--source-ref` to `a0450428704fcd41b411203f2fc88c06c779610b`. The output lists counted and missing paths, identical/different overlaps and excluded ancillary paths. A missing ref is an error, not a zero count. An earlier PR diff can show an already integrated path as added because its base is old; that is not a second translation.

The measurements and limits of the present correction are in [the review record](../reviews/repository-consistency/DECISION.md). The tool inventories bytes and identities only. Body completeness and fidelity require actual content review, not filename arithmetic.

## Ancillary public text

The body counts do not include every public sentence. Repository and section introductions, roadmap explanations, contribution/publication guidance, navigation, cards, status labels, downloads, error/help messages, search/index disclosures, captions and release notes have separate source and coverage records. No complete-site translation claim follows from body counts or translated titles.

## Acceptance and delivery

KC-Brain authors and self-checks the full text against its pinned English original. Preserve negation, quantifiers, modality, source attribution, units, numbers, equations, code, table rows, examples, limits and bibliographic locators. Literal protocol identifiers are not translated. Research-draft status is retained.

A separate reviewer names the exact source and target, coverage, method, findings and limitations. Earlier acceptance of selected fixes does not cover other bodies or changed bytes. A demonstrated title-only change may receive a title-only review; it does not establish scientific truth.

After source and rendition review, ordinary CI and acceptance, integrate actual translated bodies into the locale loader, rebuild from the exact source and check served HTML/Markdown/PDF where supplied. Resolve links consistently in classification, comparison and rendering. Missing bodies remain explicit unavailable states or English fallbacks, not falsely labelled Russian or Chinese texts.

Engineering is available under [the current operator direction](EXECUTION_STATUS.md). There is no blanket quota pause. This inventory neither dispatches a new paid experiment nor creates an index admission, changes Muneral state or certifies a deployment.
