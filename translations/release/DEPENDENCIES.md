---
title: "Reading Dependencies: Glossary Links and Release Boundaries"
sources: ["Knowledge Contract project corpus and publication edition"]
status: repository dependency record; not rendition admission
updated: 2026-11-09
---

# Reading Dependencies: Glossary Links and Release Boundaries

The initial extraction of twenty reviewed translations omitted two files that their existing links require. The ordinary link job in run `42593994509` found exactly two missing local targets: the final glossary link in each full Contract Checks translation. The separately executed readiness run `42593994174` passed all eighteen synthetic controls and the complete twenty-target source/title comparison. A successful identity comparison did not hide the link failure.

This correction restores the **already authored glossary bodies unchanged** from translation snapshot `34405422aad944fab20f96bcecd863f7bad7cd59`. It does not edit a reviewed study, invent a stub, weaken link checking or substitute an English document under a translated-body label.

| Auxiliary file | Exact restored Git blob |
| --- | --- |
| `translations/ru/reference/glossary/GLOSSARY.md` | `81364f076440f58680c5ef4770fdb6b3a66d73f1` |
| `translations/zh-Hans/reference/glossary/GLOSSARY.md` | `72015a328dbbd9af4ad3872887b571f7a123ebf9` |

These two files retain their original author-draft metadata and historical source pins. **They are not added to the twenty-pair reviewed release manifest**, not newly reviewed, not current-source certified and not admitted as website renditions. Thus this repository extraction contains twenty reviewed bodies plus two existing draft glossary dependencies; it is not twenty-two reviewed translations. The current authoritative English glossary and its accepted Russian/Chinese terminology crosswalk are at [Shared Vocabulary](../../reference/glossary/GLOSSARY.md).

The source-language glossary has evolved beyond a title change, so the source/title-only preparation tool must not repin these auxiliary bodies as if their full semantics had been rechecked. Their later full-text reconciliation remains translation work. A website compiler must either resolve a glossary reference to the actual current canonical work with an explicit English fallback, or use a separately admitted full rendition. It must not claim these historical draft bodies are the current published translations merely because the files exist in the source tree.

Any mechanical site-link normalization must identify the same logical work and relevant anchor, preserve historical evidence URLs, and record the exact link-only delta. If that delta changes meaning or scientific prose it returns to KC-Brain. This correction changes no historical review, corpus allowlist, index state or production deployment.
