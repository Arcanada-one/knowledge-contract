---
sources: none
---

# Revision and governance: author review record

This record reports the producer's inspection and local checks of [the manuscript](../../papers/revision-and-governance/PAPER.md). It is not independent scientific acceptance, deployed conformance, or a release decision. Reference numbers below identify the manuscript's existing bibliography; no third-party text is reproduced here.

## Exact scope and identities

- Baseline commit: `e351df0c28f0b9965a580f45b48a297d1872c3ce`.
- Baseline manuscript blob: `8a9c232571d2961b831e447825a93b042bd3f04c`.
- Baseline SHA-256: `e221151a7c6778ef4c6843074a881efead94bad2f0b95e21c697f122c67f58dc`.
- Candidate SHA-256: `20079132357dc2e4e651cde78d528b37712ecdef030af3934ebd2e8048e3f78a`.
- Candidate blob: `c433591c6e87eb0791c4932c41c4f7538114e628`; 21,282 UTF-8 bytes.

The baseline was read in full. Its blob is unchanged from the earlier inspected main `ddfaecfcf3c1dafe339d6db9c5bc86b3399e5991`; the intervening release-catalogue change is not overwritten. This proposal changes one existing manuscript, not a new foundations paper or a batch of source books. Existing catalogue, requirements, evidence receipts, corpus decisions, allowlists and historical source inventory remain untouched.

## Changes and scientific review

The abstract now identifies the deductive method and the limited result of each proposition. Section 1.1 separates this account from PROV representation, truth maintenance and AGM theory revision. Section 3.1 distinguishes equality of a checker result from soundness and current authority. Section 6.1 traces five different revision events and the alternative-ground counterexample. Section 7.1 pairs intended behavior with weaker strategies and controls the independence premise of Proposition 4. Section 9 adds a bounded conclusion.

These are substantive scope clarifications, not merely typography. All of original Section 4, including four statements, proofs and limitations, remains byte-identical, as do Section 8, front matter and References. Original heading anchors, mathematical expressions and link targets are retained. A synthetic example is explicitly not a measured deployment event.

| Proposition | Producer assessment | Important remaining boundary |
| --- | --- | --- |
| 1: historical selection | The conditional argument is valid: an exact immutable reference does not depend on the current pointer. | No perpetual availability, integrity mechanism or present disclosure right follows. |
| 2: deterministic check transfer | Equal complete inputs to the same deterministic function give the same output. | Even an unsound checker can repeat success; function identity and hidden inputs require justification. |
| 3: reassessment candidates | Reverse reachability locates represented dependents. | Completeness of real dependencies is assumed, and alternative support can preserve an assessment. |
| 4: adoption and facts | A model of adoption with the contingent fact false defeats entailment of that fact. | The premise does not apply when the fact is already entailed by the adoption event; no rejection of institutional facts is implied. |

None is advertised as a new general theorem of belief revision. The contribution is their scoped use in an account that separates records, assessments and authority. An independent reviewer must assess whether that contribution and its presentation are sufficient; document identity cannot decide scientific merit.

## Source-fit recheck on 2026-11-07

| Existing reference | Material actually inspected | Exact manuscript use | Limits |
| --- | --- | --- | --- |
| [1] PROV-DM | Dated 30 April 2013 W3C primary specification: core structures and Section 5.2.2. | Section 1.1: revision is a specialized derivation relation. | Representation does not establish truth, authenticated authority or implementation. |
| [2] Doyle 1979 | Author bibliography and institutional/publisher abstract records; attempted full-text retrieval failed. | Existing Section 1 high-level account of recording reasons and revising assumptions, unchanged. | No new full-text reading, algorithm reproduction or source-proof verification claimed. |
| [3] AGM 1985 | Primary journal scan, Sections 1–2 through the basic postulates; first-page screenshot inspected. Further requested page renders failed, while the text was available. | Section 1.1: theories and consequence operations differ from merely versioned records. | Not a complete reread of all proofs, and no KC-to-AGM representation theorem or postulate-conformance result. |

All three references remain; none was silently removed. Relevant-section inspection is not whole-work verification. Geometry and semiring sources are not appended to this paper without a matching claim. The separate historical-v2 restoration remains open and is not completed by this manuscript.

## Local evidence and reproduction

Run `python3 -B tools/verify_revision_governance.py --paper papers/revision-and-governance/PAPER.md`.

[RESULTS.md](RESULTS.md) retains the actual JSON from Python 3.13.5 and the checker-sensitivity results. There are 16 document-preservation checks and 18 authored boundary illustrations. The finite graph comparison covers all 512 directed graphs on three vertices including loops, with 4,608 membership comparisons. Separate domains contain 256 equal-input/function-table label pairs and four adoption-model sets satisfying both satisfiability premises. Those counts have different units; the equality illustrations add no empirical evidence for checker soundness.

A second run reproduced the JSON exactly. Appending text to the candidate made its content-lock check fail with exit 1. A deliberately weakened direct-dependency-only traversal returned exit 1 and disagreed with transitive closure in 384 membership comparisons. Both temporary mutants were removed. The comparison implementation and tests were written by the same producer, not an independent reviewer.

## Required next review

Read the entire exact candidate against the baseline. Check the source comparisons and the distinction among repeated outputs, justified evidence and current authority; assess the constructed example and every retained proposition. Return findings against the candidate hash. Changed bytes require renewed delta review, not a silent update of the lock.

Current required repository checks, their prescribed environment, DCO/source/link/license checks, full CI, independent semantic review, site rendering and live source readback have not been established by this local run. No author merge, site deployment, index admission or runtime authorization is granted by this proposal. Operational tasks and private correspondence are not part of this public record.
