# Engineering cases

One case per engineering work of the Knowledge Contract project: what the goal was, how the work was set up, what was checked and how, which receipts exist, what came out, where it stops, and what failed on the way. English, CC BY 4.0.

## Rules

1. **Every number links to a receipt.** A number in the prose is followed by a tag such as `[R1]`. The case's own `Receipts` table maps the tag to a file in this repository and a locator (a JSON Pointer, a line count or a table row count) and states the expected value. `tools/check_cases.py` resolves every row and rejects a number with no tag, a tag with no row, and a value that differs from the file. Number words (one, two, twelve, ordinals, hyphenated forms) and Roman numerals are rejected in a written case so that a number cannot hide in a word; code spans, links, comments, tables outside Receipts and the title are scanned, and fenced code blocks are not allowed.
2. **A planned case has no numbers.** It names the receipts it awaits and keeps every section so that the gap is visible. A case becomes `written` only when its receipts are in the repository.
3. **Failures stay.** The section "What failed on the way" is required. A case with nothing to say there says why it believes so.
4. **No secret, personal identifier or private host detail.** The checker applies the same deny shapes as the corpus exporter, plus email, phone and handle shapes.
5. **A tag proves a match, and a noun check narrows the meaning.** The Near column of the Receipts table names the nouns that must follow the tagged number within a short distance, so a number cannot be tagged to a receipt about something else. This is a guard, not a proof: a reviewer still checks the pairing.
6. **A case reports what a receipt shows, not more.** A check that was not run is written as not measured.

Start from [`_TEMPLATE.md`](_TEMPLATE.md).

## Index

| Case | Work | Status |
| --- | --- | --- |
| `paper-publication-pipeline` | Publication of the papers and specifications (KCP-0040 to KCP-0042) | written |
| `candidate-export-gate` | The fail-closed candidate exporter (KCP-0018) | written |
| `ru10-stand-and-repin` | The RU10 stand and its re-pin (KCP-0039) | planned |
| `ocr-stand-doclab` | The OCR stand doclab | planned |
| `conversion-adapter-and-deploy` | The conversion adapter and its production deployment | planned |
| `book-to-knowledge-pipeline` | The book-to-knowledge pipeline (KC-2) | planned |
| `theory-checks` | Falsifiable checks of the papers (KC-3) | planned |
| `practical-closure` | The practical closure (KC-4) | planned |
| `public-read-api` | The public read API (KCP-0019) | planned |

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [ATTRIBUTION.md](../ATTRIBUTION.md).
