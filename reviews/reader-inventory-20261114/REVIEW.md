---
title: "Reader Inventory: Source Counts and Translation Boundaries"
sources: none
status: internal-review-findings-resolved; external-review-pending
updated: 2026-11-14
---

# Reader Inventory: Source Counts and Translation Boundaries

## Scope and source

KC-Brain prepared this bounded editorial reconciliation under Pavel Valentov's direction to continue the Knowledge Contract roadmap. It reconciles current reading guides with the source snapshot at `6a6f202f7f70be2ad3aea3369e45409761708596`; it does not author new manuscript translations or change catalogue membership. The complete catalogue, translation paths and rendition metadata at that revision are the inputs. A separate agent prepared these edits under the same controller; this is not an external independent review or native-speaker certification.

The source snapshot contains 31 catalogue documents, 26 canonical body files in each of Russian and Simplified Chinese, and eight sidecar entries with recorded agent reviews. The 52 present files out of 62 work-language slots are a file inventory. They do not establish body completeness, fidelity to the latest English source, rendition admission, native-speaker review, served pages or index admission. The eight review records retain their original subjects, bindings, scope and limitations; no review was created or repinned by this change.

The two additional catalogue documents proposed in PR105 are not in this source snapshot. A future 33-document catalogue needs a new inventory at its own commit. The programme target of 34 works remains a third, planned scope.

## Exact edited paths and dispositions

| Paths | Previous reader-facing statement | Reconciled statement |
| --- | --- | --- |
| `PROGRAMME.md`, `guides/programme.ru.md`, `guides/programme.zh-Hans.md` | The 31-work catalogue is a PR89 proposal; 30 works remain accepted until integration. | The pinned source catalogue already contains 31 works; both foundations retain research-draft status. The 34-work target remains planned. Add the bounded translation inventory and distinguish recorded agent reviews from native review and website delivery. |
| `roadmap/TRANSLATIONS.md` | The older source/proposal union is presented as current: four body files on main and 25 in PR76 per language, six absent per language. | Add the distinct `6a6f202f` source snapshot: 26 present per locale, five absent, 52/62 overall. Preserve the historical table, its exact pins and the historical 50/60 denominator. |
| `ROADMAP.md`, `roadmap/ROADMAP.ru.md` | Current translation work still uses the older 25-file proposal and 12 missing files. | Bind the reader inventory to `6a6f202f`: ten missing files, separate review/admission states, PR105 excluded from the denominator. |
| `README.md` | The catalogue and Meaning Bridge are still described as proposed for integration; the broader translation paragraph leads with the historical 50/60 count. | Describe source integration without changing scientific status, lead with 52/62 at the exact snapshot and retain PR76 as history. |
| `READING.md`, `guides/READING.ru.md`, `guides/READING.zh-Hans.md` | The catalogue is called proposed; readers are directed only to the older translation PR for prepared texts. | Identify the source snapshot, link the current inventory and pinned locale source directories, and retain PR76 as history. Repository availability is distinguished from served website pages. |
| `DOCUMENTS.md`, `papers/README.md` | Meaning Geometry or the two foundations are described as PR89 catalogue candidates awaiting integration. | State their presence in the pinned source catalogue while retaining research-draft and scoped-review limits. The Meaning Geometry disposition distinguishes its bounded mathematical review from broader scientific acceptance and the separately recorded source/site state. No document names or scientific text are changed. |
| `SOURCES.md` | No registration for this new inventory's JSON output. | Register the two newly produced inventory records against the exact project source snapshot. Existing source registrations are preserved. |

Historical review and evidence files, `publication-catalog.json`, `publication-renditions.json`, canonical manuscripts, translation bodies, naming metadata, requirements, dependency graph and task states are unchanged. Site manifests, deployment, index and served-page claims are outside this edit.

## Inventory observation

The unmodified existing reporter was executed twice against the same exact source, base and draft commit; the output was byte-identical. Using the same base and draft counts the already integrated tree once through the reporter's union rule. Its exact stdout is retained as [current-file-inventory.json](current-file-inventory.json). [inventory-checks.json](inventory-checks.json) records the catalogue and sidecar blobs, report digest, missing paths and bounded checks.

The historical `0892eeb1` / PR76 `9723b478` report was also reproduced with the existing tool. Its four base files, 25 proposal files and six missing files per locale agree with the retained table. Every old union path is present in the new source snapshot; Knowledge Utility contributes the additional path per locale. The historical table's bytes and old review/evidence records remain unchanged; only its surrounding presentation now identifies it as historical.

The current missing titles and paths were compared directly with the catalogue: Meaning Bridge, Interaction and Memory, Evidence and Falsification, Knowledge Reuse and Meaning Geometry, each in both locales. Body completeness and translation fidelity were not inferred from paths.

## Internal review and dispositions

The controller received the internal review from a separate agent, `mailbox_status`, which confirmed all 16 candidate-file hashes and independently recomputed the pinned inventory: 31 source documents, 26 files per locale, 52/62 slots and eight sidecar entries with recorded agent reviews. This is a separate checking pass within the same controller, not external independence or native-speaker certification. The three remaining reader-text findings were addressed with the requested bounded changes:

1. `guides/programme.zh-Hans.md`: the closing paragraph now refers to three remaining planned engineering works, and distinguishes Meaning Geometry's research-draft status from broader scientific acceptance.
2. `PROGRAMME.md`: the final sentence no longer describes Meaning Geometry as awaiting source-catalogue integration; it retains the bounded draft status and requires separate review/decision for broader acceptance or a status change.
3. `papers/README.md`: the Meaning Geometry disposition states the six-deduction/countermodel review scope without conflating that review with source integration, website delivery or index admission.

These three findings are resolved in the local candidate. The inventory reports and source pins are unchanged, so a repeated whole-inventory audit is not claimed or needed for this prose correction. External peer review and native-speaker review remain unperformed.

## Verification and remaining review

Local checks used Python 3 and the pinned Pandoc 3.1.3 renderer. The first source gate correctly refused the two unregistered new JSON inventory files. After adding their provenance row to `SOURCES.md`, all four final gates passed. The initial failed observation is retained in the working validation log rather than reported as an initial success.

| Check actually performed | Result and scope |
| --- | --- |
| `python3 -B tools/check_publication.py .` | PASS: catalogue, document metadata, local Markdown links, evidence references and hashes. |
| `python3 -B tools/check_sources.py .` | PASS after registration of the two new JSON records. |
| `python3 -B tools/check_requirement_register.py` | PASS: 349 requirements, unchanged register. |
| `python3 -B tools/check_document_names.py` | PASS: names, catalogue, front matter, H1 and readable roadmap identity. |
| Existing publication/source/separation/DCO/CI unit suites | 93 tests passed. No new implementation-mirroring test was added for these prose edits. |
| Exact-ref inventory and preservation checks | Two byte-identical current reports; historical counts reproduced; missing paths matched to the catalogue; historical table unchanged. |
| Changed-path scope and `git diff --check` | PASS: only the named reader/provenance files and the three new inventory/review files changed; no whitespace error. |
| Offline Markdown lint attempt | NOT_RUN: `markdownlint-cli2@0.24.0` was not in the npm cache (`ENOTCACHED`). No Markdown-lint success is claimed. |

The first hosted CI result and its bounded follow-up are recorded below. The result at the next submitted revision must be checked directly; no result from another head is transferred here.

After applying the three internal-review corrections, one publication gate with Pandoc 3.1.3 passed, and `git diff --check` passed. The earlier broader checks retain their stated scope. A review by another agent under the same controller remains internal. No fresh full-body translation review, external peer review, native-speaker review, website build, visual acceptance, deployment or index check is claimed.

## First hosted CI failure and retained-history follow-up

[PR106](https://github.com/Arcanada-one/knowledge-contract/pull/106) was submitted at `b6b8f45023bfd6e35f0623bd6a263f5f94770767`. Its [corpus-map job](https://github.com/Arcanada-one/knowledge-contract/actions/runs/43553772801/job/132321888032) failed while running the unchanged `tools/verify_corpus_map.py --repo .`: structural validation was true with no structural errors, but the F01 source object at `61d674244f70002e20506b387b210fd584074ad2:papers/human-meaning-and-computable-knowledge/PAPER.md` was absent and the retained-map blob could not be confirmed. All other listed source-object checks were true. This was an actual first hosted failure, not a successful run or a change to the translation counts.

The local Git graph confirms that this F01 commit is outside the ancestry of source `6a6f202f`; the other six source commits are ancestors. A full branch-history checkout therefore need not contain F01. The same missing-history case had already been repaired in [PR105's workflow at dec63e46](https://github.com/Arcanada-one/knowledge-contract/blob/dec63e4631d1b02e7b22bbc2e780c41cd6a7bfd7/.github/workflows/ci.yml). That existing fix was absent from main and from the main-based PR106. This follow-up reuses its exact step, rather than claiming a newly discovered validator defect:

```sh
git fetch --no-tags origin 61d674244f70002e20506b387b210fd584074ad2
```

The step runs immediately after the `corpus-map` job's full-history checkout. No map, source pin, expected retained blob, validator, projection or refusal condition changes. The retained F01 map still has to match `f67ae8f491cb82a72703de9a2143b3620f5b9291` through the original validator. The source-history repair changes only `.github/workflows/ci.yml` and this review record relative to the first PR106 submission; the other fifteen submitted files remain unchanged.

A local control used the real repository objects and a disposable Git remote whose only advertised branch was main. Its fresh, non-shallow clone reproduced the exact F01 source-object and retained-blob failure. Executing the fetch command extracted from the edited workflow made both the unchanged /1 map and /2 inventory candidate pass their original source-object checks. A separate input with a deliberately wrong retained blob still failed with exit 1. HEAD and tracked worktree state were unchanged by the fetch. The 35 existing CI-workflow tests also passed. This is a local file-transport check; the follow-up's GitHub fetch and complete hosted CI still require observation at its own new head. The inventory and earlier editorial review were not rerun or upgraded by this repair.
