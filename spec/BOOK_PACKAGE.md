---
artifact_id: KC_BOOK_PACKAGE
revision_id: KC_BOOK_PACKAGE-r1
title_en: "Book Package: from a source book to Markdown, meanings and a relation graph"
language: en
status: draft specification
scientific_status: concept_draft
license: CC-BY-4.0
sources: none
---

# Book Package: from a source book to Markdown, meanings and a relation graph

| Field | Value |
| --- | --- |
| Artifact id | KC_BOOK_PACKAGE (revision r1) |
| Status | draft specification; not a finished result |
| Schema | [`schemas/book-package.schema.json`](../schemas/book-package.schema.json) (Apache-2.0) |
| Validator | `tools/check_book_package.py` (Apache-2.0) |
| Fixtures | `schemas/fixtures/book-package/` (synthetic, invented for this repository) |
| Licence | CC BY 4.0 |

## 1. Purpose and what this document does not claim

A book package is the unit in which one source representation of a book (one file) is carried through conversion into Markdown, semantic description and a relation graph, so that the result can travel inside the Knowledge Contract as a candidate. This document fixes the **format**. It makes no claim that any conversion is faithful, that any extracted meaning is correct, or that any package is admitted by the Knowledge Contract runtime (KC2). Every record carries `kc2_admission: not_measured`; a value of `admitted` is rejected by the schema, because admission is decided elsewhere and never by the producer.

Passing the validator proves structure: shapes, digests, counts, endpoints, anchor identity and status coherence. It does not prove that the text of an anchor says what an object claims. That is the job of review, recorded separately in the quality report.

## 2. Layout

```text
<package_id>/
  manifest.json      identity, source binding, components with digests, rights, status
  document.md        faithful conversion of the source; no generated text
  readable.md        readable edition; the only file edits may change
  assets/            images and other extracted resources
  edits.jsonl        edit ledger: one record per change from document.md to readable.md
  objects.jsonl      semantic objects
  relations.jsonl    relations between objects
  quality.json       quality report
```

`document.md` is never edited. A correction goes into `readable.md` through a ledger record that holds the source fragment, the replacement, the anchor, the basis, the reason and the input and output digests. Every accepted edit is reversible (`reversible` is the constant `true`). The ledger is tied to the files: the digests chain from `document.md` through each accepted edit, each `original_text` must occur in the text it edits, and `readable.md` must equal the replay of the accepted edits over `document.md`. Paths are relative, contain no `..`, and never start with `/`.

## 3. Identity and source binding

Three identifiers are kept apart: `work_id` (the work), `edition_id` (edition and language) and `representation_id` (one file). Translations of one work share a `related_works` relation (`translation_of`, `edition_of`, `same_work_as`, `packaged_with`) and keep separate editions, languages and evidence. The manifest holds the SHA-256 and size of the source representation, its format, an `integrity` state (`verified`, `mismatch`, `unverified`) and a `completeness` state (`full`, `partial`, `bibliography_only`). Rules enforced:

- `mismatch` forces `package_status: blocked_integrity`; the expected hash is never replaced to make a package pass.
- `bibliography_only` forces `package_status: bibliography_only` and forbids `document_md`; such a record is never queued as a full text.
- `knowledge_ready` requires `verified` integrity and `full` completeness.
- `document_md.input_sha256` equals the source representation hash, and names the converting tool and version.

## 4. Semantic objects

An object (`KCBookObject/v1`) is a concept, claim, procedure, figure, table, formula, code block, example or other structure. It carries its text, language, origin, evidence anchors (at least one), qualifiers (conditions, numbers with units) and the eight semantic facets of [SEMANTIC_TYPES](SEMANTIC_TYPES.md): `representation_modes`, `content_kinds`, `discourse_functions`, `aboutness`, `source_position`, `semantic_operators`, `assessment_refs`, `governance_refs`. Each facet is present. A facet is either `known` with a value, or `unknown`, `not_applicable` or `withheld` with a reason and no value; absence of information is never an empty list. `content_kinds` uses the eighteen rubrics of the SEMANTIC_TYPES crosswalk; the combined example and counterexample rubric is split into two values, so the schema lists 19. A claim of class `benchmark` must carry corpus, device, tool version, settings, units and mode (`encode`, `decode`, `encode_decode`).

## 5. Relations

A relation (`KCBookRelation/v1`) connects two objects of the package and has one of six types: `defines`, `uses`, `variant_of`, `requires`, `compared_with`, `contradicts`. It carries evidence anchors tagged with the side they support (`from`, `to`, `both`). Rules:

- at least one anchor is required for every type;
- `contradicts` needs an anchor for the `from` side and an anchor for the `to` side, because a contradiction asserted from one side only is a reading, not a finding;
- an object may not be related to itself; endpoints must exist in the same package;
- a relation that touches a stale object is stale or rejected (section 9).

## 6. Evidence anchors

Every anchor repeats the `representation_id` and the source `sha256` it points into; the validator rejects an anchor that names another representation or source. Coordinates are never bare numbers.

| Kind | Source formats | Fields |
| --- | --- | --- |
| `page_bbox` | PDF, DjVu, PS after conversion | `page` (from 1), `bbox` (4 numbers, positive area), `bbox_origin`, `bbox_unit` |
| `spine_offset` | EPUB | `spine_item`, optional `element_path`, `start`, `end` (end not before start) |
| `section_block` | HTML, MD, TXT | `section_id`, `block_id` |
| `sheet_range` | XLSX | `sheet`, `range`, `layer` (`formula`, `cached_value`, `literal`) |
| `json_pointer` | JSON, DocC | `pointer` (RFC 6901) |
| `slide_block` | presentations | `slide`, `block_id` |

A new source format needs a new anchor kind in a new schema revision, not a loose string. The validator requires the anchor kind to fit the source format of the manifest (for example `page_bbox` for PDF, `section_block` for Markdown). It does not resolve an anchor against the source: that a section, page or range exists, and that it says what an object claims, is not checked here.

## 7. Generated content is marked, always

Every object and relation has an `origin`: `author_statement`, `editor_correction`, `generated_meaning`, `generated_description`, `our_experiment` or `model_inference`. Everything except `author_statement` must carry a `generation` record (tool, version, optional model id, run id, input digest, time) and must set `presented_as_author` to `false`. An `author_statement` must not carry a `generation` record. Machine descriptions of illustrations and generated meanings live only in the object file; `document_md.contains_generated_text` is the constant `false`, and `readable_md` declares whether it holds any. The rendering of the knowledge layer to Markdown labels every generated block "GENERATED, not the author's statement". A missing asset is `state: missing_asset` with no path and no digest; no image or description is invented for it.

## 8. Quality report: extraction and semantics apart

`quality.json` has two blocks that never merge. `extraction` holds a status (`pass`, `partial`, `adapter_required`, `failed`, `not_measured`), expected and seen units, a list of checks (`pass`, `fail`, `unknown`, `not_applicable`, each with a method) and a CER block. CER is either `measured` with a value, a gold or silver reference class and a sample size, or `not_measured` with value `null`; a null is not a zero. `semantics` holds a status (`not_built`, `built_unreviewed`, `reviewed`, `not_measured`), object and relation counts and, when reviewed, the reviewer type, sample size and result. `not_built` and `not_measured` force both counts to zero: an empty graph means that the semantic layer was not built, never that the book has no support for a question. There is no combined score; the schema rejects one.

`package_status` is derived, not chosen freely: `knowledge_ready` requires extraction `pass` and semantics `reviewed`; `structure_only` requires semantics `not_built`.

## 9. Staleness

A source span corrected after objects were derived from it makes those objects stale. The validator requires: an object listed under `depends_on_objects` of a `stale` edit is `stale` or `rejected`, and so is every relation that touches a stale object. A new context package must not reuse a stale quotation.

## 10. Rights and layers

`rights.license_class` is `author_open`, `third_party_restricted` or `unknown`; `publishable_layers` lists what may leave the producer: `document_md`, `readable_md`, `assets`, `knowledge`, `quality`. A work that is not `author_open` may not publish `document_md`, `readable_md` or `assets`. This is a producer-side guard, not a legal opinion; whether the knowledge layer of a restricted work may quote it is a rights question for the publication decision.

## 11. Mapping to candidate export v2 and Knowledge Contract V3 admission

The candidate exporter (`tools/export_corpus.py`, schema `KnowledgeContractCandidateExport/v2`, DEC-AUP-0171) carries only Markdown files whose path matches its path pattern under `papers/`, `spec/`, `articles/` or `schemas/`, that are listed in its explicit scope, have a merged source commit and a reviewed publication decision with a personal-name rights holder and a licence of CC-BY-4.0 or Apache-2.0. A package therefore maps as follows, as a **proposal** that the exporter's own rules still decide.

| Package element | Candidate export v2 element |
| --- | --- |
| `document.md`, `readable.md` (only if listed in `publishable_layers`) | one entry each: `path`, `content sha256`, rights holder, licence, `status: current` |
| objects and relations | not carried as JSON; rendered to one Markdown file (`render_knowledge_markdown`) which becomes one entry |
| `manifest.json`, `objects.jsonl`, `relations.jsonl`, `edits.jsonl`, `quality.json`, assets | not carried (not Markdown); stay in the package and are referenced by digest |
| `rights.holder`, `rights.license` | publication decision `rights_holder` and `license`; the exporter requires a personal name as holder and CC-BY-4.0 or Apache-2.0 as licence, so a layer without `rights.license` gets no row; `rights_basis`, `third_party` and `attribution` are written by the publication step |
| `package_status`, quality blocks | `limits` text of the decision (built by `candidate_projection`); a proposed row has status `proposed`, and only the exporter's allowlist makes it `current` |
| layer not in `publishable_layers` | no allowlist row; an absent row means deny |
| `kc2_admission: not_measured` | `kc2_admission: not_measured` (the exporter sets it; a producer cannot) |

`candidate_projection` proposes such rows, with the repository path `articles/book-packages/<package_id>/<file>`. That path fits the exporter's path pattern but is not in its scope list. The function does not widen the exporter's scope: `SCOPE_PATHS` is an explicit list and widening it, or adding a path pattern for packages, needs a new decision in the programme record. Until then this specification is itself not an indexing input, and the mapping has not been tried against a real exporter run. Admission under [KNOWLEDGE_CONTRACT_V3](KNOWLEDGE_CONTRACT_V3.md) is a separate step performed by the runtime resolver; a package supplies identity, sources, scope and conditions, and is a candidate until that step records otherwise. No consumer of the v2 manifest was available to the author of this revision, so acceptance by the downstream indexer is **not measured**.

## 12. Validation

1. The JSON Schema checks the shape of each record and the conditional rules above (origin and generation, contradicts sides, CER null, not-built counts, status coherence, benchmark context, paths, admission constants).
2. `tools/check_book_package.py <dir>` adds the cross-file rules: file digests, counts, unique identifiers, endpoint existence, package, work and edition identity, anchor identity, geometry and fit to the source format, ledger chain and replay, staleness coupling, quality counts, status derivation, rights versus layers.
3. Positive fixtures: one synthetic package and one object per anchor kind. Negative fixtures: one file per violated rule, regenerated byte for byte by `tools/book_package_fixture.py`.
4. Mutation tests: every negative fixture is rejected for its own named reason, and every cross-file mutation of the valid package is reported with its expected message. A mutation that is accepted, or rejected for another reason, fails the build.

These checks establish that the validator distinguishes the listed violations. They do not establish that the list is complete, that the fixtures resemble real books, or that a conversion is faithful.

## 13. Limits and open points

- The format is exercised only on a synthetic fixture. No real book has been converted by this specification yet.
- `generation.input_sha256`, `size_bytes` of the source and the existence of an anchored section are recorded but cannot be verified from the package alone.
- A fixture marked `reviewed` records a review that the fixture does not prove took place.
- Extraction quality and semantic quality are defined as separate blocks; no threshold for either is fixed here.
- Right-to-left scripts, vertical Japanese and ruby are not covered by any anchor refinement; coverage of them is `not_measured`.
- Whether the downstream indexer accepts the Markdown rendering is not measured.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [ATTRIBUTION.md](../ATTRIBUTION.md).
