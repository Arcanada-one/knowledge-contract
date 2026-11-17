# Status evidence belongs to a reader component

17 November 2026. KC-Brain producer-side follow-up to the two findings in
[c141](https://github.com/Arcanada-one/knowledge-contract/pull/124#issuecomment-6943624263)
and [c142](https://github.com/Arcanada-one/knowledge-contract/pull/124#issuecomment-6944982296).
The source subject starts at `435700a963027ea433c3fe5e221b73c948592394`.
This is an engineering validation proposal, not a new mathematical theorem,
independent translation acceptance or a publication receipt.

## Problem and pre-change contract

The preceding site checker correctly distinguished work identities but kept
their labels in a page-global set. A status belonging to a different component
could therefore satisfy an unmet obligation. Correct work identity and text
also did not establish the effective language or explicit exposure of the
label. These are narrower properties than the earlier successful 36-work
build checked; the earlier receipt remains valid within its original scope.

The [pre-change contract](https://github.com/Arcanada-one/knowledge-contract/pull/124#issuecomment-6946018412)
names the actual layout boundaries, positive inheritance controls, adverse
mutations, immutable inputs, source-preservation constraint and rollback.
The test must exercise the actual site checker on temporary copies of generated
pages. A separately implemented synthetic predicate is insufficient to show
that the proposed production checker distinguishes those cases.

## Scoped obligation

For every required pair of a reader component and a work, require a status
witness belonging to that component. The witness must name that exact work,
contain its localized status label, have the selected effective language and
meet the declared static exposure conditions. A witness elsewhere on the page
does not satisfy the obligation.

This changes the quantification boundary: existence somewhere on a page is
weaker than existence within each required component. It does not require one
badge per arbitrary source link. The renderer defines which links share a
component and which have separate obligations.

| Renderer surface | Required scope |
| --- | --- |
| Paper card | Its own card; cover, title and read links may share the work's metadata badge |
| Specification or study row | Its own linked row |
| Reader's publication status | Its own heading component; a navigation badge is not a substitute |
| Scientific manuscript references | The matching reader's deduplicated sidebar summary, preserving scientific body HTML |
| Reader sibling navigation | The corresponding sibling link |
| Current locale navigation on its own reader | Reuses the separately mandatory own heading; only the matching active `.locale-chip` inside `.locale-flags` under `header#header` qualifies |
| Roadmap | The same `dd` field; repeated links to one work may share its field summary |
| Repository | The same table row, including separately rendered cells |
| Search | The same result link |
| Programme direct catalogue link | That link and its own adjacent status component |

Historical source links remain bound to their declared revision. A current
catalogue status must not be inferred for an older document whose bytes differ.
The publication source stays `6eec88097cf5255543c792e53c92f75c0d483728`; the
separate roadmap stays `55e279c43dc9bcf8732467a32661c2ac4b7cf920`.

## Correctness includes accepting legitimate markup

The HTML language algorithm inherits language from the applicable ancestor
when an element has no local language declaration. An explicitly empty `lang`
instead indicates unknown language. Consequently a missing inline `lang` is
not a sufficient counterexample. The control population retains actual
programme and reader examples that correctly inherit EN, RU or zh-Hans.
Source: [HTML language attributes](https://html.spec.whatwg.org/multipage/dom.html#the-lang-and-xml:lang-attributes).

`aria-hidden` describes exclusion from accessibility APIs, not visual hiding.
The [published WAI-ARIA 1.3 working draft](https://www.w3.org/TR/wai-aria-1.3/#aria-hidden)
permits redundant content to be excluded when equivalent meaning and
functionality remain exposed. The proposal therefore does not declare every
hidden duplicate an error. A suppressed badge cannot serve as the required
witness, but another correctly bound, exposed witness in the same supported
component can satisfy that obligation.

The checker is restricted to the site's generated static HTML and explicit
suppression attributes or supported inline declarations. It does not compute
stylesheets, geometry, clipping, script state, browser accessibility trees or
general natural-language equivalence. Other prose may repeat a status; that
is not automatically a machine-verified substitute for a required component.
No universal HTML, CSS or assistive-technology compliance claim follows.

The first scoped-checker run rejected 21 otherwise valid reader pages because
the current-language button repeats the current reader route without adding
a second status badge. The retained refusal led to the narrowly qualified
locale-navigation case above. The own heading remains mandatory; an arbitrary
self-link or a sibling link does not receive that exception.

Final producer review also found three invalid-literal counterexamples: a later
unknown value for `display`, `visibility` or `content-visibility` replaced an
earlier hiding value in the draft parser. CSS declaration processing ignores
an invalid declaration. The successor retains these failures and adds a
bounded literal-value repair with both rejection and legitimate later-value
controls. The supported grammar is the explicit `STATUS_INLINE_VALUES` map.
Unknown values cannot cancel a previously recognized exclusion; this is
conservative for valid CSS outside that map. CSS-wide keywords, escaped tokens,
variables and general tokenization/cascade remain outside the claim.
Source: [CSS Syntax Level 3, declaration processing, 1 October 2026 Candidate Recommendation Draft](https://www.w3.org/TR/2026/CRD-css-syntax-3-20261001/#consume-declaration).

## Actual controls and unavailable cases

The pre-repair input is site base
`4475115ae03fc904aff3c7010ff298865bcbed44` plus the retained successor patch
SHA-256 `8f07e0919ab142d1bda27e230a2bea48a4d7e46829ac3de0b65bffe0c891de8d`.
Its actual `publication_checks.py` SHA-256 is
`2286fc07f01c2e89d274c10df977a7e00e1959f4d9a02807146c44187ce1e30b`.
The complete generated baseline passed with 123 labelled pages.

The frozen actual-page population contains 54 cases with stable locale/case
identifiers: 15 intended positives and 39 adverse cases. It covers nine
unchanged programme/roadmap/reader pages, six legitimate inheritance variants,
wrong or explicitly unknown language, suppressed required witnesses, a missing
badge at one of several programme occurrences and relocation to an unrelated
footer. All 54 were accepted by the old checker. The initial 42-case statement
was an intermediate report, not a separately retained original receipt.

The three actual roadmap pages contain zero work-status components at these
inputs. There is therefore no actual two-field roadmap badge mutation in this
population. Grouped-field behavior requires a separately identified renderer
fixture. A zero observation must not be relabelled as a successful real-page
test of that property.

## Successor integration and preservation

The successor site base is `5ff661bb6c894a44b3b6b1591d543c4830bc9180`, which
already includes CPU-ARC r4 through site PR61. Reconcile the proposed overlay
with that base while preserving all accepted r4 article bodies, the Journal
manifest, ten daily issues and thirty localized articles. The older overlay,
local failures and hosted receipt remain unchanged.

| Surface | Disposition |
| --- | --- |
| Scientific manuscript bodies, translation registry and review states | Unchanged |
| Site component validation and relevant renderer/test code | Scoped successor, reviewed against the actual emitted layouts |
| Earlier generated-page and source checks | Retained and executed against the successor where applicable |
| New actual-page control | Same declared case identities on the old and successor checker; different build inputs remain named |
| Historical roadmap/source bindings | Preserved; no redirection to a changed current document |
| Accepted CPU-ARC correction | Preserved exactly in the successor base |
| Hosted execution | Separate exact-head log, checkout and source-tree comparison required |
| Site adoption, non-author review and deployment | Existing owner lane; not established by this producer record |

Final artifact identities, actual runs and any initial failures are recorded
alongside this note and in the existing PR. The existence of a script or
workflow is not evidence of its execution. Helpers share the author controller;
their checks are producer assistance, not independent semantic review.

## Frozen artifacts and observed execution

The final [17-input patch](site-consumer/site-36x72-component-status.patch) is
106,723 bytes, SHA-256
`b140bb2ce697b95c5f7e693086bb04216613e58043ec35284e85590afb226db1`.
It applies cleanly to the exact new site base. The resulting checker has
SHA-256 `72e1ceb100b7482c6655d5bde13d335601022f4aadf9d4c992654bf6b7369e97`
and Git blob `f05452c909a1ddc6482f03dd81488059ccf8b021`.

| Retained observation | Result and boundary |
| --- | --- |
| Final portable harness against the old checker | All54 accepted, so39 adverse cases escaped; ordinary probe exited0 and the separate `--expect-fixed` run correctly exited1 |
| Final portable harness against the successor | 54/54 expected decisions:15 accepted positives and39 rejected adverse cases |
| Last validation-only repair | 32 build-test methods and all five direct publication/localization/link/paper/roadmap gates passed |
| Complete generation before that last checker-only repair | 36 works,72 target-language bodies,108 readers,354 HTML files,123 labelled pages and22,206 internal links |
| Other suites on that generated input before the last repair | 20 localization,37 roadmap,11 programme,8 Journal methods;752 UI controls |
| Output preservation after the last repair | All403 generated files byte-identical, including the accepted CPU-ARC inputs and Journal manifest |
| Feed inventory | Six RSS/Atom feeds,10 daily entries each;10 daily issues and30 localized pages |

The [final execution receipt](site-consumer/site-component-status-receipt.json)
keeps the complete generation and the seven post-repair commands separate.
The earlier successful component patch and its receipts remain in
[pre-inline-repair](site-consumer/pre-inline-repair/manifest.json), including
the subsequently found defect. The [actual-page result](site-consumer/actual54-result.json)
binds the checker, source page bytes and54 case identities. The [harness provenance](actual-pages/PRE_PORTABILITY_PROVENANCE.md)
identifies the original-script retention gap and the fresh same-script replay;
no reconstructed original script is claimed.

The workflow now replays the final patch on the accepted r4 site base, runs the
same54 controls with `--expect-fixed`, retains the previous three real-page
missing-binding controls, and runs the complete five Python suites (108 methods)
and752 UI cases. This paragraph describes workflow wiring; only a subsequent
exact-head hosted log can establish that it executed. The earlier c135 and
68-body historical checks and the current72-body rendition checks remain.
See [ARTIFACTS.json](ARTIFACTS.json) for content hashes of this retained package.

## Published CPU-ARC follow-up

The separate [F1/F2 disposition on site PR61](https://github.com/Arcanada-one/contract-place-site/pull/61#issuecomment-6946098799) confirms the two earlier wording findings are resolved in r4. The exact EN, RU and zh-Hans Git blobs, primary-source boundary, 15 source/rendering checks and deployment readback are retained in [cpu-arc-r4-followup.json](cpu-arc-r4-followup.json). The published correction distinguishes small-target-model perturbation outcomes from a broader model-size claim and identifies the dated retail API-price basis and applicable cache-entry invocations. It is a findings-owner follow-up after publication, not an independent whole-article review, fresh experiment replication or pre-merge acceptance.

## Reuse and rollback

For a later presentation change, enumerate the new renderer's component
obligations before reusing this guard. Retain a legitimate grouped or inherited
case as well as an error; a stricter predicate is not necessarily a more
correct one. Bind any result to exact generated bytes and actual checker code.

Rollback is a normal reviewed revert of the proposed consumer overlay to the
named site base. Do not change source review states, rewrite prior receipts or
treat delivery of this proposal as acceptance. Native admission and measured
reader benefit remain NOT_VERIFIED; execution cost is NOT_MEASURED.
