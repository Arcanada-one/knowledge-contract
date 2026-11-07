---
title: Bibliography restoration from Knowledge Contract v2 — provenance baseline
sources: none
status: research review in progress; no citation admission
---

# Recovering and checking the bibliography of Knowledge Contract v2

## Verified source locations and scope

The earlier **Knowledge Contract v2** publication is real and its bibliography is preserved at the pinned Arcanada site source [`pages/blog/posts/meaning-management-knowledge-contract-v2.en.php`](https://github.com/Arcanada-one/arcanada-landing/blob/742bb69b487677d371985a84fb5f70b3520aaff6/pages/blog/posts/meaning-management-knowledge-contract-v2.en.php), Git blob `04e846b22cec8b74566c24435571d77a1266a990`. Its public [References section](https://arcanada.ai/en/blog/meaning-management-knowledge-contract-v2#references) names **74 bibliographic paragraphs**, plus one introductory convention paragraph. This is a count of entries extracted from the pinned HTML; it is not a count of current independent primary-source verifications and need not equal the approximate historical "about 100."

The convention distinguishes (a) classical items marked **⟂**, which were **not re-fetched** in the historical verification pass, (b) other records described as resolvable on 2026-08-29, and (c) different methodological, comparison and bibliography additions assigned 2026-09-03, 09-04, 09-12 and 10-07 verification scopes. These are **source-authored historical assertions**, not new verification by KC-Brain in this pass. Each row's preserved bibliographic wording and classification is in [V2_REFERENCES.tsv](V2_REFERENCES.tsv), deliberately marked `NOT_RECHECKED` and `PENDING_SOURCE_AND_CLAIM_REVIEW`. The original HTML remains the canonical byte source; TSV is a normalized **reading inventory**, not a replacement for the source or source evidence.

A relative link `bibliography-verification-20261007.json` appears in v2's reference convention. At this audit, it was **not located** at the anticipated source-page sibling path in the pinned GitHub tree; the public `/en/blog/bibliography-verification-20261007.json` request returned HTTP 404. Do not invent, relabel or reconstruct its purported historical checks as a verified record. Its actual location/source identity is a documentary blocker for full historical verification recovery.

## Edition 1.1 citation baseline at exact revisions

The edition-1.1 split exists in `Arcanada-one/knowledge-contract`. There are eight accepted manuscript paths in source main `fb410a8460677b229d2240ba0fb27d184f48aa61` and a distinct ninth **F01 research-draft** proposal in PR48. The actual `## References` sections were read from these specific source revisions:

| Item | Current manuscript path | Reference entries | Inspected commit | Status |
| --- | --- | ---: | --- | --- |
| C01 | `controlled-knowledge-reuse` | 3 | `fb410a846067` | accepted source main |
| C02 | `semantic-objects-and-context` | 3 | `fb410a846067` | accepted source main |
| C03 | `constrained-transformations` | 3 | `fb410a846067` | accepted source main |
| C04 | `retrieval-and-context-composition` | 3 | `fb410a846067` | accepted source main |
| C05 | `interaction-and-memory` | 1 | `fb410a846067` | accepted source main |
| C06 | `evidence-and-falsification` | 2 | `fb410a846067` | accepted source main |
| C07 | `revision-and-governance` | 3 | `fb410a846067` | accepted source main |
| C08 | `knowledge-utility` | 1 | `fb410a846067` | accepted source main |
| F01 | `human-meaning-and-computable-knowledge` | 8 | `ce79e6b0ce12` | F01 research-draft PR48; not in accepted 8-paper baseline |

The eight accepted papers currently contain **19 bibliography entries counted per paper** (duplicates across papers are counted again); the proposed F01 contributes **8** further entries. These counts do not prove that missing work is cited in the appropriate discussion sentences.

## What the baseline establishes and does not establish

The earlier references were not entirely destroyed: they remain in the pinned v2 Arcanada blog. The nine split-paper reference sections **do not reproduce** that monolithic bibliography. They were selected and narrowed on individual paper paths; the evidence paper currently has only Hoare (1969) and PROV-DM (2013). This pass does not establish the editorial reason for every omission or claim that each omitted item belongs in one of the nine papers.

A reference can be restored in a particular paper only when a surviving sentence actually requires it and the **primary source or verified official text** was read for that *precise* support. For each admitted citation, the following fields are required: source pin/primary URL; author/year/title; historical v2 verification status; newly checked section/page or explicitly unverified status; target paper and sentence/heading; supported scope; non-support and source limitations; decision `restore`/`retain`/`drop-with-reason`; and independent-review outcome. Do not treat bibliography metadata, a historical ⟂ entry or the original v2's research claim as a present full-text source review.

For *Evidence, Reasoning, and Falsification*, possible **research themes to audit** are mutation testing, vacuity checks, argumentation, dependency/provenance and assertion evidence. These are literature-search topics, **not approved additional References**. The paper's proof of conditional soundness is its own mathematical statement; a citation cannot prove its premises or turn finite model checks into an empirical validation. Popper/Lakatos/Mayo would require actual primary-text reading and an exact matching claim before inclusion.

## Completion checklist and release boundary

1. Reconcile every `V2-###` record with a surviving exact heading/claim in one or more nine-paper paths. If none exists, mark `drop-with-reason`, preserving the original source record.
2. Recover the *actual* historical verification manifest if present, without guessing from the HTML link. If unavailable, preserve `NOT_RECHECKED` and perform new source-limited verification where justified.
3. Attach source-limited citations to the relevant sentences in **reviewed manuscript revisions**. Provide per-paper restored/retained/dropped tables and avoid reference padding.
4. Run full publication and source checks and independent Agent-Brain review on changed exact bytes before merge. Site re-pin/build/deployment/live readback and any index admission remain separate facts.

This preliminary baseline is original KC-Brain **source/inventory analysis**, not completion of the reference restoration or a new scientific manuscript. It changes no released paper, no licence, no task state, no publication list or index.
