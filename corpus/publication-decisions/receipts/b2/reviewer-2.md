session_id: kcp-b2-blind-reviewer-2-20261103
model: claude-opus-5-5
input_digest: 75cb87d567483af5a62b1d9b047ab5d8a3618923c8dff914e3fd7de725b9803e

Blind review 2 of 2: publication decision batch b2 (14 English entry pages, P00 to P13)

**Reading statement.** I read the whole input in sequential chunks through to the end: the diff with all 14 decision lines, all 14 page blobs line by line, the three declarations and the checklist. I mapped page line numbers from each page's first front-matter line. Every line number cited in the 14 decision rows, including the "own-package material as missing" line, points to the line that carries the quoted text. I ran no commands, so the byte hashes and lengths were not computed (see item 1).

**Mentions: reference or reproduction, judged by the page's own words**

All mentions are **references**. No page reproduces third-party text. The quoted phrases are the authors' own statements about unread, unverified or outside material.

- P00: L25 books, L33 pkg, L39 books, ext and nr are references. The page gives counts only ("917 derived descriptions"); no outside text appears.
- P01: L25, L34, L38, L40 (books and ext) and L47 are references. "OCR accuracy against the original PDF was not measured" contains no source text.
- P02: L25, L29, L30, L33 (books and nr), L35, L39, L47 and L49 are references. "two books copying one source" is the authors' illustration.
- P03: L32, L38, L39, L40 (books and ext), L46 and L48 are references. The logs are reported as counts.
- P04: L25, L30 (ext and pkg), L31, L32 (books and nr), L33, L38, L40 and L41 are references. BM25 and PNG are only named.
- P05: L31 ("SET COVER") and L33, L38, L40 and L49 are references. On L40 the page says the theorems "are quoted with premises". On this English page no theorem statement appears, so it is a reference here. The decision line already records the disagreement with the register.
- P06: L25, L31 (ext and nr), L32, L33 and L41 are references.
- P07: L25, L29 ("NIST, NOAA, and one recipe fragment of a USDA collection") and L39 are references. The page reports run counts only, with no excerpt.
- P08: L25, L32 (books and nr), L33 (books and both ext), L40, L41, L49 and L50 are references.
- P09: L25 (both ext), L29, L31, L32, L34 ("AKP forms"), L43 and L52 are references.
- P10: L25 (books and ext), L32 (nr and pkg), L34, L38 and L41 (nr and pkg) are references.
- P11: L33 (three mentions), L38, L39 ("the cited contamination work was not read"), L40, L44, L48 and L49 are references.
- P12: L25, L30, L31, L32 (nr and pkg), L39, L48 and L49 are references.
- P13: L29 ("the causal literature, not read"), L31, L39, L48, L49 and L50 are references.

**Omissions found (all NON-BLOCKING; none shows reproduction)**

1. P08 L38 (books): "Nothing is established about real books, reader comprehension, or a production permission mechanism"
2. P08 L25 (ext or nr): "It does not check whether a quotation matches its primary source or whether the markup is true"
3. P07 L25 (ext): "A check on real acquired sources has its own scope"
4. P09 L52 (nr, disputed): the row quotes only the first clause. Also missing: "the amendment speaks of seven profiles, the edition lists six"

**Checklist**

1. **Not measured (byte-level); textual agreement holds.** Each BLOB digest matches its line's `sha256` exactly, for example "33aed0c8…fdd2" for P00 and "e94b1062…b4d8" for P13; I checked all 14. I could not hash the bytes or confirm the lengths without commands. This is not read as a fail.
2. **Holds.** "UPSTREAM original" matches `"upstream":"original"` on all 14 lines. REUSE `path = "**"` declares "CC-BY-4.0". NOTICE says "Text and documentation are licensed under CC BY 4.0". LICENSE is "Attribution 4.0 International". Every page's front matter has "license: CC-BY-4.0".
3. **Holds.** "rights_holder":"Pavel Valentov" is a named person. The rights_basis quotes "'2026 Pavel Valentov and Knowledge Contract Arcana contributors'", which matches REUSE.toml exactly. It also says "DCO sign-offs that are declared and not verified".
4. **Holds for the lines and the pages.** I found no secrets, host names, host paths or addresses. Agency names (NIST, NOAA, USDA) appear only as references, not as marks used for branding. The LICENSE text is the official CC text, supplied as a declaration.
5. **Holds.** Each page ends with "Based on Knowledge Contract Arcana … (CC BY 4.0)", and each line carries "credit line of ATTRIBUTION.md applies".
6. **Holds.** The limits field states, among other things, "does not establish … absence of unrecognised third-party material, scientific validity … that a review took place".

**The 14 lines**

- **Schema and keys:** all 14 lines use the same 12 keys in sorted order, with "schema":"KnowledgeContractPublicationDecision/v2" and "status":"current". The JSON escaping is consistent, including the nested quote in the P05 row (`\"R01 exposes the whole core\"`).
- **Digests:** see checklist item 1.
- **Holder, license, upstream:** consistent on every line.
- **Item-2 sentence:** present word for word on every line: "as of this line no review of reproduced third-party text has been performed beyond the reading, by the b2 decision reviewers, of the page mentions listed in this line". The neutral sentence "this line claims neither that the page reproduces third-party text nor that it does not" is also present on all 14.
- **No reproduction claim either way:** no line asserts that a page reproduces third-party text, or that it does not. Holds.
- **Rules (a) to (c):** every page states it is a scientific draft ("Status | scientific draft (`concept_draft`)"). Every page says independent semantic review was not performed, and every page names what was unread or unverified. The pages bear out rule (a).

**Other observations (NON-BLOCKING)**

- The rights_basis cites "the source commit 817a8d8d42d452b9daeb68df55f9c9029366cc82" and "OPENNESS.md item 3". Neither is in the input, which contains the declarations read at the base. Whether the commit and the base agree is not measured. The REUSE string quoted in the lines does match the declaration bytes supplied.
- Each line names a receipt, "receipt":"corpus/publication-decisions/receipts/b2.json", but the diff adds only the jsonl file. Whether the receipt exists at the reviewed head is not measured.

**Finding: no BLOCKING finding.** No line text is contradicted by its page. Every row quote is verbatim at its stated line. No line contains a host path or a secret. No page reproduces third-party text.

VERDICT: APPROVE ae7ea884fa79b0cf510a6f4fc2b7d3d9d57c70ded2697fcdc63575bbcf1063d8
