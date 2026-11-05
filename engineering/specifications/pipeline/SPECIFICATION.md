---
sources: none
name: "pipeline"
title: "Knowledge-Supply Pipeline: Stages, Document Identity and Receipt Chain"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Repository-only engineering contract for the nine stages that carry one document from intake to the search index, its content-addressed identity and its chain of stage receipts."
---

# Knowledge-Supply Pipeline: Stages, Document Identity and Receipt Chain

**Author:** Pavel Valentov · **Status:** repository-only engineering document, not part of publication edition 1.1

| Implementation component | Scope |
| --- | --- |
| [Receipt schema](../../../schemas/pipeline-receipt.schema.json) | `PipelineStageReceipt/v1`, one record per stage |
| [Chain validator](../../../tools/check_pipeline_receipts.py) | Order, links, identity, rights, consumption and honesty of one chain |
| [Fixtures](../../../schemas/fixtures/pipeline/) · [generator](../../../tools/pipeline_fixture.py) | Twelve valid chains and twenty-seven one-defect mutants |
| [Tests](../../../tools/test_pipeline_receipts.py) | The validator against every fixture, drift of the committed files, mutants of the validator |

## 1. Purpose, boundary and status

One production path carries a document from the moment it arrives to the moment it can be found: Doclab Arcana recognises and bundles it, Conversion Arcana converts the formats Doclab does not read, Knowledge Contract holds it as a book package in a library and serves it, and the Arcanada knowledge base indexes it. This specification fixes what the stages are, how one document is named across them, what each stage leaves behind, and how the whole record is checked.

It reuses and does not replace the [book package](../book-package/SPECIFICATION.md) (`book-package/2`), the producer export manifest, the project-index run receipt and the change-admission receipts. It adds no central ledger.

This document is a repository-only engineering contract. It is not in the publication catalogue, it has no corpus allowlist row, and no export or index run reads it. It can enter the published corpus only through a later edition decision batch (edition 1.2 at the earliest); until then its edition label records the edition it was written against and promises nothing.

It does not claim runtime admission (`kc2_admission` is `not_measured` in every receipt), the quality of any recognition or conversion, or that any stage other than the ones listed as built in §2 exists.

## 2. The nine stages

Every document passes the stages in this order, each exactly once and each leaving a receipt. A stage that cannot finish leaves a receipt that says so and the chain ends there. Two stages may also end `skipped`, with a reason: `convert` for a format Doclab reads as it is (PDF and images), and `classify` when no classification is wanted; a skipped stage produces nothing, and the next stage that finishes reads the output of the nearest earlier stage that finished, or the original source.

| Stage | Owner | Consumes | Produces | Muneral | Built today |
| --- | --- | --- | --- | --- | --- |
| `intake` | Doclab Arcana | the original file | a source record | X2 (ee333ee6) | partly: Doclab intake records the source digest and size |
| `classify` | Doclab Arcana | the source record | a classification with evidence and confidence | X2 (ee333ee6) | not built |
| `convert` | Conversion Arcana | the source record | converted text and a conversion receipt | X3 (2c7133da), X4 (93ca3f5e) | not built as a Doclab call; the API is live |
| `recognise` | Doclab Arcana | the source, or the converted text (the source when `convert` was skipped) | a transcription with page anchors | X5 (f5c304bc) | built for PDF and images on the operator's Apple Silicon Mac |
| `bundle` | Doclab Arcana | the transcription | a checked result bundle with a damage list | X5 (f5c304bc) | built |
| `kc-package` | Doclab Arcana | the result bundle | a `book-package/2` package | K5 (7c68d3d8, done), X5 (f5c304bc) | built (doclab-arcana#8) |
| `library` | Knowledge Contract | the package | a library entry with a stable registry id | X5 (f5c304bc), E2a (8b70ed28) | not built |
| `publish` | contract-place-api | the library entry | an allowlist row with digest and chunk count | X6 (7f4a6667) | built for corpus documents; no book class |
| `index` | kb-feeder and Scrutator | the published document | chunks in the knowledge base with a reader | X6 (7f4a6667) | built for the corpus; not for books |

**PIP-R001.** A chain MUST contain the stages in this order without a gap or a repeat, and MUST start at `intake`; it MAY stop after any stage, and only `classify` and `convert` MAY end `skipped`.

A stage is *finished* when its outcome is `done`. A `skipped` stage is not finished: it produces nothing and does not end the chain; `paused_safe`, `refused` and `failed` end it. A retry of a stage is a new chain for the same document, never a second receipt in the old one: the old chain keeps its record of the attempt that did not finish.

## 3. Document identity

**PIP-R002.** The pipeline key of a document MUST be `d_` followed by the lowercase hexadecimal SHA-256 of the exact bytes of the original file, as Doclab already writes it, and every receipt of the chain MUST carry that key unchanged.

A changed source is a new document with a new key; it is never an edit of the old one. Human-facing names (a book slug, a package identifier, work, edition and representation identifiers) are names that map to the key in the library registry; a location (a Drive identifier, a path, a server mirror) is never an identifier. The library of books moved from one Drive folder to another with every key intact, which is the case this rule exists for.

**PIP-R003.** The `intake` receipt MUST list exactly one input with role `source`, and it MUST be the digest that the key names; a chain whose key is not the digest of its own source is invalid. An `intake` that did not finish and lists no source is not judged.

This rule is reversible.

**PIP-R004.** If a Source Library decision (task E2) chooses a different pipeline key, this section MUST be amended by a pull request that restates the key, the mapping to the names above and the validator rule, and receipts written under this version stay valid under it.

## 4. Stage receipts

Each stage writes one `PipelineStageReceipt/v1` next to the artefacts it produced, in the bundle, the package directory or the library entry. These receipts are the authority.

**PIP-R005.** A library-level index of chains MAY exist as a derived view and MUST be rebuildable from them; it never decides a verdict.

A receipt records: the document key; the stage; a run identifier; the tool and its version; the host-clock start and finish; the outcome; for a refusal, a pause or a failure, a reason; the rights class at that stage; the SHA-256 of every input and every output; optional measurements; and the SHA-256 of the previous stage's receipt file. `kc2_admission` is always `not_measured`.

**PIP-R006.** An outcome of `done` MUST list at least one input and one output; `skipped` MUST give a reason and list no input and no output; `paused_safe`, `refused` and `failed` MUST give a reason and list no output.

A stage that did not finish therefore offers nothing that a later stage could consume.

**PIP-R007.** Each receipt after the first MUST carry the SHA-256 of the previous receipt's file bytes, and the first MUST carry null; the order of a chain is the order of its links, never of its file names.

**PIP-R008.** A stage MUST verify the digest of its predecessor's receipt and of each of its own inputs before it writes, and an absent or unverifiable predecessor MUST end the stage as `paused_safe`, not be guessed around.

**PIP-R009.** A stage that finished MUST list among its inputs at least one output of the nearest earlier stage that finished or, for `intake`, `classify`, `convert` and `recognise` only, the original source; no later stage MAY list the original source as an input.

**PIP-R010.** No receipt MAY follow a receipt whose outcome is `paused_safe`, `refused` or `failed`.

**PIP-R011.** A stage MUST NOT finish before it started or start before its predecessor finished.

A measurement is either `measured` with a value or `not_measured` with a reason and no value; "not measured" is never reported as a value, a pass or a fail.

## 5. Hand-off formats

The tables name the usual input of each edge; the rules of section 4 are the authority on what a stage may consume.

| Edge | What is handed over | Digest and validator |
| --- | --- | --- |
| intake → classify | the source record | the source digest, the key |
| classify → convert | the classification and the source | the record digest |
| convert → recognise | converted text and the conversion receipt, or nothing when `convert` was skipped (then recognise reads the source) | the text digest, or the source digest |
| recognise → bundle | the transcription with page anchors | the Doclab bundle manifest |
| bundle → kc-package | the result bundle | the bundle manifest digest |
| kc-package → library | a `book-package/2` package | [`check_book_package.py`](../../../tools/check_book_package.py) |
| library → publish | the library entry and its package digest | the allowlist row digest |
| publish → index | the published document | the index run receipt of the step-3 runner |

## 6. Rights and publication boundary

**PIP-R012.** A stage MAY keep the rights class of its predecessor or narrow it, and MUST NOT widen it; from least to most permissive the classes are `third_party_restricted`, `unknown` and `author_open`.

The rights class decides what leaves the machine. Text of a work that is not `author_open` stays out of public repositories; a package of such a work publishes no layer, as `book-package/2` already requires. Publication of any document in the Knowledge Contract corpus still passes the decision route (a decision pull request with independent reviews, then a row pull request, then the export). Nothing here authorizes a publication or a payment.

## 7. Failure, resume and idempotency

A stage that cannot proceed ends as `paused_safe` with a reason; it does not emit a broken artefact. Re-running a stage on the same inputs gives the same output digests, or a new chain whose receipt says why not. A partial output is never consumed: a stage that did not finish lists no output.

## 8. Conformance

The validator reads a directory of receipts and nothing else: a chain occupies a directory of its own, and a receipt kept next to a bundle's other files is copied there or referenced by it. It applies the schema to every file and then these rules, each with a stable refusal code. The requirement that a different pipeline key amends this document, the rule that a derived index is rebuildable and the rule that a stage verifies its predecessor before it writes are process requirements: they bind the stages and the people who amend this document, and no validator can check them from a chain.

| Code | Refusal |
| --- | --- |
| `PIPE-EMPTY`, `PIPE-READ`, `PIPE-SCHEMA` | no receipt in the directory; not strict JSON (duplicate member, BOM, invalid UTF-8), a symbolic link or a file over 1 MiB; or not matching the schema (unknown field, an unmeasured value with a number, `kc2_admission` other than `not_measured`, outputs on a stage that did not finish) |
| `PIPE-HEAD`, `PIPE-LINK`, `PIPE-FORK` | not exactly one head (a stray second chain, or none); a link naming no receipt of the chain (a receipt altered, removed or missing); a receipt with two successors |
| `PIPE-ID`, `PIPE-IDENTITY` | the key changes inside the chain; the key is not the digest of the original |
| `PIPE-STAGE-ORDER`, `PIPE-SKIP`, `PIPE-AFTER-STOP`, `PIPE-INPUT`, `PIPE-SOURCE`, `PIPE-TIME` | a stage missing, repeated, out of order or the chain not starting at `intake`; an essential stage skipped; a receipt after a paused, refused or failed one; no input from the nearest earlier finished stage (or, where allowed, the source); the original source listed as an input by a stage that may not read it; time running backwards |
| `PIPE-RIGHTS` | the rights class widened |

Twelve valid synthetic chains (all nine stages; `convert` skipped; `classify` and `convert` both skipped; one ending in a refusal at each of the nine stages) and twenty-seven mutants of the first, each with one defect and one expected code, are committed under `schemas/fixtures/pipeline/` and rebuilt by the tests; a test also mutates the validator and requires the fixtures to turn red. A passing chain says that the record is complete, ordered, linked, consistent about one document and one rights class, and honest about what was not measured. It says nothing about the quality of any stage.

## 9. What is and is not established

Of the nine stages, `kc-package` is built and merged, `recognise` and `bundle` are built for PDF and images on one host, `publish` and `index` are built for corpus documents only, and `classify`, `convert` as a Doclab call and `library` are not built. No runtime verdict is claimed for any of the three projects, and `kc2_admission` stays `not_measured`.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [attribution](../../../ATTRIBUTION.md).
