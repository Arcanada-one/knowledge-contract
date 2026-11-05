session_id: kcp-b3r2-blind-reviewer-2-20261105
model: claude-sonnet-5-5
input_digest: a8ed5f63c40e88aa67e1a2212a415bfa2dcb814189f24b94fd2772bd800bb0b0

## Reading statement

- Read in full by eye: the 29 decision lines (as printed by program, shared fields once), the REUSE.toml and NOTICE declarations, the checklist, and the source-map appendix lines 66-68 and 91-95.
- Read only in part by eye: the 29 pages. I saw excerpts around lines flagged by program (lines matching quotation, licence, third-party, reproduction, book, corpus patterns), the front matter lines 1-14 grep results, the reference-list line ranges, and the three source-transcription study paragraphs (lines 18-28) and two executable-projections paragraphs (lines 30, 55). I did not read any page end to end.
- Checked only by program: JSON well-formedness and canonical form, uniqueness of paths, sha256 and byte lengths, front matter author/license presence, Author-line presence, scans for host paths, addresses, host names, key/secret/token patterns, trademark/copyright symbols in pages and decision lines. The scans are pattern based; a secret or path not matching the patterns would be missed.

## Digest of the reviewed diff

sha256 of the diff bytes (everything before the line --sources--) followed by "--files--\ncorpus/publication-decisions/b3.jsonl\n" computes to 6821db903970a9487278fdc9125ef259ba55caa7d7942194d934abe86ec6dfc3. It MATCHES the author's stated digest. The whole input also hashes to the stated input_digest.

## Per-item judgement

1. Hashes and lengths: PASS. 29 BLOB records, 29 decision lines, identical path sets. For every path sha256(bytes) equals both the BLOB digest and the decision-line sha256; the byte count equals the declared length; the BLOB upstream equals the line upstream. 0 mismatches.
2. Upstream and licences: PASS. upstream is original on all 29 lines and in the declarations. Every line says license CC-BY-4.0; the REUSE.toml default annotation (path **) gives CC-BY-4.0 with the holder string below; the Apache-2.0 override covers code/schema/tool paths only, none of the 29 pages are Markdown pages in that set. NOTICE says text and documentation are CC BY 4.0. Front matter of all 29 pages has license: "CC-BY-4.0".
3. Rights: PASS. rights_holder is Pavel Valentov (a named person). rights_basis quotes '2026 Pavel Valentov and Knowledge Contract Arcana contributors' exactly as in REUSE.toml, names CC-BY-4.0 for pattern '**', says it is a statement of the repository and not a verified fact, and says contributors' parts rest on DCO sign-offs that are declared and not verified. NOTICE line "Author: Pavel Valentov, Independent Researcher ..." names the person. I could not verify the source commit id cited in rights_basis (it is not in the input).
4. Third-party, marks, secrets, paths, hosts: PASS with notes. No long quotation, no reproduced table or figure from an outside work, no trademark or copyright symbols, no secrets, no host paths, private addresses or host names found by program or in the excerpts read. Matches were only the word "token" in its technical sense, public URLs (contract.place, api.contract.place, GitHub repository) and a commit hash. The decision lines contain none of these either. Page mentions of outside or unidentified material (all judged from the page's own words):
   - papers/constrained-transformations/PAPER.md lines 159-161: reference list (3 entries); reference, not reproduction.
   - papers/controlled-knowledge-reuse/PAPER.md lines 143-145: reference list (3); reference.
   - papers/evidence-and-falsification/PAPER.md lines 127-128: reference list (2); reference.
   - papers/interaction-and-memory/PAPER.md line 118: reference list (1); reference.
   - papers/knowledge-utility/PAPER.md line 145: reference list (1); reference.
   - papers/retrieval-and-context-composition/PAPER.md lines 125-127: reference list (3); reference.
   - papers/revision-and-governance/PAPER.md lines 128-130: reference list (3); reference.
   - papers/semantic-objects-and-context/PAPER.md lines 162-164 reference list (3); line 28 names W3C PROV-DM and SKOS by description with citation; reference.
   - reference/bibliography/BIBLIOGRAPHY.md lines 22-158 (entries from line 22 on; sections at 12, 142, 158): bibliographic entries with the page's own "used for" descriptions; reference.
   - engineering/studies/source-transcription-and-uncertainty/STUDY.md line 24: names three printed books (a 1952 cookbook edition, a 1977 navigation text, a 1964 automation problem book) as the audited corpus; lines 18, 26-28 give counts of fields and descriptions derived by the study; statement about outside works plus own measurements, no reproduced text seen.
   - engineering/studies/executable-projections-and-revision/STUDY.md line 55 ("three books"), line 30 (book-layer report with OCR reader), line 116 (Russian prose views of the study sources): statements of what was done; no reproduction seen.
   - appendices/source-map/APPENDIX.md line 68 (historical cooking, navigation and electrical examples, "unavailable third-party source corpora"), line 93 ("Third-party books, page images and OCR corpora are not redistributed here"), line 95 (source register replaces the earlier catch-all description): statements of limits.
   - engineering/specifications/book-package/SPECIFICATION.md lines 249-255 (rights classes; "no quotation budget or right to republish is inferred"): normative text about third-party material, not third-party text.
   - reference/glossary/GLOSSARY.md line 140: mentions quoted historical labels such as "independent review"; a short label, not a reproduction. The glossary has Russian equivalent terms in a column; these are the project's own translations of terms.
   Unidentified material: none found that a page presents as outside text. Because I read the pages only in part, I cannot exclude an unflagged quotation; see finding N3.
5. Credit line: PASS under the stated ruling. The attribution field says: for the project's own publication, item 5 is satisfied by front matter author and license on all 29 pages plus citation metadata; ATTRIBUTION.md lines are for reusers; 10 named pages have no visible Author line. Verified: author: "Pavel Valentov" and license: "CC-BY-4.0" are in the front matter of all 29 pages (line 6 and neighbouring line). A visible "**Author:** Pavel Valentov" line at body line 14 is present on exactly 19 pages (all 11 specifications and all 8 papers) and absent on exactly the 10 pages the field names (6 studies, glossary, bibliography, 2 appendices): the set difference is empty. Two precision points: the glossary has a visible "Maintainer: Pavel Valentov" line at line 14 though no Author line, and book-package carries a visible "Credit and licence: Knowledge Contract Arcana ... (CC BY 4.0)" line at 307. The statement is accurate as written and sufficient as a stated project ruling; it honestly records the gap and a follow-up. The claim about citation metadata returned by search and fetch is not verifiable from the input.
6. Limits: PASS. limits states it does not establish authorship identity, agent-text copyright, absence of unrecognised third-party material, scientific validity, closure of edition 1.0 findings, currency beyond the source commit, and that the record is written by the same account that reviewed. third_party is "not established" with reasons and does not claim absence.

Form checks: 29 lines, each parses as JSON and re-serialises identically with sorted keys and compact separators (no whitespace differences); 29 distinct paths; identical key set (12 keys) on every line; schema KnowledgeContractPublicationDecision/v2 and status current on all; receipt is corpus/publication-decisions/receipts/b3.json on all 29. All 29 lines carry byte-identical attribution, limits, rights_basis, third_party fields (only path and sha256 differ).

## Findings

- N1 NON-BLOCKING: 10 of 29 pages have no visible credit in the body; the ruling relies on front matter and metadata. Accepted by the ruling and a follow-up is recorded.
- N2 NON-BLOCKING: the attribution field says the glossary has no visible Author line; it does have a visible Maintainer line naming the same person. Harmless imprecision (the page is more credited than stated).
- N3 NON-BLOCKING: my page reading was partial and pattern-driven; absence of third-party reproduction is not established by this record, consistent with third_party and limits wording.
- N4 NON-BLOCKING: rights_basis cites a source commit and OPENNESS.md items that are not in the input and could not be checked by me.
- N5 NON-BLOCKING: the attribution, limits and third_party texts are identical on all 29 lines and long; no page-specific third-party judgement is recorded (consistent with "not established").

No BLOCKING finding.

VERDICT: APPROVE 6821db903970a9487278fdc9125ef259ba55caa7d7942194d934abe86ec6dfc3
