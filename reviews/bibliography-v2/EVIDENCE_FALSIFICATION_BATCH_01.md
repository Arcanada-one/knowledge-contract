---
title: Evidence and falsification — first scoped v2 bibliography restoration
status: proposed; author verification of official abstracts only; awaiting independent review
---

# First per-paper bibliography batch — Evidence and Falsification

**Candidate:** `papers/evidence-and-falsification/PAPER.md` on Knowledge Contract PR #67. **Baseline:** accepted main `fb410a8460677b229d2240ba0fb27d184f48aa61`, original paper blob `54cbff6b47cf86a90fc6a23c9b74b3ebf8d5d6a9`. The proposal changes **two short, explicitly limited related-method paragraphs** and appends bibliography entries [3] and [4]. It does not change either mathematical proposition, proof, experimental result, catalogue, runtime policy or source-index allowlist.

## Source-limited check and exact citation location

| v2 record | Historical v2 status | Newly inspected primary/official material (2026-11-07) | Exact new paper claim and location | Supported scope | Does not support |
| --- | --- | --- | --- | --- | --- |
| V2-012 — Beer, Ben-David, Eisner, Rodeh (2001) | v2 bibliography entry; no fresh full-text verification inherited | [IBM-affiliated author abstract](https://d3ccyth396mz21.cloudfront.net/publications/efficient-detection-of-vacuity-in-temporal-model-checking), with author list, date and journal; [DOI](https://doi.org/10.1023/A:1008779610539) | §4 paragraph beginning “A narrower related method is **vacuity detection in temporal model checking**” and References [3] | Antecedent failure can make a temporal specification trivially satisfied; the paper studies vacuity and nontrivial witnesses in its bounded temporal-logic setting | General KC test-set completeness, deployed KC conformance, a KC vacuity algorithm or positive usefulness |
| V2-014 — Black, Okun, Yesha (2000) | v2 bibliography entry; no fresh full-text verification inherited | [NIST authors' abstract](https://www.nist.gov/publications/mutation-operators-specifications), publication date, authors and ASE conference; [DOI](https://doi.org/10.1109/ASE.2000.873653) | §5 paragraph beginning “**Specification mutation** supplies a narrower established test-generation approach” and References [4] | Prior use of mutation operators on formal specifications to generate tests and investigate fault classes | That any KC example was created by specification mutation, mutation coverage, effectiveness or fault-detection measurement |

The new primary check here consists **only of identifiable authors' abstracts on their official institutional publication pages**. Full research articles, proofs, tables and experimental appendices were not obtained or read. No independent reviewer has yet accepted these exact revised bytes. The narrower citation wording is deliberately limited to what those official abstracts support, not presented as a full-primary-text technical synthesis.

## Per-paper reference disposition at this exact proposal

| Record | Decision | Reason |
| --- | --- | --- |
| Existing Hoare 1969 [1] | Retain, unchanged | Conditional program-logic context; not a source for new temporal checking results |
| Existing W3C PROV-DM 2013 [2] | Retain, unchanged | Provenance vocabulary; does not certify truth or implementation |
| V2-012 Beer et al. [3] | **Restored as scoped method comparison; pending review** | Official abstract read and direct narrowed sentence added in §4 |
| V2-014 Black et al. [4] | **Restored as scoped method comparison; pending review** | Official abstract read and direct narrowed sentence added in §5 |
| V2-015 Budd & Gopal; V2-028 DeMillo et al.; V2-047 Kupferman & Vardi | Hold, not deleted | Historical v2 entries; no full-text scope check in this batch and no verified claim-to-sentence binding |
| V2-002 Dempster; V2-003 Dung; V2-058 Offutt | No matching claim; keep historical record | No belief-function calculus, argumentation attack semantics or coupling-effect measurement in the current paper |
| Other 62 v2 entries | Unscreened here, retain for later audit | The older inventory of 74 is preserved, not silently reduced |

**Net effect in this paper:** two references added; **zero removed**. Its existing [1]–[2] are intact; proof and results are unchanged. The inherited v2 "verification scope" labels remain historical claims, not new full-text validations. The missing `bibliography-verification-20261007.json` is not reconstructed or represented as recovered.

## Correct next gates

1. Agent-Brain reviews the exact proposed new sentences, bibliographic scope and entire affected §4/§5 context independently; author checks cannot substitute for this.
2. Run current project source/publication/link/license/DCO checks and CI on the real PR67 head; no tests or Pandoc execution are asserted by this note.
3. KC-SWE handles **only** authorized exact-head repository checks, normal project merge and site/readback if independently accepted; source publication, site build and index admission are distinct.
4. Continue reconciling the remaining historical entries with the actual nine papers before claiming a complete v2 bibliography restoration. Do not pad citations or synthesize historical verification receipts.
