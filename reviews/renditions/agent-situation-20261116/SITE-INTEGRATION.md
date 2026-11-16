---
language: en
sources: none
status: prepared downstream patch; independent review and production integration pending
---

# Two canonical publication statuses: bounded site handoff

## Concrete finding and candidate

Both inspected site revisions reject source statuses that already exist in
Knowledge Contract `8c7cd3bc1247998cb9554c568da26949da31b749`:

| Canonical work | Exact source status |
| --- | --- |
| `semantic-bridge` specification | `engineering-draft` |
| `semantic-bridge-conformance` study | `internally-reviewed-finite-evaluation` |

`scripts/build_publication.py:33,113–114` accepts only `research-draft`.
The rendering and independent label maps likewise know only that status. This
is a concrete source/site compatibility gap, not a translation failure or a
reason to change the canonical status to fit the old compiler.

`site-status-support.patch` is a seven-file candidate: five implementation
files and focused additions to the existing Python/Node test suites. It was
applied and tested only in an isolated local clone of pinned checker
`d3d17929f209612669f38db6a735d46bc9ec309c`. The final patch also passes
`git apply --check` on both that original tree and site
`b59e1fc38d8d2b84697537fb86453538dc66cfda`; both originals remain clean.
The patch is 26,471 bytes, SHA-256
`1864016dd6ca50a30b724ec6530fc35483db17bca47762f528333e3b64db51f6`.

## Source and consumer map

| Surface | Exact implementation | Required disposition |
| --- | --- | --- |
| Source schema/allowlist | `scripts/build_publication.py`, `STATUSES` and `load_inputs()` | Add the two exact values; preserve rejection of unknown values, source identity and clean-checkout checks. |
| Independent output checker | `scripts/publication_checks.py`, `STATUS_LABELS` and `check_status_labels()` | Add all three locale labels. Existing checks still require badges beside displayed works and a reading-page notice. |
| Programme/roadmap HTML | `scripts/programme.py`, `STATUS_LABELS`, `localize_and_badge_links()`, `roadmap_linked_status()` | Add matching labels so known new statuses are not skipped on linked-work displays. |
| Runtime and prerender UI | `src/site/app.js`, `statusLabels`, `statusNotes`, `statusOf()`, `statusBadge()`, `statusNote()` | Add translated labels and bounded explanations. Existing shared functions cover cards, reader metadata/notice, sibling links, lists, repository rows, local search and page titles. |
| Machine-readable reading index | `build.mjs`, `llms.txt` generation | Replace the one-size-fits-all `not an accepted paper` suffix with status-specific descriptions; retain the existing research-draft output exactly and reject unknown descriptions. |
| Catalogue status transport | `scripts/publication_catalog.py:74–91` | Already preserves the exact raw status. No change; status-bearing records do not join the implicit accepted-document cover sequence. |
| Public manifest | `build.mjs:86–87`, `scripts/check_publication.py:73` | Already carries `status` into `publication.json` and checks equality to the compiled catalogue. No change. |
| Structured metadata | `src/prerender.mjs:83`, `creativeWorkStatus` | Already emits the exact source enum. Do not translate or replace this machine identifier. |
| Discovery and category filters | `src/site/app.js`, `home()`, `referenceResults()`, `publicationList()`, `searchItems()` | Existing type/category filters remain; the home paper selection still excludes every record with a nonempty status. No new accepted-paper category is introduced. |
| Localized title checker | `scripts/check_localization.py:487–488` | Consumes `publication_checks.STATUS_LABELS`; the new labels must match the rendered title suffixes. No separate enum change. |
| Body rendition display | `src/renditions/renditions.js`, existing source-record wrapper | Uses the shared source record and preserves status notices while replacing language-specific content. No rendition-state mutation. |
| SEO/sitemap/hreflang | `src/prerender.mjs:18–28,50–56,98–103`; `publication_checks.check_rendition_indexing()` | Keep the independent rendition-review decision unchanged. A publication status containing `internally-reviewed` must not turn an unreviewed translation into a reviewed or indexable translation. |
| Search service | `src/site/search.js` API `status` and full-revision comparison | A different status domain: backend snapshot/currentness. Do not map publication enums into it or claim API index admission. |

`draft-notice` remains the existing CSS/checker hook for a bounded publication
notice; the visible text for the finite-evaluation status does not call it an
unreviewed research draft. No CSS/layout redesign or new status filter is needed
for this bounded source change.

## Proposed labels and meaning

| Status | EN | RU | zh-Hans |
| --- | --- | --- | --- |
| `engineering-draft` | Engineering draft | Инженерный черновик | 工程草案 |
| `internally-reviewed-finite-evaluation` | Internally reviewed finite evaluation | Конечная оценка с внутренней рецензией | 经过内部审查的有限评估 |

The engineering notice excludes accepted-specification, implementation
conformance and production-readiness claims. The finite-evaluation notice limits
the findings to stated cases and assumptions and explicitly excludes independent
scientific acceptance, general correctness and production validation. Original
`research-draft` labels, notices and exclusions are unchanged. These new UI
translations are producer wording, not independently admitted translations.

## Separate source-inventory work

This patch intentionally retains publication pin
`39e4054830d9cb05bc0432d25f7320cb8a97f054` and its 31-work release.
It does not add the later five works or regenerate files. A future 36-work
adoption also needs the established release owner to reconcile its expected
inventory with the actual accepted source:

- `scripts/check_publication.py:20–23` pins the old type counts
  (10 papers, 11 specifications, 6 studies, 1 glossary, 1 bibliography, 2 appendices).
- The same file at line 30 requires 31 records; its line 74 prints 31 works/93
  reader pages.
- `scripts/check_papers.py:110–111` separately requires 31 records.
- README inventory and coverage prose describe that old source snapshot.

These are valid current-snapshot checks, not failures to remove. Bind successor
expectations to the adopted catalogue and preserve exact population coverage;
do not weaken the checks merely to permit a build. Local support for two enums
alone cannot establish that a 36-work release is ready.

## Verification actually performed

Read exact source paths at both named site revisions and the current knowledge
catalogue. The final candidate passed:

| Actual check | Result and scope |
| --- | --- |
| `python3 -B scripts/test_build.py -v` | 18 tests passed. Includes committed synthetic source-status preservation, unknown-status refusal, original pin/dirty-source checks, all three locale labels, adverse badge/notice controls and programme/roadmap joins. Existing rendering checks also ran. |
| `node scripts/test_ui_localization.js` | 506 cases passed. Includes nine status × locale cases: six for the two new statuses and three unchanged research-draft cases; reader notices, titles, cards, lists, repository rows, search and roadmap links use actual app functions. |
| Bounded `llms.txt` consumer | The Node suite executes the actual emission block with fixture documents and a captured file write. Finite internal evaluation receives its own limitations, never the generic accepted-paper suffix; unknown status refuses. This is not a full build. |
| Original snapshot boundaries | Both original working trees are clean; final `git apply --check` passed on both exact heads. Publication pin and generated files remain unchanged. |

The tested environment was Python 3.12.14, Node 24.22.1 and Pandoc 3.1.3.
An initial Python run used the environment's Pandoc 3.1.11.1 and also passed;
that preliminary probe is explicitly superseded in `site-status-result.json` by
the successful rerun with the repository-required 3.1.3 binary. Exact command
outputs, tool versions, file/blob hashes and patch applicability are retained in
`site-status-result.json`, `site-status-bindings.json` and `logs/`.

The new status checks use reversible synthetic status overlays on the pinned
31-work content. They preserve rendition state and accepted-paper exclusion.
The existing Node suite also prerenders that unchanged corpus in a disposable
directory; it does not build or validate a 36-work release.

No full native build, actual successor-source compilation, browser layout check,
hosted CI, publication, source-pin adoption or remote write was performed.
This is same-controller producer QA, not independent scientific or release
acceptance. The existing KC-SWE release lane owns integration and the remaining
checks in `SITE-TEST-PLAN.md`; this handoff creates no new task identity, worker or
publication authorization.
