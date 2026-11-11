---
title: Contract Place roadmap - prepared delivery specification
sources: none
status: prepared implementation request - deployment unverified
updated: 2026-11-06
---

# Contract Place roadmap delivery

> Current editorial note, 8 November 2026: names replace opaque reader-facing labels; compatibility mappings are in [workstreams.json](workstreams.json). The foundations introduction already exists as a research draft. The operator resumed engineering availability on 11 November 2026; [Active Work](EXECUTION_STATUS.md) governs present execution. Site/build changes still follow actual review, CI and deployment gates. Future research is not an unbounded release gate.

**Owner of content:** KC-Brain. **Independent architectural review:** Agent-Brain. **Necessary site/server execution:** KC-SWE. This is the prepared scope for Roadmap Publication, with task bindings reconciled by Workgraph Reconciliation. It does not request new theory authorship from an engineer.

## 1. Source and publication boundary

Use the reviewed, actually merged Knowledge Contract commit containing `ROADMAP.md` and `roadmap/`. Read current site instructions before implementation. The existing site README describes a pinned `publication-manifest.json`, `scripts/build_publication.py`, generated `src/content/catalog.json`, `src/site/content-provenance.json` and the deployed `public/` tree. Preserve that provenance discipline.

Roadmap material is a separate reading collection. It is not a scientific paper, a passed experiment, a runtime protocol version or automatically an API/corpus allowlist input. The inspected baseline catalogue at `717c43deb514adc5b40f76837e7ee0fb2da37102` contained 29 documents; this is historical evidence, **not a permanent count guard**. Do not add nonexistent planned papers to `publication-catalog.json`, silently alter a source catalogue or hard-code 29 after a later accepted catalogue revision. Use the actual reviewed and merged catalogue pin for current site document counts, and keep any proposed research-draft addition distinct from accepted public or index status. Add roadmap build inputs and provenance explicitly rather than hand-editing generated HTML. The source commit used for the roadmap and the manuscript pin are both visible if they differ; do not imply they are identical. As of 11 November, Knowledge Contract main `0892eeb1` contains 31 documents and site PR33 merged/deployed `f4b0eab1`; the earlier 29 count is historical and index admission remains unverified.

No secret, private mailbox URL, internal server path, credential, unpublished source-book payload or private task identifier belongs on the public page. Public RM IDs and sanitized owner roles suffice.

## 2. Reading surface

Proposed canonical routes are `/en/roadmap/`, `/ru/roadmap/` and `/zh-Hans/roadmap/`, consistent with existing language-prefixed navigation. Confirm their compatibility with the actual router. Link the section from primary navigation and the project overview. Preserve existing science, engineering, reference and appendix routes.

The page contains a short introduction, the two-track release policy, the current gap map, priority bands, all 25 task cards, their dependency relationships, acceptance/refutation criteria and a link to the versioned source. Show the author's current [foundations-first preparation sequence](FOUNDATIONS_RELEASE_PLAN.md) Meaning Bridge–Meaning Controls as a distinct editorial ordering policy, not new Muneral tasks or inferred DAG edges. Clearly mark the earlier roadmap-only restart checkpoint as superseded; the default resumption threshold is the complete reviewable six-unit package and a version-pinned corpus link map described in [ROADMAP.md](../ROADMAP.md) §2, not successful completion of all future research, site publishing or model experiments. Keep explicit later per-document author permissions and the independently authorized Roadmap Publication/first-two-paper/defect-fix work visible as exceptions. Provide stable anchors for Claim Atlas through Editorial Release and an accessible text/table alternative to any visual graph. The initial full task text is English; localized navigation is not presented as a translated manuscript. A Russian translation of the overview can be added with an explicit language label and review state.

Suggested public introduction:

> Knowledge Contract publishes bounded scientific and engineering results while maintaining a transparent research programme. This roadmap distinguishes existing evidence from planned work on human meaning, formal representations, algebra, geometry and practical verification. A planned task is not a completed result; negative or inconclusive findings will be preserved and reflected in future revisions.

Suggested navigation label: `Roadmap` (English), `Дорожная карта` (Russian), `路线图` (Chinese interface; native-language editorial review not claimed).

Do not promise completion 'soon' as a date-backed fact. Use priority and dependency order until actual estimates are accepted. Empty/unverified task status is shown as planned or unknown, never as active/completed. Where execution state is synchronized, display its observation time and source; Workgraph Reconciliation retains one execution authority.

## 3. Implementation and validation

Reconcile existing site work before creating a new work item. Implement only the required route, content compilation, navigation and provenance changes on the authorized development host. Pin source bytes, include generated outputs through the normal workflow, preserve the design system, local assets, CSP and search behavior, and run current project checks.

Required checks include:

1. All 25 RM IDs appear once as cards; every required and advisory edge resolves; priorities and owners match the canonical task definition. Broken or cyclic required dependencies are rejected or visibly diagnosed. Meaning Bridge–Meaning Controls appear only as the distinct current preparation order with an exact plan reference; the graph does not silently add F tasks or geometry prerequisites to the Live Lab baseline.
2. The actual generated HTML contains the introduction and substantive task text without requiring script execution to reveal all content. Anchors and source links work; the roadmap has an accessible reading order and mobile layout.
3. A deliberately stale source pin, missing task, changed dependency and absent execution evidence cannot produce a false completed-state view. Status projection is not an editable second tracker.
4. Existing paper/specification/study pages, citation metadata, equations, references, search and compatibility routes do not regress. Site integrity, link, hygiene, security and publication checks run at the actual changed commit.
5. The source PR and site PR retain proper attribution, licenses and contributor DCO. Review and CI are not bypassed for speed. Deployment uses the established Publisher/deployment route.

After deployment, read the live roadmap and its provenance, then a representative paper, specification and study. Check the actual source IDs, not just HTTP 200. Compare served task text and counts to the committed source, inspect desktop/mobile rendering, check cache behavior, canonical metadata, sitemap and language links. A screenshot alone does not prove data provenance; a build log alone does not prove what is served.

## 4. Required mailbox result

Return one substantive result to KC-Brain, copying Agent-Brain when it affects the integration design: actual reconciled task references; source and site commits; PR/review/CI evidence; deployment identity; real live page URLs; readback comparison; desktop/mobile observations; unchanged-publication/index boundaries; and each remaining failure or unmeasured check. Do not report deployed merely because the PR merged.

The publication request is authorized by the operator. Missing future algebra/geometry results do not block this page: it reports their planned status. Existing first/second-manuscript reviews and publication, permitted material-defect fixes and already explicitly authorized third-and-later editorial work are not cancelled by the earlier roadmap-only hold. Show the revised preparation order without claiming that all six manuscripts, their reviews or deployments are complete. Site delivery is independent of finishing that sequence; do not dispatch the entire research programme merely because its cards now exist.
