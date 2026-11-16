---
title: "Agent Situation Renditions: Source Fidelity and Catalogue Integration"
language: en
sources: none
status: author-prepared; independent language acceptance and site delivery not established
updated: 2026-11-16
---

# Agent Situation Renditions: Source Fidelity and Catalogue Integration

## Conclusion

This candidate adds the full Russian and Simplified Chinese bodies of
[Agent Situation](../../../papers/agent-situation/PAPER.md), a research draft in
the existing Agent State priority. It also repairs a reproduced catalogue
metadata integration failure. Neither change supplies independent scientific
or linguistic acceptance, a new experiment, a website deployment or runtime
admission.

The isolated parent is Knowledge Contract PR104 head
`89382a5fa70d361ab906d44c7c4ea2b6ea28bc83`. That parent remains unchanged for its
existing review. The canonical English source is main
`8c7cd3bc1247998cb9554c568da26949da31b749`, paper Git blob
`93a11fb3ad161a5ed3ed817636035ed0556a46fd`, SHA-256
`f04471d2b66bbb0d2ac64e41325bbd9367fd2f5d49f40bb90235beae2ff81677`.

| Target | Body SHA-256 | Git blob |
| --- | --- | --- |
| [Russian](../../../translations/ru/papers/agent-situation/PAPER.md) | `aace3a61cb4d211e20d5359d90c0975d0d1e8d8c79a6d8a465ed88cc32a271da` | `9cdbb6eecda7cb5e4891a6c67042545d778c8a7e` |
| [Simplified Chinese](../../../translations/zh-Hans/papers/agent-situation/PAPER.md) | `092dbc4c61f6fea0799c2a6152e629b5c1b5fb21697cf1a48f2aa12ef4aedca3` | `ff08de59ebd9a948546a84449001b5f43fa42f8e` |

The exact content commit and sidecar bindings are recorded in the subsequent
integration section after remote content readback. Until then these are
prepared bytes, not files asserted to exist at the parent commit.

## Improvement applied

### Complete bodies and bounded producer review

The authoring controller read the English source and both complete renditions.
Two analytical helpers prepared language drafts; a third checked structural
parity. All share the same controller and are producer assistance. This is not
independent or native-speaker acceptance. Internal document names were aligned
with the existing localized catalogue, while reference destinations and
external bibliographic identities were preserved. The Russian phrase for a
fixed reader was kept as a reading component, without narrowing it to a model.

The read-through retained the distinction between unknown and false, receipt
and external completion, observation age and receipt time, source revision
comparison and authority, and declared dependency closure and graph
completeness. All conditional premises and the later check/effect race remain.
Abstract integer costs remain distinct from measured tokens. The planned
agent comparison remains unexecuted; the finite study remains author-produced.
No gain in task performance, cost, production use or independent replication
is added by translation. The 21 cited external works are translated from the
canonical synthesis, not independently reverified by this increment.

The [producer validator](producer_validate.py) reuses the actual parser and
rendition checks from site commit
`d3d17929f209612669f38db6a735d46bc9ec309c`, with exact checker hashes and Pandoc
3.1.3. Its [local result](producer-result.json) records explicit staged inputs:

| Checked population, per language | Observed result |
| --- | --- |
| Top-level block sequence | 79 corresponding blocks |
| Heading levels and canonical GFM anchors | 18, including the title; 17 section mappings |
| Paragraph/list/cell boundaries | 57 Pandoc Para nodes, including one display-formula paragraph; 56 prose paragraphs; five observation-list items |
| Tables | Three; 7, 14 and 8 rows including headers; three cells per row |
| Mathematical expressions | 15 inline and one display, exact TeX and order |
| Links and attribution | 32 links to 31 distinct targets; all 22 front-matter source identifiers retained |

Fifteen scoped adverse checks were detected: seven mutations per locale and
one wrong source digest. They cover section/paragraph loss, a missing table
row, a changed budget formula, an unre-based relative link, swapped table-row
numbers and a false source commit. These are structural controls, not fifteen
scientific experiments. Paragraph parity cannot detect a lost clause or
negation; that limitation remains explicit in the executable result.

### Actual catalogue consumer failure and repair

The current English catalogue contains 36 works. The parent metadata sidecar
still described 31 works with 62 locale records and the older catalogue pin.
Executing the site's real `compile_localization` on the parent produced
`LOCALIZATION_INVALID: catalogue localization is stale for the current catalogue`.
Changing only the catalogue pin still fails on stale source hashes. Rebinding
those hashes without adding the five missing work pairs still fails the
complete work/language inventory.

The repair adds ten title/summary records for Agent Situation, Semantic Bridge,
Semantic Verification, Context Controls and Source Rule Checks. It retains the
existing 62 translated titles, summaries and unreviewed statuses exactly. Ten
metadata source hashes are rebound for five existing works whose English
bytes changed while their catalogue descriptions stayed identical. This
metadata-only rebinding does not refresh the corresponding manuscript
renditions or their review records.

The [consumer replay](check_catalogue_metadata.py) compiles all 72 metadata
records and rejects eight specific defective sidecars through the unchanged
site consumer. [The result](catalogue-metadata-result.json) retains the actual
failure, partial repairs, missing Chinese record, wrong hash, English title,
fabricated review and duplicate work/language-entry cases. Its isolated byte injection
changes only the tested sidecar input; source reads and Git ancestry checks
remain real. The workflow now invokes both new checks explicitly.

An omission in the earlier file-coverage increment is now exposed: passing
body checks did not exercise this 36-work metadata migration. The prior
successes remain valid for their declared source-body scope; they never proved
a complete site release. This increment applies the existing localized-release
method to the actual downstream metadata consumer and adds that execution to
CI, without changing scientific acceptance rules.

During preparation, the source-declaration gate refused four newly added
control/evidence files before their origin row was supplied in `SOURCES.md`;
the subsequent source check passed. A local unit-test command initially named
nonexistent `tools.test_sources` and `tools.test_dco` modules: the run failed
with two import errors while the 35 workflow tests passed. The corrected
invocation uses the actual four modules named in the repository's licensing
workflow and passed all 76 tests. Neither initial refusal is counted as a
successful full test run. A later source-check invocation from the scratch
parent directory failed to locate the script; invoking it from the repository
directory succeeded.

## Remaining release boundaries

The cumulative candidate has 68 body files out of 72 catalogue-language slots.
Semantic Bridge and Semantic Verification still lack both target bodies.
Ten of the retained rendition records bind earlier English bytes: two locales
each for Knowledge Transformations, Evidence and Falsification, Meaning
Geometry, Research Foundations and Source History. Their fidelity to changed
English sources needs its own comparison; merely updating a hash would not
establish it. File presence, source currency and linguistic review are
different inventories.

The pinned site builder also rejects the new source status values
`engineering-draft` and `internally-reviewed-finite-evaluation`. Those source
statuses are preserved. The catalogue consumer success is not a complete site
build. A [seven-file downstream patch](site-status-support.patch) now provides
both statuses with precise EN/RU/zh-Hans labels and notices, preserving their
limited meaning. Its [actual local receipt](site-status-result.json) records
18 Python tests and 506 existing/new Node cases, including nine status/locale
fixtures through the actual app functions. The final patch applies cleanly to
both the pinned checker and site head `b59e1fc38d8d2b84697537fb86453538dc66cfda`.
This is prepared source, not an installed site change. The [handoff](SITE-INTEGRATION.md)
and [remaining checks](SITE-TEST-PLAN.md) retain the separate 31-to-36 work
inventory/type-count migration, full build, indexing and served-page boundaries.
The currently published 31-work source pin is not changed here.

The existing parent PR must finish its own review before a dependent candidate
can be retargeted to main and checked as a release subject. New renditions
remain author drafts without review objects. The 66 prior rendition entries,
including eight historical review objects, must remain unchanged when the two
new bindings are registered. Content, publication decisions and index
allowlists remain separate changes. No native build or deployment is claimed.

## Idea and next use

The owner should review each full language body against the pinned English
source, then exercise the resulting registered renditions and 72 metadata
records through the site's current consumer. The site owner can use the
separately identified status-support patch and its tests on the actual next
release head. The intended reader benefit is complete, traceable text and
consistent cards in the selected language; it must be observed on generated
and served pages after release. Cost and user benefit are NOT_MEASURED.

Rollback is a new reviewed commit reverting this candidate's two bodies,
metadata update, two sidecar additions and associated workflow steps while
retaining these historical observations. Do not rewrite the parent review or
the original 31-work release evidence.
