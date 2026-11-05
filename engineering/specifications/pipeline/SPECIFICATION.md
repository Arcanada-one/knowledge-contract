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
| [Fixtures](../../../schemas/fixtures/pipeline/) · [generator](../../../tools/pipeline_fixture.py) | Thirteen valid chains and forty-one one-defect mutants |
| [Tests](../../../tools/test_pipeline_receipts.py) | The validator against every fixture, drift of the committed files, mutants of the validator |
| [Document class canon](document-classes.json) · [result schema](../../../schemas/document-classification.schema.json) | `kc-doc-class/1` and `DocumentClassification/v1` (§10) |
| [Classification checker](../../../tools/check_document_classification.py) · [fixtures](../../../schemas/fixtures/document-classification/) · [generator](../../../tools/document_classification_fixture.py) · [tests](../../../tools/test_document_classification.py) | Twelve boundary cases and the one-defect mutants (§10) |

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

### Recognition by import

Recognition outputs can exist before any receipt does. They are not re-run to manufacture a history, and no receipt is written for a run that cannot be shown to have happened. What the pipeline records instead is an **import**: the existing outputs are verified against the source bytes at the time of the import, and the receipt says that this, and nothing more, was done.

**PIP-R023.** The `recognise` stage MAY be performed by an import adapter that verifies existing recognition outputs against the source bytes now, instead of running recognition. The receipt of such an adapter MUST name the import in `tool.name` (a name ending in `-import`), MUST give the actual start and finish of the verification as `started_at` and `finished_at`, MUST list as `outputs` the existing recognition outputs that were verified, each by the SHA-256 of its exact bytes, and MUST list as `inputs` what PIP-R009 allows (the source, in a chain whose `classify` and `convert` were skipped) and MAY list the earlier evidence files by digest.

**PIP-R024.** An import receipt that finished MUST carry the measurement `recognition_executed` as measured with the value `false`, and the measurements `original_run_id` and `original_finished_at`, each either measured (read from the earlier evidence) or `not_measured` with a reason. A quality or damage figure taken from the earlier evidence MUST be named `recorded_` followed by its name and is a figure as recorded, never one measured again by the import.

**PIP-R025.** A receipt whose tool does not name an import MUST NOT claim `recognition_executed` as `false`; a receipt whose tool names an import, whatever its outcome, MUST NOT claim `recognition_executed` as anything but measured `false`; a receipt MUST NOT carry the measurements `recognition_executed`, `original_run_id` or `original_finished_at` twice; and an import adapter exists for the `recognise` stage only.

**PIP-R026.** A chain with an imported `recognise` is a new chain for the same document key: it starts at `intake` with the source hashed at the time of the import, `classify` MAY end `skipped`, the earlier recognition outputs and evidence are kept unchanged and referenced by digest only, and the rights rules of PIP-R012 and PIP-R027 apply to it as to any chain (the receipts carry the rights state known at each stage, which for an imported book is `unknown`, or `third_party_restricted` when that is known; the determination of the work's rights is in the package's rights record). A receipt never claims work that was not done: a stage that did not run is recorded `skipped` with its reason where PIP-R001 allows it (`classify` and `convert`), and otherwise the chain stops; the imported `recognise` is the one case of a stage that verified and did not run, and it says so by `recognition_executed` measured `false`. A consumer that needs recognition to have been executed MUST read `recognition_executed`; a checker that accepts the chain does not say that it was. The absence of the measurement means that it is not established, never that recognition ran, and a `true` is the producer's statement; an import presented under the name of an ordinary recognition tool and without the measurement cannot be told from a run by its receipt. The checker reads receipts only: that the verified outputs match the source bytes is established by the importer at the time of the import and by nothing in the chain. The recorded-figure naming, the choice of the rights class and a non-empty `original_run_id` are rules of the producer that the checker does not enforce, and the match of `-import` is exact and case-sensitive.

**PIP-R028.** In a chain whose `recognise` is an import, the `bundle` stage MAY verify an existing bundle instead of assembling it, and when it does it MUST record that with the measurements `bundle_assembled` measured `false` and `bundle_verified` measured `true`, and lists the verified bundle manifest by the SHA-256 of its exact bytes as its output; its tool does not name an import (PIP-R025 allows that name on `recognise` only). The two measurements are carried together on the `bundle` stage and nowhere else, each measured `true` or `false`, and `bundle_assembled` `false` is valid only after an imported `recognise`; an ordinary bundle stage needs neither. The checker reads the two measurements, that they are booleans, that they are carried on the `bundle` stage and that `bundle_assembled` `false` follows an imported `recognise`; it does not check that the output is the hash of the verified manifest (only that the next stage consumes it) and it does not look at the outcome of the bundle receipt, so that the verification really took place is the producer's statement; a bundle that was verified and carries neither measurement reads as an ordinary assembly.

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

**PIP-R012.** A stage MAY keep the rights class of its predecessor or narrow it, and MUST NOT widen it; from least to most permissive the classes are `third_party_restricted`, `unknown`, and then `public_domain` and `author_open`, which are equally open.

**PIP-R027.** The rights class a receipt carries MUST be the rights state known at that stage, and a determination of the rights of a work (for example `public_domain` with its evidence) MUST be made only in the package's rights record, never in a receipt; a chain that starts at `unknown` does not end at `public_domain`, and the receipt classes and the package's rights record are read separately. The checker refuses only a widening of the class along a chain (PIP-R012); that a receipt carries the state known at its stage, and that a determination is made in the package's rights record and not in a receipt, are rules of the producer that it does not check: a chain whose receipts all carry `public_domain` is not refused by it, and a reader MUST take the rights of a work from the package's rights record.

The rights class decides what leaves the machine. Text of a work whose class is neither `author_open` nor `public_domain` stays out of public repositories, and a package of such a work publishes no layer, as `book-package/2` already requires; a `public_domain` package publishes layers on the evidence record described in §9, the layers Arcanada writes only under the licence that record names. Publication of any document in the Knowledge Contract corpus still passes the decision route (a decision pull request with independent reviews, then a row pull request, then the export). Nothing here authorizes a publication or a payment.

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
| `PIPE-IMPORT` | a bundle verified instead of assembled without a verified bundle, outside an imported chain or with one of the two bundle measurements missing or on another stage; a `recognise` receipt of an import adapter without `recognition_executed` measured `false`, with it claimed otherwise at any outcome, or (when finished) without `original_run_id` and `original_finished_at`; `recognition_executed` `false` on a tool that does not name an import; one of the five import and bundle measurements twice; an import name on a stage other than `recognise` |

Thirteen valid synthetic chains (all nine stages; `convert` skipped; `classify` and `convert` both skipped; an imported `recognise`; one ending in a refusal at each of the nine stages) and forty-one mutants of the first, each with one defect and one expected code, are committed under `schemas/fixtures/pipeline/` and rebuilt by the tests; a test also mutates the validator and requires the fixtures to turn red. A passing chain says that the record is complete, ordered, linked, consistent about one document and one rights class, and honest about what was not measured. It says nothing about the quality of any stage.

## 9. Public-domain works and declared damage in `book-package/2`

This section is the repository-only note of an amendment of the `book-package/2` rules that is pending a later edition decision batch; the published [book package specification](../book-package/SPECIFICATION.md) is unchanged until that batch. Until a package exists in a library, the amendment changes no migration: it is made in place, and the profile string stays `book-package/2`.

A fourth rights class, `public_domain`, lets a work whose term has expired be carried and published. It is not `author_open` and it is not a licence: the manifest carries a `public_domain` record with a basis, the jurisdictions (or `worldwide` with its reason), at least one `https` evidence address, the time of the determination and who made it, and two facts kept apart, each with its own basis: the **work** (`term_expired`) and the **digital copy** (`open`, with the digitiser's terms: CC0 1.0, a public-domain mark, a public-domain statement, or no restriction stated). A `public_domain` package has no top-level `license` (it cannot be expressed); the layers that Arcanada writes (the knowledge layer, the quality report) are published only under `public_domain.own_layers_license`, which covers exactly those two layers, and the public-domain text is covered by the evidence record alone. The restricted and unknown classes publish nothing, as before.

A package may carry a declared damage list in its quality report: a status (`none` or `declared`), the number of places, and one declaration per kind with its count and its places (page, block, what, a short quote). The places are the sum of the declaration counts. A package with declared damage cannot derive `knowledge_ready`.

**PIP-R013.** The damage list travels with the package and is shown wherever the package is shown; a library that publishes a package with declared damage MUST publish the list with it and MUST NOT present the package as clean.

If a different rights model is adopted by the edition batch before any package is merged into a library, the one package written under this amendment is migrated by a new release; the amendment and its fixtures are then replaced, not extended.

## 10. Document classes (`kc-doc-class/1`)

The `classify` stage says what kind of content unit a source is, so that a later stage can choose how to read it. This section is the repository-only canon of the classes, the way an uncertain answer is recorded, and the way a result is bound to the receipt chain. It does not release anything: it is not in the publication catalogue and no export reads it.

Classification concerns the content unit the source represents. It is not the file extension, the transport, the quality of the copy, the rights class or the intended use. Edition, language, volume, media type, the recognition method (OCR or native text), the acquisition channel and the storage location are separate attributes and are not classes. The kinds of the Knowledge Contract (role, skill, competency, blueprint, constraint, work item) and the document types of the publication catalogue are separate vocabularies.

| Class | Definition | Boundary |
| --- | --- | --- |
| `book` | A book or an independently identifiable book volume, with an evidenced bibliographic identity and an authorial or editorial structure. | An ISBN or a page count is not a required test. A verified fragment of a book keeps the book identity, and its partial coverage is stated in the result. |
| `paper` | A standalone article, preprint, or research or technical report that addresses a bounded subject as its own publication. | Length and peer-review status do not by themselves make a source a book, and a paper's class proves nothing about its claims. |
| `export` | A contextual archive of an application, a workspace or a correspondence, treated as that archive: its records, their order, participants, relationships and state are retained. | Saving a book or a paper out of an application does not make the saved file an export. |
| `dataset` | A standalone structured collection of observations, examples or records with a data schema or a dataset description. | A table exported from a database with described columns can be a dataset; tables inside a paper do not change the paper's class. |
| `other` | A source of a recognised type that lies outside the four classes above. | An invoice or a slide deck can be `other`. A source that is unreadable or whose type is uncertain is not `other`: it is `unknown` or `ambiguous`. |

The same table is the machine-readable canon [`document-classes.json`](document-classes.json), whose exact bytes are identified by their SHA-256.

A result is a separate file, `classification.json`, tagged `DocumentClassification/v1` ([schema](../../../schemas/document-classification.schema.json)). It names the document key, the taxonomy and the canon digest, the status, the class and the candidates, a reason where one is required, the coverage (`complete`, `partial` or `not_measured`), the classifier (name, version, method), the evidence and the confidence.

**Statuses.** `classified` carries one class and that class as the only candidate. `ambiguous` carries no class, at least two distinct candidates among `book`, `paper`, `export` and `dataset`, and a reason. `unknown` carries no class, no candidate and a reason. `other` is a class of its own and never stands for an ambiguous or an unknown source; because it is the residual class and has no positive features of its own, it is not one of the competing candidates of an `ambiguous` result, and a source that might be a recognised type outside the four positive classes is recorded as `unknown` with the reason, or as `ambiguous` between the positive classes it may be.

**PIP-R014.** A classification result MUST name the taxonomy `kc-doc-class/1` and the SHA-256 of the exact bytes of the canon file, and a result that names another taxonomy identifier or another digest MUST be refused and MUST NOT be read against the latest canon.

**PIP-R015.** A `classified` result MUST carry exactly one class and exactly that class as its only candidate, an `ambiguous` result MUST carry no class, at least two distinct candidates and a reason, and an `unknown` result MUST carry no class, no candidate and a reason.

**PIP-R016.** (A rule of the classifier's behaviour, not one the schema or the checker can verify.) A classifier MUST NOT use the class `other` for a source whose class is uncertain, and MUST NOT choose between candidates by an arbitrary priority; it MUST record the alternatives it found.

**PIP-R017.** A result MUST NOT carry an invented number as confidence: when no calibrated assessment exists it MUST say `not_measured` with a reason, and a measured score MUST name its method, its version and its interpretation.

**PIP-R018.** A result MUST identify, by SHA-256 and by a selector, a rule or a feature, the representation that was actually inspected, and MUST state whether the coverage of the unit is complete, partial or not measured.

**PIP-R019.** The classify receipt of a finished stage MUST list the exact bytes of the result as one output with the role `classification` and their `sha256`, and the receipt schema MUST NOT gain a field for a class or a taxonomy.

A `classify` stage that is skipped still produces nothing and no class. A result of status `unknown` is a finished observation: processing that is safe for the media type alone can go on, and the receipt chain of §4 is unchanged.

**PIP-R020.** A stage that needs a particular content class MUST NOT proceed on an `ambiguous` or an `unknown` result by choosing a class itself.

**PIP-R021.** A classification MUST NOT change the rights class, the declared damage, the `knowledge_ready` status, publication, indexing or `kc2_admission` of the document; it is provenance for later stages and never an admission.

**Migration from `kc-doc-class/0`.** The temporary set existed only as text in a task title and in one letter to the implementer. Its identifiers were `book`, `paper`, `edition`, `export`, `dataset` and `other`; the letter dropped `edition`, and the set was labelled `kc-doc-class/0`. There was never an `article` identifier. No code and no stored data carry any class value, because no classifier has been written yet, so there is nothing to convert. `/1` keeps the five identifiers `book`, `paper`, `export`, `dataset` and `other`; `edition` is an attribute, not a class.

**PIP-R022.** A classification under a later taxonomy MUST be a new result for the same document key with its own receipt chain, the earlier results MUST be kept, and a change of storage location MUST change neither the key nor the class.

The twelve boundary cases are committed as valid results under `schemas/fixtures/document-classification/valid/`: a complete book with evidenced identity and declared damage (the damage stays in the quality report and is not an input of the class); the same book saved as a PDF from a drive; a chapter whose parent book is verified (a book with partial coverage); a standalone preprint or long report; a complete journal issue of several independent papers (`other`); a contextual chat or email archive; an independently packaged labelled dialogue corpus with a dataset manifest; a database CSV with described columns; a paper containing tables and measurement appendices; a recognised invoice or slide deck (`other`); an unreadable scan without metadata (`unknown`); and a source with unresolved book-versus-report evidence (`ambiguous`). Passing them states the outcome for those cases and nothing about the accuracy of any classifier. Thirty-one one-defect mutants under `invalid/`, each with one expected refusal code, are rebuilt by the tests.

| Code | Refusal |
| --- | --- |
| `DCL-READ`, `DCL-SCHEMA` | not strict JSON (duplicate member, BOM, invalid UTF-8) or over 1 MiB; not matching the schema, including every status, class and candidate rule, a confidence number without a measurement, missing evidence or coverage |
| `DCL-TAXONOMY`, `DCL-CANON` | a taxonomy identifier other than `kc-doc-class/1`; a canon digest that is not that of the canon file |
| `DCL-INVARIANT` | the status, class and candidate rules broken (checked again outside the schema) |
| `DCL-BINDING` | the classify receipt does not list the exact bytes of the result as its single `classification` output, or names another document |
| `DCL-CANON-FILE` | the canon file disagrees with the schema (class ids, statuses) or defines another taxonomy |

A passing check means the result is well formed, bound to one canon and one document, and honest about what was not measured. It does not mean that the class is right.

## 11. What is and is not established

Of the nine stages, `kc-package` is built and merged, `recognise` and `bundle` are built for PDF and images on one host, `publish` and `index` are built for corpus documents only, and `classify`, `convert` as a Doclab call and `library` are not built (§10 specifies the classification result; no stage writes one yet). No runtime verdict is claimed for any of the three projects, and `kc2_admission` stays `not_measured`.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [attribution](../../../ATTRIBUTION.md).
