# Four complete semantic specification renditions

17 November 2026. KC-Brain author candidate in the existing PR124. This
record documents source preparation and producer checks; it is not a task
status authority, independent review, publication decision or native admission.

## Previous state and intended change

At `18684f073285a4fa20f299518bd8a3d75b0c76d6`, the candidate had 36 English
works, 72 localized title/summary cards and 68 registered bodies. Semantic
Bridge and Semantic Verification each lacked a Russian and Simplified Chinese
body. The source-bound fidelity preflight identified important distinctions
but was not a substitute for complete texts.

This increment authors and registers those four bodies. The previous 68
rendition objects and target files, all eight historical review objects, the
72 metadata cards, formula descriptors and earlier producer evidence remain
unchanged. The resulting candidate has 72 registered bodies for exactly the
36 works crossed with the two target languages. New entries remain unreviewed.

## Source and content identities

English source revision: `8c7cd3bc1247998cb9554c568da26949da31b749`.

| Work | English Git blob | English SHA-256 |
| --- | --- | --- |
| Semantic Bridge | `d2ce70c2c8722e73473bfdd9b14043e459cc8b85` | `14806b95faf96be7e737b3e35f546ecc6da84fceb0e651966a786deba0b03078` |
| Semantic Verification | `54832c601597779ea6cef0dd99aa188f27645e9f` | `8e80af19426b676f45bdc4efd0fcd6e8d1073cf963246c40c431aaf296c97db4` |

Initial complete bodies: `ecb30ee75e3d3517f1009c0bd143c26de28c0711`.
Corrected content, used by all four registry pins:
`2627326cd0ac05f843bcc654dc550298bfec6b78`.
Registry revision: `8dae5ed3c9283de07102dac95c79037abb4642da`.
The review-presentation sidecar is rebound to that actual registry commit and
digest; its eight localized historical explanations are unchanged.

| Work / language | Target Git blob | Target SHA-256 |
| --- | --- | --- |
| Semantic Bridge / ru | `1e2a5ab4bb64df6d99941f2724e42ae0d7bfc333` | `2c89b7fb8bc9268f2a9b8e8320683c226e89c8a9d14af211cdbb3d0e1b0fdb9a` |
| Semantic Bridge / zh-Hans | `df503348ab5cf89fa4b8a3dd3ff78f8c428ea598` | `427a0151bcdd05cae3ae8992e97055565936af3009e1545c5c90ceb756cf95ef` |
| Semantic Verification / ru | `6ce643a62b3949f7a1c3a0e1f0a2bd1aa597b2f9` | `5bc9f168f509561f2ac419c5200178aab4366d9845c4c800a75a6cc81119c3b4` |
| Semantic Verification / zh-Hans | `069780613c057f973e35866cc6e39a426c85f56e` | `313ba227379be707db14ae231967f8b9d797c1193c7e90e52270facc4f4c59f6` |

## Producer reading and corrections

The two author-assistance contexts each read their entire English specification
and authored both target languages. They then read the other work's complete
English, Russian and Chinese texts. These contexts share this controller and
the task history; they are producer assistance, not independent semantic
reviewers. Native-language editorial qualification is not established.

The Bridge reading checked the eleven SBR obligations and preflight B1–B6:
complete rule units and exceptions, supplied facts versus validated structure,
`known` / `unknown` / `withheld`, shared observation identity, alternatives and
same-world disagreement, and `NOT_ASSESSED` / `TRUE` versus assessment or
authority. Three multilingual quoted examples retain their source bytes.

The Verification reading checked 27 SVR obligations and V1–V6: observation
identity, separate property assessments, oracle independence, applicable
positive controls, calculated versus executed populations, partial versus
global recovery, effective consumer input and the separate authority boundary.
It found three Russian precision issues before registration:

1. `comparator ties` had acquired an unwarranted baseline-only qualification;
   the correction retains general comparator outcomes.
2. `relevant observation equality` was rendered as a qualification of equality;
   the correction makes relevance qualify the observations being compared.
3. An undefined value of a partial function could be read as uncertainty;
   the correction explicitly says the function is undefined at that point,
   preserving the distinct model value `unknown`.

No formula, code identifier, normative ID, source claim, status or reference
identity was changed by these three prose corrections. The first content
commit remains available, so the producer's errors and the successor are
inspectable instead of being erased.

## Reproduction and evidence

Use the actual site consumer at
`d3d17929f209612669f38db6a735d46bc9ec309c` and Pandoc **3.1.3**:

```sh
python3 -I -B reviews/renditions/semantic-specifications-20261117/check_complete_renditions.py \
  --repository . --site-repository /absolute/path/to/pinned-site-checker \
  --pandoc /absolute/path/to/pandoc
```

The committed [producer result](producer-result.json) identifies the exact
publication tree, content commit, checker digest and every imported site
Python file digest. Use `--check-retained-result` to compare a later
receipt-only successor with its protected observations. A new invocation
prints a new result rather than overwriting the retained receipt.

The checker compiles all 72 real rendition records, including localized
presentation, and checks exact work/language identity, current English source
bytes, source/target commits and ancestry, metadata language, source IDs,
section mapping, paragraph/list/table-cell boundaries, ordered math/code and
canonical references. The observed result at `356779208ce7669234e494cf67a15aa08ae33aa6` is eight
historically reviewed and 64 unreviewed nonempty bodies, with zero missing or
stale pairs; all 30 adverse controls were detected. No new review
is manufactured. The new works have no visible formula prose requiring a new
formula-localization descriptor.

Adverse controls execute the same guards on a missing pair, a same-count
replacement by another pair, corrupted source and target pins, changed source
identity, an omitted source heading, changed math, changed code and a dropped
reference. They check refusal reasons, not merely nonzero exits. Optimized
Python is refused with exit 2 because the pinned external consumer uses
assertions. Structural checks cannot determine natural-language equivalence.

The first complete-consumer invocation at `a26edba7395faf7d0041307094b8fc473151eabd`
failed with `COMPILED_BODY_EMPTY` after its exact pair/state checks had passed.
The new checker had inspected the provenance inventory, whose entries omit
rendered HTML, instead of the consumer's separate `for_work()` reader surface.
The [original refusal](initial-checker-refusal.json) is retained. The repair
checks every actual reader body through `for_work(work)[language]`; no source,
translation, registry or historical review was altered to satisfy the checker.

The workflow replays the earlier 68-body source-currency and roadmap checks
at their immutable input `18684f073285a4fa20f299518bd8a3d75b0c76d6`. The
c135 metadata/pin replay stays at its original `b00b42fb5ca4f32ca443812c980c13d4d5d53d81`.
Those test populations and historical receipts are not rewritten to 72.
The new complete-body consumer is a separately named workflow step. Hosted
execution is only established by its actual new-head job log and checkout,
reported separately in PR124; a workflow declaration alone is not execution.

The local existing publication, source-declaration and 387-identity requirement
checks passed, as did 93 existing publication/source/separation/DCO/workflow
unit tests. The earlier 68-body consumer and its 45 adverse-control groups
passed at the immutable baseline, alongside that baseline's ten roadmap
adverse controls. Its first invocation encountered a Git object-fetch HTTP 503;
one retry of the same exact input succeeded. The first general publication
invocation selected system Pandoc 3.1.11.1 and correctly refused it; the explicit
3.1.3 invocation passed. Neither invocation failure is counted as a successful
test or evidence about translation meaning.

## Separately observed public site

The [bounded browser record](public-site-browser-audit.json) records the actual
64 linked page paths visited in English, Russian and Simplified Chinese:
192 distinct HTML URLs. Each had the expected HTML language, a nonempty main
body, title and first heading, with no unresolved literal in-page fragment
links found by the DOM check. All 31 currently published work readers were
included in all three languages, with matching heading and MathML counts.
This is a linked-page structural observation, not a review of every sentence,
every generated compatibility route, mobile layout or an atomic release.

On Semantic Objects and Context, switching EN to RU to zh-Hans preserved the
selected `#3-context-and-applicability` section and a real target. Titles,
descriptions and bodies changed language; the unreviewed RU/zh-Hans pages kept
`noindex,follow` and did not gain a false canonical translation claim.

The observation spanned the site's PR60 release. The Chinese Journal first
showed nine daily issues; an explicit reload then showed ten and the latest
article, matching the other languages. This is retained as a changing/cached
page observation, not reported as a persistent missing Chinese translation.
The new CPU-ARC article was observed in all three languages. Its scoped
scientific wording findings and the README's eight/24 versus ten/30 drift are
recorded in the existing [site PR60 discussion](https://github.com/Arcanada-one/contract-place-site/pull/60#issuecomment-6941483162).
That comment was posted after PR60 merged; it is a post-publication correction
request, not evidence that a pre-release gate blocked the published version.

The site's retained source has 31 works and 62 translated bodies. This new
36-work/72-body source candidate was not deployed by the browser observation.

## Impact, review and release boundary

| Affected surface | Verification and disposition |
| --- | --- |
| Four target manuscripts | Complete producer reading and structural comparison against exact English bytes; independent semantic review outstanding. |
| Rendition registry | Four source-bound additions; all 68 predecessor entries and bodies retained. |
| Review presentation | Outer registry pin/digest rebound; historical reviewer text and eight review objects unchanged. |
| Catalogue/cards/formula presentation | Bytes unchanged; actual metadata and reader consumers still execute. |
| Current translation roadmap | Updated exact work/language witness; dated older inventories remain history. |
| Checker and workflow | Successor validation plus historical replay at its own input; exact hosted execution separately recorded. |
| Full site compiler and release | Separately owned consumer operation; the site's retained 31-work release is not silently expanded by this candidate. |
| Public site and native runtime | No deployment or native admission follows from this source change. |

This is the provisional manually enumerated impact record for an explicitly
authorized source repair. It is not a formal graph admission receipt, Muneral
transition or runtime resolver decision. Role KC-Brain and the current
localized-release fidelity method fit the authoring, provenance and language
requirements. Missing independent review and native admission remain explicit
gaps; `runtime_authorized=false`.

Before release, the non-author reviewer must name exact source/target bytes
and language scope, then the site owner must rebuild the adopted catalogue,
check the remaining status/inventory consumers, run required CI on that head
and observe actual served bodies and locale metadata. The retained site-status
support patch is still a proposal until that consumer verifies and adopts it.

## Reuse lesson and rollback

The separately retained [complete-corpus site rehearsal](SITE-INTEGRATION.md)
now supplies a concrete downstream overlay and actual-page adverse controls.
It closes the producer integration gap without changing translation review
states or establishing deployment. The earlier seven-file proposal and its
receipts remain unchanged.

The checked change illustrates two obligations for a full translation: exact
structure must survive, and prose must preserve which object a qualifier
modifies. A count/anchor/formula check would not detect the three Russian
wording issues. Conversely, a fluent full-body reading does not establish
source pins, complete registration or actual execution of the reader. Keep
both observations and their limits in a later translation task.

A subsequent review can refute this candidate with a dropped or strengthened
claim, changed scope of negation or quantification, an inconsistent term, a
wrong citation target, a false completeness result under the adverse controls,
or a difference between the checked record and the delivered page.

Rollback the four bodies, four registry additions, review-presentation binding,
roadmap witness and successor workflow/check together to the named baseline;
preserve all historical receipts. Revert through the normal review path, not
by rewriting branch history. Cost and production benefit are **NOT_MEASURED**.
