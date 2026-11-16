---
title: "Ten Rendition Bodies Aligned with Their Current English Sources"
language: en
sources: none
status: author-prepared; independent language acceptance and site delivery not established
updated: 2026-11-16
---

# Ten Rendition Bodies Aligned with Their Current English Sources

## Conclusion

This increment updates the actual Russian and Simplified Chinese manuscripts
for five works whose English bodies had changed. It applies the source/body
currency distinction to the real rendition consumer. All ten remain author
drafts. The change supplies neither a new scientific result nor independent
translation acceptance, site deployment or runtime admission.

The existing candidate baseline is PR124 at
`b00b42fb5ca4f32ca443812c980c13d4d5d53d81`. The frozen parent PR104 remains at
`89382a5fa70d361ab906d44c7c4ea2b6ea28bc83`. The canonical English snapshot is
`8c7cd3bc1247998cb9554c568da26949da31b749`; the superseded English bindings
for these ten manuscripts were at
`161a01afb1b756adf059ea2e1cbdd0dca29d83a2`.

| Work, each in RU and zh-Hans | Actual content brought forward |
| --- | --- |
| [Knowledge Transformations](../../../papers/constrained-transformations/PAPER.md) | Abstract and quotient clarification, complete relation-coherence section and Proposition 4, proof, false-path example, conditional laws and references |
| [Meaning Geometry](../../../papers/geometry-of-semantic-representations/PAPER.md) | Abstract, finite nonempty outcome sets, Hausdorff metric and Proposition 7 with complete proof, domain and computability qualifications, examples and references |
| [Evidence and Falsification](../../../papers/evidence-and-falsification/PAPER.md) | Vacuity and specification-mutation comparisons, both new references, and their explicit limits |
| [Research Foundations](../../../reference/bibliography/BIBLIOGRAPHY.md) | Two methodological entries and all 21 Agent Situation use/limit records, including reading scope, dates, preprint and rights qualifications |
| [Source History](../../../appendices/source-map/APPENDIX.md) | Semantic Verification research-draft section, fixed source snapshot, elementary partial-recovery qualification and unchanged 29-claim index scope |

The new source/rendition entries bind to the existing content commit
`7020a5d9bd0cba850c1b3bbdcb1fad5ce4775524`, tree
`0e238e0ec16ddd3c4174c6d457c14c806643895f`. All ten uploaded Git blob identities
matched the local content tree. The body register was then committed as
`c862f829b388b39eaa9c78de8d7915b588d21fe7`, before the review presentation
descriptor was bound to it. No future commit identity is predicted.

## Improvement applied

### Source deltas and bounded author review

The authoring controller compared the precise English changes with both old
translations. Two analytical helpers prepared the mathematical deltas; a
third inspected actual consumer and presentation dependencies. The mathematical
drafts and six reference/evidence updates received additional reading within
the same controller. This is producer assistance and same-controller QA, not
an independent scientific or native-speaker review.

The new proofs retain successful-domain saturation, representative
independence, a common intermediate observation profile, and nonempty finite
outcome premises. Successful relational paths do not certify termination of
every runtime branch. Equality of outcome sets does not establish equality of
independently realized outcomes. The executable rational-distance qualification
is preserved; arbitrary real-valued distances are not declared computable merely
because a table is finite.

Bibliographic names, official titles, links and source identities are retained.
All added use/limit explanations and reading records are translated. The
recorded 7 November abstract inspections and 14 November selected readings are
historical source statements, not external literature checks newly performed
by this increment. Lin remains abstract-only. Preprints retain their status;
the Sheng record retains its CC-BY-NC-ND-4.0 restriction and no redistribution
claim. No production frequency, general reliability or transferred authority
is added by translation.

The obsolete `source_review_state: proposed-editorial-revision` field was
removed from the two transformation drafts because their current English
source is already in main. This does not change
`translation_status: author-draft` or add a review.

### Failures found through the actual consumer

An initial Chinese Geometry draft retained the full multiset of formulas but
reordered inline expressions in two otherwise equivalent sentences. The real
consumer requires exact mathematical order and rejected it with
`RENDITION_FORMULA_CHANGED`. The two sentences were reordered without changing
their conditions or expressions. All 140 mathematical objects now preserve
the English order, as do all 130 objects in each transformation draft.

Both Source History translations already contain a short disclosure after
the scientific-crosswalk heading that the table links lead to pinned English
originals. The extra block-shape check initially treated this retained
paragraph as a mismatch. It now recognizes only these two exact historical
paragraphs, verifies their AST identity against b00, and records the exception.
The actual consumer still checks each complete, unmodified target AST.

The first full rendition compilation at
`5827cd29b7833b4b4e4a1d1736effb81c76f36fa` then exposed a separate real
presentation failure: `FORMULA_LOCALIZATION_COVERAGE` for Knowledge
Transformations. Its new displayed formula contains the nonempty MathML text
`"for all "` at math index 89, mtext index 1. A source-math inventory of all 36
English documents found this to be the only missing descriptor; the four
existing descriptors covered their eight other nonempty text annotations.

The repair adds one source-bound annotation with Russian `"для всех "` and
Simplified Chinese `"对于任意 "`, preserving the universal quantifier over
all pairs and the boundary spaces. Its TeX digest is
`88fee1d40bf85f7c9c453d05f191dd2d5cb869e05ecc5852ea7c244320b20b35`.
The formula descriptor source revision is updated to the current English
snapshot; Geometry's changed source digest is rebound while all its existing
annotations and translations remain unchanged. The corrected descriptor is
committed at `6391480d9229acd693271faa9f038b73ceca3bc8`.

The regression restores the exact earlier descriptor by substituting only
that file's byte read during the real historical constructor. Actual Git,
ancestry and source/target bytes remain in use. Both locales must succeed with
the current descriptor and fail with the exact historical coverage error.
A different exception is not accepted as a detected defect.

### Reproducible current and historical checks

The [current checker](check_source_currency.py) pins the actual site code at
`d3d17929f209612669f38db6a735d46bc9ec309c` and Pandoc 3.1.3. It verifies all
committed input bytes and revision ancestry, compiles the 72 current metadata
records, validates the ten manuscripts, and runs the actual full rendition
consumer with both formula and review presentation. It checks paragraph,
list and table-cell boundaries, exact formulas and code, source references,
section maps and the two declared historical locale notices. These structural
checks cannot establish the semantic equivalence of every prose clause.

The integrated local replay passed at input commit
`6391480d9229acd693271faa9f038b73ceca3bc8`: 45 adverse control groups
were detected, comprising 44 body/source controls and one exact historical
formula-descriptor replay covering both locales. The final source and hosted
results are recorded separately; this local receipt does not predict a CI result.

The [current result](producer-result.json) reports the executed code digest,
source and target blob identities, compiled presentation provenance and exact
adverse cases. The byte/ancestry and consumer populations are:

| Population | Before this increment | Current candidate |
| --- | ---: | ---: |
| Canonical English works | 36 | 36 |
| Localized title/summary records | 72 | 72 |
| Registered translated bodies | 68 | 68 |
| Body source digests matching current English | 58 | 68 |
| Older-source body bindings | 10 | 0 |
| Missing work/language bodies | 4 | 4 |
| Historical review objects | 8 | 8 |

All 58 other register entries and their target files are unchanged. The full
metadata sidecar and the eight review presentation entries remain unchanged;
only the review descriptor's register revision/digest are rebound. The eight
historical review objects preserve their identities and scope. Compiled states
remain eight reviewed and 60 unreviewed bodies, with four missing pairs. A
current digest is not new acceptance of an old review or an unreviewed body.

The older Context Controls, Source Rule Checks and Agent Situation producer
scripts and receipts remain byte-identical. The historical c135 catalogue
checker still expects 58 current and ten older bindings. It is replayed from
an isolated worktree at b00, rather than edited to report the new counts.
Its successful [separate replay](historical-c135-replay.json) remains historical
evidence. The workflow explicitly runs that replay and the new current
consumer check as distinct steps. Optimized Python is refused with code 2
and the specific explanatory diagnostic because the pinned external consumer
uses assertions.

A separate [historical wrong-pin-code replay](check_historical_pin_regression.py)
addresses the outstanding r3 review question. It executes the exact b00 checker
with only the target refusal-code string changed in memory to the earlier
incorrect `RENDITION_RENDITION_PIN`. It requires that precise AssertionError,
the adverse rendition-pin input and the actual consumer call chain. The
[local receipt](historical-pin-regression.json) records the original and mutant
digests. This is one separate regression, outside the 45 current control groups;
the workflow invokes it before removing the historical worktree. Neither the
historical script nor its result is rewritten. A local run alone is not
hosted-execution evidence; the corresponding job must be read separately.

Hosted run [43947421265, job 133580658772](https://github.com/Arcanada-one/knowledge-contract/actions/runs/43947421265/job/133580658772)
executed these commands successfully for head
`12e5ebbca2db4a607c00ac76cff992023639b905`. Its actual checkout was
`d185ec87f583c7d69fe2d13b61e281f471b6ba2b`; the job printed the 45-group
PASS, the exact historical wrong-code AssertionError and the optimized-mode
refusal. The first general CI failed only the Markdown rule for three code
spans depicting significant trailing spaces in this record. Those examples
are now quoted as strings without changing their values. Final-head checks
and tree correspondence are recorded in the PR conversation after execution.

Local publication metadata/navigation/evidence checks, document naming and the
387-identity requirement register passed. The three relevant existing unittest
modules for workflow wiring, Context Package pins and translation inventory
passed all 56 tests. These maintenance controls are separate from the 45 new
consumer groups and are not counted as new scientific experiments.

This record does not claim a full site build: the pinned site's full-input
status allowlist predates the current catalogue, and the separately prepared
status-support patch remains its own release input. No branch merge, site
release, deployed-page probe or corpus-admission decision is supplied here.

## Idea and next use

Source freshness is an input relationship, and the actual reader adds further
requirements. Updating real manuscripts exposed both formula-order and
visible-MathML dependencies that a digest inventory alone could not reveal.
The useful repeatable method is to translate the actual delta, bind the exact
bytes, execute the actual consumer and challenge it with the earlier failing
input. Passing a separate source-currency classification model would not have
completed those steps.

The next content increment is the four remaining Semantic Bridge and Semantic
Verification bodies. DEUS's separate language review remains necessary for
the current new drafts. KC-SWE's existing site integration should consume the
exact source candidate, preserve the 36-work/72-metadata inventory, exercise
the status-support change, and supply its own release and served-page evidence.
Agent-SWE's real-use work and F05 execution qualification remain separate from
this publication increment; no replacement executor or task is created.

For rollback, restore the ten body files, three presentation/register files
and workflow changes together to b00, or revert this increment in reverse
dependency order. Leave all historical source/review records intact. A
consumer must not retain new descriptors against old bodies or vice versa.

This is a scientific-source author record, not a migrated KC-Brain canon save.
The new collective mailbox rule requires its shared native `cmail` client for
mail and canon changes. That client is unavailable in this executor; the four incoming copies read at the start of this increment
remain unarchived. No direct GitHub mail mutation substitutes
for it. Role migration and native admission/loading are not established.
Resource cost and improvement in production outcomes are not measured.
