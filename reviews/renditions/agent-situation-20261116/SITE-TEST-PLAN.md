---
language: en
sources: none
status: prepared downstream patch; independent review and production integration pending
---

# Status support: completed checks and remaining integration plan

The executed portion is recorded in `site-status-result.json` and `logs/`. The rest
belongs to the existing KC-SWE release lane after adoption of an exact successor
source pin. These checks do not authorize that adoption or establish independent
scientific acceptance.

## Executed on the exact patch in an isolated d3 clone

```sh
python3 -B scripts/test_build.py -v
node scripts/test_ui_localization.js
```

Use Python 3, Node 24 and Pandoc 3.1.3 on PATH. The actual receipt records Python
3.12.14, Node 24.22.1 and Pandoc 3.1.3. Both commands exited zero: 18 Python tests
and 506 Node cases. The patch adds four net Python test methods and 15 Node cases
to the existing suites; it also moves the existing unknown-status source test
out of the generated-catalogue-dependent class so it always executes.

1. **Compiler source identity and status.** A committed synthetic catalogue
   passes through the real `load_inputs()` with a research-draft paper,
   engineering-draft specification and internally-reviewed-finite-evaluation
   study. Exact type/status pairs survive. Unknown `accepted-ish` is refused.
   Existing clean/unmarked input, wrong pin and dirty-source controls remain.
2. **Actual app, all three languages.** Nine status × locale cases verify reader
   badge, full notice, page-title suffix, card, listing, repository, local search
   and roadmap output. Expected strings are separate test data. Research-draft
   wording is unchanged; finite evaluation explicitly limits its scope and
   excludes independent scientific acceptance. Unmarked records have no status
   badge/notice; unknown status refuses in both reader and search rendering.
   Status-bearing records remain excluded from the accepted-paper count, and
   status overlays leave rendition states byte-for-byte unchanged.
3. **Output-checker sensitivity.** All three statuses in all three languages
   pass first. Removing each badge, replacing it with `Accepted`, or removing
   each reader notice causes the expected refusal. Existing research-draft
   stray-badge and Chinese-full-stop controls also pass.
4. **Programme and roadmap.** Both actual Python link renderers retain each of
   the nine status/locale labels and localized destinations. Removing the added
   programme badge reproduces the unchanged source prose exactly.
5. **Machine-readable descriptions.** The actual contiguous `build.mjs`
   `llms.txt` emission block executes on fixture documents with a captured write.
   Research-draft output is unchanged, engineering and finite-evaluation
   limitations are distinct, finite evaluation does not receive an accepted-paper
   classification, unmarked output remains unmarked, and unknown status refuses.

The ordinary UI suite additionally checks current language/anchor navigation and
uses the actual prerenderer in a temporary directory on the unchanged 31-work
content. That baseline prerender is separate from the new-status VM fixtures.

## Remaining source-adoption checks

Before a later 36-work release, reconcile the exact adopted source population:

- `scripts/check_publication.py` currently pins 31 records and type counts
  10/11/6/1/1/2 for paper/specification/study/glossary/bibliography/appendix.
- `scripts/check_papers.py` independently expects 31 records.
- README and the checker summary describe 31 works/93 localized reader pages.

These gates are valid for the unchanged current pin
`39e4054830d9cb05bc0432d25f7320cb8a97f054`. Bind replacement expectations to the
actual successor catalogue; retain exact coverage instead of weakening the
checks. This patch deliberately does not change pin, counts or generated files.

Compile the accepted successor through the full `scripts/build_publication.py`
path. Verify exact status equality from canonical catalogue through compiled
records, `publication.json`, reader `creativeWorkStatus` and generated `llms.txt`.
Verify rendition review, noindex, sitemap and hreflang remain governed by their
own source/review bindings. A publication status containing `internally-reviewed`
must not promote an unreviewed translation or backend API snapshot state.

Retain the ordinary publication/hygiene/page/paper/link gates and existing suites:

- `python3 -B scripts/test_build.py`
- `node scripts/test_ui_localization.js`
- `ROADMAP_SOURCE_DIR=<exact-roadmap-checkout> python3 -B scripts/test_roadmap.py`
- `PROGRAMME_SOURCE_DIR=<exact-source-checkout> python3 -B scripts/test_programme.py`
- `python3 -B scripts/test_localization.py`
- `python3 -B scripts/test_catalogue_localization.py`
- `python3 -B scripts/test_renditions.py`
- `node scripts/test_search.js`

Regenerate catalogue/provenance/public files through the compiler, verify
reproducibility and run ordinary hosted CI. Read all affected reader/list/search/
programme/roadmap surfaces in EN/RU/zh-Hans on desktop and mobile, especially the
longer finite-review badge and notice. After the established release owner
deploys, read actual served source revision, statuses, translated bodies,
notices and asset/cache identity. Those release checks have not been executed
by this local handoff.
