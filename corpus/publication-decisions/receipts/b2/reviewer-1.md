session_id: kcp-b2-blind-reviewer-1-20261103
model: claude-sonnet-5-5
input_digest: 75cb87d567483af5a62b1d9b047ab5d8a3618923c8dff914e3fd7de725b9803e

**Blind review b2, reviewer 1 of 2**

**Reading statement.** I read the whole input in order. That is the diff with all 14 JSON lines, the 14 blob records and page bytes (P00 to P13), the REUSE.toml, NOTICE and LICENSE declarations, and the fixed checklist. I read the 14 pages line by line, front matter to credit footer. I also read the LICENSE text, which is the unmodified CC BY 4.0 text. Line numbers below are page lines, counted from the opening front-matter marker as line 1. I checked the numbers for the mentions against the pages and they match.

**Mentions, judged from the pages' own words.** Every mention is a reference or a statement of limits. None is a reproduction. No page body contains quoted third-party prose, a formula, a table or a figure taken from an outside work.

| Page | Judgement |
| --- | --- |
| P00 (25, 33, 39 ×3) | The three-book observations, the unread source identifier and the "917 derived descriptions" are the authors' own derived counts and statements of limits. Reference. |
| P01 (25, 34, 38, 40 ×2, 47) | Statements that something was not run, not measured or not read. Reference. |
| P02 (25, 29, 30, 33 ×2, 35, 39, 47, 49) | Illustrative examples and unread own-package reports. Reference. |
| P03 (32, 38, 39, 40 ×2, 46, 48) | Own logs and counts; "fixed OCR/VLM versions" names tools only as a need. Reference. |
| P04 (25, 30 ×2, 31, 32 ×2, 33, 38, 40, 41) | A PNG signature, BM25, dense or hybrid retrieval, and SQL-like queries are named only as comparisons not made or as alternatives. Reference. |
| P05 (31, 33, 38, 40, 49) | SET COVER, NP-hard and UTF-8 are named only. Line 40 says "Cited external submodular-optimisation theorems are quoted with premises, not proved here and not verified by the writer". The English page body contains no theorem text, so on this page it is a reference. Whether the Russian full text quotes them is outside these bytes. The decision line discloses the mismatch with the register's "no excerpts intended" and does not correct the register. Not blocking. |
| P06 (25, 31 ×2, 32, 33, 41) | Outside registries and literature are named as unread or outside the model. Reference. |
| P07 (25, 29, 39) | Three public documents are named (NIST, NOAA, a USDA fragment) as test inputs. CER/WER are named as `null`. Reference, with no excerpt on the page. |
| P08 (25, 32 ×2, 33 ×3, 40, 41, 49, 50) | Named tools and facilities, own run counts, unread own reports. Reference. |
| P09 (25 ×2, 29, 31, 32, 34, 43, 52) | A JSON Schema and AKP forms are named as the authors' own work, plus unread reports. Reference. |
| P10 (25 ×2, 32 ×2, 34, 38, 41 ×2) | Own observations and assumptions. Reference. |
| P11 (33 ×3, 38, 39, 40, 44, 48, 49) | "The justification is not reproduced in this paper" says outright that it is not reproduced. The page cites "the cited contamination work was not read" and does not reproduce it. Reference. |
| P12 (25, 30, 31, 32 ×2, 39, 48, 49) | Own pilot figures, unread own sources. Reference. |
| P13 (29, 31, 39, 48, 49, 50) | "the causal literature, not read" is named only as unread. Reference. |

**Omissions from the table.** All are NON-BLOCKING, and none shows reproduction of third-party text.
- P03 line 38: "three captions fell into alt-text" (books).
- P08 line 33: "three alt-text copies also changed" (books).
- P10 line 32: "348 of 348 hashes" (own audit).
- P09 line 52: "the amendment speaks of seven profiles, the edition lists six" (an nr-type held inconsistency).

The mention list is an aid and incomplete by its own wording, so these do not weaken the decision.

**Checklist.**
1. I compared each decision line's `sha256` with the digest in its blob record by eye. All 14 pairs are textually identical (P00 33aed0c8… through P13 e94b1062…). Recomputing the digests from the page bytes, and the diff digest, was **not measured** by me. I ran no commands.
2. Pass. All 14 front matters say CC-BY-4.0. The REUSE default annotation, NOTICE (text under CC BY 4.0) and LICENSE (CC BY 4.0) agree. The declared upstream is `original` in all 14 lines.
3. Pass. The holder is Pavel Valentov. `rights_basis` quotes the REUSE.toml holder string "2026 Pavel Valentov and Knowledge Contract Arcana contributors" exactly, and says contributors' parts "rest on DCO sign-offs that are declared and not verified".
4. Pass on these bytes. I saw no secrets, host paths, host names or addresses in the pages or lines. The only URLs are the project's own public site and repository in the credit footer and NOTICE. Third-party text: none reproduced (see mentions).
5. Pass. All 14 pages end with the credit line "Based on Knowledge Contract Arcana … (CC BY 4.0)" and the licence and attribution links.
6. Pass. The `limits` field is identical in all 14 lines. It disclaims authorship identity, agent-text copyright, absence of unrecognised third-party material, scientific validity, that a review took place, and summary fidelity.

**The 14 lines.**
- All have `status` `current`, `rights_holder` Pavel Valentov, license CC-BY-4.0 and upstream `original`.
- The `third_party` field begins "not established".
- All 14 contain, verbatim, "as of this line no review of reproduced third-party text has been performed beyond the reading, by the b2 decision reviewers, of the page mentions listed in this line".
- All 14 say "this line claims neither that the page reproduces third-party text nor that it does not".
- All 14 state write-once and "a later finding is recorded as a new line in a new batch".
- None states whether a page reproduces third-party text.
- The pages say they are scientific drafts, that independent semantic review was not performed and that the synthesis gate is open. They name unread, unverified and missing material in their own words, as rule 3(a) requires.

No BLOCKING finding.

VERDICT: APPROVE ae7ea884fa79b0cf510a6f4fc2b7d3d9d57c70ded2697fcdc63575bbcf1063d8
