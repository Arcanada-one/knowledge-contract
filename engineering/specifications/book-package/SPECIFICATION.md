---
name: "book-package"
title: "Book Packages: Source Identity, Semantic Layers, and Validation"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "A concrete book-package schema, reversible conversion ledger, semantic layers, rights boundaries and synthetic conformance checks."
---

# Book Packages: Source Identity, Semantic Layers, and Validation

**Author:** Pavel Valentov · **Publication edition:** 1.1

| Implementation component | Scope |
| --- | --- |
| [Schema](../../../schemas/book-package.schema.json) | `book-package/2`, five `KCBook*/v2` record families |
| [Validator and projection](../../../tools/check_book_package.py) | Structural and cross-file checks, safe Markdown rendering, candidate rows |
| [Builder](../../../tools/build_book_package.py) | Wraps source bytes and supplied conversion output; does not interpret a book |
| [Synthetic fixtures](../../../schemas/fixtures/book-package/) | Invented source and negative records; no third-party book text |
| [Conformance tests](../../../tools/test_book_package.py) · [review regressions](../../../tools/test_book_package_review.py) | Validation, reversible edits, rights, scoped review, rendering and status derivation |

## 1. Purpose and validation boundary

A book package binds one source representation to its conversion, semantic records and review observations. This specification defines the implemented `book-package/2` profile. Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). Record validation does not establish conversion fidelity, semantic truth, actual reviewer independence, publication rights or task-specific admission.

**BPK-R001.** The manifest MUST declare `validation_profile: book-package/2`, and every record MUST use its `KCBookPackageManifest/v2`, `KCBookObject/v2`, `KCBookRelation/v2`, `KCBookEdit/v2` or `KCBookQuality/v2` tag.

Unknown versions are unsupported.

**BPK-R002.** A consumer MUST NOT silently reinterpret a version 1 record as version 2.

The **Knowledge Contract admission runtime** decides use under the [core contract](../knowledge-contract-core/SPECIFICATION.md). The inherited literal field `kc2_admission` is not a protocol version.

**BPK-R003.** Its value in producer records MUST remain `not_measured`; the producer cannot grant admission.

`not_measured` maps to assessment `unknown` with reason “no observation,” never to `pass`.

## 2. Layout and reversible edits

```text
<package_id>/
  manifest.json
  document.md
  readable.md
  assets/
  edits.jsonl
  objects.jsonl
  relations.jsonl
  quality.json
```

**BPK-R004.** The package identifier MUST be a readable lowercase hyphenated slug, 3–96 characters; a single letter followed by digits is forbidden.

`release_id` identifies the particular release separately.

**BPK-R005.** Component paths MUST remain relative and inside the package, with no parent traversal or symlinks.

`document.md` is the unchanged converter output.

**BPK-R006.** Accepted edits MUST target `readable_md`; `asset_text` has no supported digest-chain semantics and is rejected.

**BPK-R007.** A package without `document_md` and `readable_md` MUST NOT contain accepted edits or a built semantic layer.

**BPK-R008.** Each accepted edit MUST have a nonempty original and replacement, an anchor, basis, reason, actor, input digest and output digest.

**BPK-R009.** At its step, the original MUST occur exactly once, and the replacement MUST occur exactly once in the resulting text.

Occurrences include overlaps: `aa` occurs twice in `xaaay`.

**BPK-R010.** Applying the accepted edits in ledger order MUST produce `readable.md`; undoing them in reverse order MUST reproduce `document.md` exactly.

Insertions, deletions and ambiguous repeated-fragment edits are unsupported by this search-reversible profile.

**BPK-R011.** JSON readers MUST reject duplicate object member names at every depth, non-finite number tokens and a UTF-8 BOM, so independent readers cannot choose different rights or status values from the same record.

**BPK-R012.** All comparison and hashing MUST use exact bytes with strict UTF-8 decoding and no newline translation.

`\r\n`, `\r` and `\n` remain distinct. JSON Lines, `SHA256SUMS` and check lists split only on `\n`; one final newline is allowed, blank JSON Lines and lines ending in `\r` are rejected. U+2028, U+0085 and other control characters do not become additional record separators.

The edit lifecycle is `pending` → `accepted` or `rejected`; `stale` means an obsolete proposal whose base no longer matches, and is never replayed. Accepted ledger entries are immutable: a later correction creates another entry or a new package release. A stale proposal's declared or overlapping dependents remain unresolved until reassessed in a new valid record.

## 3. Identity and integrity observations

`work_id` identifies the work, `edition_id` the edition and language, and `representation_id` one source file. Translations and editions retain separate identities and anchors, with explicit `related_works` relations. A representation records its source digest, size, format, integrity (`verified`, `mismatch`, `unverified`) and completeness (`full`, `partial`, `bibliography_only`).

**BPK-R013.** A `verified` or `mismatch` integrity declaration MUST include `integrity_check` with `method`, `observer`, `checked_at`, `expected_sha256` and `observed_sha256`.

**BPK-R014.** The observed digest MUST equal the representation digest.

Verified integrity requires equal expected and observed digests; mismatch requires different digests.

**BPK-R015.** The expected digest MUST NOT be replaced to conceal a mismatch.

This is an attributed producer observation. The validator checks its shape and internal consistency; it cannot authenticate the expected digest's authority or reconstruct an unavailable source. The builder records whether its expected digest was supplied by the caller.

**BPK-R016.** A production consumer MUST authenticate the relevant observation at its declared trust boundary before treating it as evidence of source integrity.

**BPK-R017.** `document_md.input_sha256` MUST equal the representation digest and its component record MUST name the converter and version.

With no supported converter output, the package remains `adapter_required`; no empty or invented document substitutes for conversion.

## 4. Semantic objects and facets

An object identifies a concept, claim, procedure, figure, table, formula, code block, example or other structure.

**BPK-R018.** Every object MUST retain its text, language, origin, at least one source anchor, status and all eight facet fields: `representation_modes`, `content_kinds`, `discourse_functions`, `aboutness`, `source_position`, `semantic_operators`, `assessment_refs`, and `governance_refs`.

Qualifiers carry conditions and numeric units when present.

The facets implement a bounded profile of [semantic types](../semantic-types/SPECIFICATION.md). Representation modes include `text`, `image`, `audio`, `video`, `structured_data` and their explicit combinations. Source positions are `asserts`, `hypothesizes`, `presumes`, `denies`, `asks`, `reports_other_position`: `presumes` denotes a presupposition and is not a synonym of hypothesis.

**BPK-R019.** Operators include epistemic and deontic modality, quantifier, negation, condition, exception and order; each operator MUST name its scope.

A free-text qualifier condition applies to the whole object unless a scoped operator supplies the more precise binding.

The nineteen content-kind tokens are `definition`, `state_description`, `observation_measurement`, `generalization`, `explanatory_model`, `formal_model`, `procedure`, `structure_configuration`, `constraint_norm`, `goal_intent`, `preference_evaluation`, `argument_evidence`, `example`, `counterexample`, `question_problem_gap`, `narrative_episode`, `analogy_metaphor`, `hypothesis_interpretation`, and `commitment_speech_act`. This vocabulary is not an exhaustive taxonomy.

**BPK-R020.** Each facet MUST be `known` with a value, or `unknown`, `not_applicable` or `withheld` with an explicit reason and no value.

Known representation modes, content kinds, discourse functions and aboutness are nonempty by this profile's cardinality rule. Known-empty operators, assessment references or governance references assert an established empty set and are allowed only with that meaning.

**BPK-R021.** An object named by a package review MUST include that review's identifier in known `assessment_refs`; known-empty cannot deny the very review that cites it.

Unknown references remain unknown rather than empty.

**BPK-R022.** A `benchmark` claim MUST additionally record corpus, device, tool version, settings, units and mode.

Structural presence does not verify those declarations or establish task applicability.

## 5. Relations

A relation connects two existing, different objects of the same package with one of `defines`, `uses`, `variant_of`, `requires`, `compared_with`, `contradicts`.

**BPK-R023.** Every relation MUST retain its conditions, origin, evidence, endpoints and status.

Every relation has at least one evidence anchor tagged `from`, `to` or `both`.

**BPK-R024.** A `contradicts` relation MUST include separate `from` and `to` evidence, so one-sided attribution cannot masquerade as a two-sided finding.

**BPK-R025.** A relation touching a stale or rejected endpoint MUST itself be stale or rejected.

Review of a relation does not silently rehabilitate its endpoint.

## 6. Evidence anchors and source formats

**BPK-R026.** Every anchor MUST bind the same representation identifier and source digest as its manifest.

The implemented format-to-anchor mapping is exact:

| Anchor kind | Exact format tokens | Coordinates |
| --- | --- | --- |
| `page_bbox` | `pdf`, `djvu`, `ps` | page from 1; bounding box with positive area; origin and unit |
| `spine_offset` | `epub` | member `spine_item`, optional element path, start/end offsets |
| `section_block` | `html`, `md`, `txt`, `tex` | section and block identifiers |
| `sheet_range` | `xlsx` | sheet, cell range, `formula` / `cached_value` / `literal` layer |
| `json_pointer` | `json` | RFC 6901 pointer |
| `slide_block` | `ppt`, `pptx` | slide number and block identifier |
| none | `zip`, `tar_gz`, `sevenz` | opaque source identity only; archive member addressing is unsupported |

**BPK-R027.** Archives MAY be retained as an unavailable source requiring an adapter, but MUST NOT carry converter output, edits or semantic records under this profile.

A member-path anchor requires a separately versioned extension. DocC is not a format token; a DocC JSON file uses `json`.

The validator checks geometry, ordering and the declared mapping, not whether a cited source location exists or supports the text. Extracting a different representation creates a new binding; it does not justify reusing coordinates from the previous one.

## 7. Attribution and safe rendering

Origins are `author_statement`, `editor_correction`, `generated_meaning`, `generated_description`, `our_experiment` and `model_inference`.

**BPK-R028.** A non-author origin MUST have a generation record and `presented_as_author: false`.

**BPK-R029.** An author statement MUST NOT carry a generation record.

On an author statement, `presented_as_author: true` means an asserted verbatim quotation; `false` means an explicitly attributed paraphrase. This flag never establishes quotation fidelity by itself.

**BPK-R030.** The public Markdown renderer MUST preserve every object and relation field, including qualifiers, operator scopes, source position, conditions, anchors, generation and assessment references.

It emits each complete record in a JSON literal block, with a fence longer than any backtick run in the payload. Origin labels and record headings are emitted outside that container from controlled fields.

**BPK-R031.** Payload headings, HTML or apparent origin labels MUST NOT create new rendered record structure.

Every non-author block is visibly labelled “GENERATED, not the author's statement.”

`document_md.contains_generated_text` is always false; generated meanings and image descriptions remain separate derivatives. A missing asset records `missing_asset` without a fabricated path or digest. The public renderer refuses non-`author_open` packages.

## 8. Quality observations and readiness

Extraction and semantic observations remain separate; there is no combined score. Extraction statuses are `pass`, `partial`, `adapter_required`, `failed`, `not_measured`. Check results use the [status model](../status-model/SPECIFICATION.md): `pass`, `fail`, `unknown`, `not_applicable`. Each check has a unique identifier and method.

**BPK-R032.** A `not_applicable` check MUST state the inapplicability reason in `detail`.

**BPK-R033.** Extraction `pass` MUST contain at least one applicable passing check, no failed or unknown check, and matching seen/expected unit counts when those counts are supplied.

An empty checklist or an all-inapplicable checklist cannot prove successful extraction. `adapter_required` contradicts available converter output; `pass` or `partial` contradicts absent converter output.

CER is either measured with a value, reference class and sample size, or `not_measured` with null. A null is not a measured zero. Semantic status is `not_built`, `not_measured`, `built_unreviewed` or `reviewed`; the first two require empty object and relation files.

**BPK-R034.** Every semantic review MUST identify `review_id`, `reviewer_id`, `producer_id`, reviewer type, independence basis, time, result, the exact object and relation identifiers examined, and the current object-file, relation-file and readable-file digests.

**BPK-R035.** `sample_size` counts distinct reviewed objects, not relations or checklist items, and MUST equal the object-ID list length.

Reviews cannot name nonexistent records. A review of earlier bytes cannot be transferred to new bytes by changing only the timestamp.

**BPK-R036.** The `knowledge_ready` profile uses **complete coverage**, not a statistical sample: every object and relation MUST be included, every included record MUST be `reviewed`, the result MUST be `supported`, and the declared reviewer MUST be a human or blind agent distinct from the producer.

Same-session review, partial support, unsupported results and omitted records cannot earn this status.

**BPK-R052.** There MUST be at least one object.

A narrower review is retained honestly under `partial_pilot`.

These checks verify declared scope, separation and byte bindings. They do not prove that a human review occurred or that identities are independent. The synthetic fixture uses explicitly invented reviewer identities for testing. Authenticating observations belongs to the consuming trust boundary.

### Total package-status decision table

**BPK-R037.** The validator MUST compute the first matching row below and require equality with the submitted `package_status`.

All well-formed combinations receive one result; contradictory component/check declarations are additionally rejected rather than assigned a success status.

| Priority | Condition | Derived status |
| --- | --- | --- |
| 1 | Source integrity is `mismatch`, even if completeness is bibliographic | `blocked_integrity` |
| 2 | Completeness is `bibliography_only` | `bibliography_only` |
| 3 | Converter output is absent | `adapter_required` |
| 4 | Semantic layer is `not_built` or `not_measured`, with zero objects and relations | `structure_only` |
| 5 | Full, verified source; extraction passes; complete independent declared review supports all reviewed records | `knowledge_ready` |
| 6 | Any remaining well-formed converted package | `partial_pilot` |

**BPK-R038.** `blocked_integrity`, `bibliography_only` and `adapter_required` MUST omit both document and readable components.

**BPK-R039.** `structure_only`, `partial_pilot` and `knowledge_ready` MUST contain both.

A reviewed package with unverified integrity or partial source coverage is therefore representable as `partial_pilot`. Extraction failure remains visible even when files are structurally present.

## 9. Correction impact and reassessment

**BPK-R040.** An accepted correction MUST invalidate every object explicitly named in `depends_on_objects` **or** whose source anchor overlaps the edit.

The producer's dependency list cannot suppress the overlap rule. Section/block and slide/block matches are exact; intervals and comparable page boxes use intersection; JSON pointers use equality or ancestor relationships. Sheet ranges conservatively invalidate the whole same-sheet scope; incomparable geometry is treated as potentially overlapping.

**BPK-R041.** An affected object MUST be stale or rejected until its `reviewed_edit_ids` explicitly names the accepted corrections and a supported, independent declared review covers that object and the current readable and semantic file digests.

References to unknown or unaccepted edit identifiers are rejected. A stale proposal cannot be cleared by this accepted-edit mechanism. Dependent relations follow section 5. This is a declared reassessment record, not evidence that a producer's semantic reasoning was correct.

## 10. Rights and publication layers

`rights.license_class` is `author_open`, `third_party_restricted` or `unknown`.

**BPK-R042.** Only `author_open` MAY declare the package publication `license` (`CC-BY-4.0` or `Apache-2.0`) and nonempty `publishable_layers`.

**BPK-R043.** Restricted or unknown works MUST omit that licence field and leave the publication layer list empty.

This blocks book text carried through semantic chunks as well as through document files. No quotation budget or right to republish is inferred from extraction, review or a producer-supplied licence string.

Private processing of an otherwise valid restricted package is outside public projection.

**BPK-R044.** The projection function MUST return no rows for such a package.

This conservative producer rule implements the established exclusion of third-party book text from the repository; it is not a legal finding about possible uses elsewhere. Any separately authored derivative requires its own source/rights assessment and publication decision.

## 11. Candidate export and admission runtime

**BPK-R045.** `candidate_projection(package_directory)` MUST validate a private immutable byte snapshot and compute the rendering from that snapshot itself.

It does not accept a raw manifest plus caller-selected Markdown.

**BPK-R046.** It MUST return no rows on validation failure or for `blocked_integrity`, `bibliography_only` or `adapter_required`, or without an allowed open publication licence.

| Package element | Candidate projection |
| --- | --- |
| Allowed document/readable Markdown | One proposed row for its exact bytes |
| Allowed knowledge layer | One proposed `knowledge.md` row for the full protected rendering |
| JSON records, assets and quality file | Retained in the package; not separate Markdown export rows |
| Unlisted layer or prohibited status/rights class | No row |
| Runtime admission | Remains `not_measured` |

Rows identify `articles/book-packages/<package_id>/<file>`, digest, holder, licence, limits and `status: proposed`. These paths fit the exporter path syntax but are not automatically allowlisted. The existing `KnowledgeContractCandidateExport/v2` exporter still requires its own admitted scope, exact merged revision and reviewed publication decision.

**BPK-R047.** The producer MUST NOT widen that scope or treat a candidate row as publication or runtime admission.

The [API integration appendix](../../../appendices/api-integration/APPENDIX.md) distinguishes repository publication, index admission and actual service results. No live consumer acceptance of this new profile is claimed by local conformance tests.

## 12. Validation and evidence limits

The JSON Schema checks record shape, fixed vocabularies and conditional fields. The package validator adds digest and count checks; identity and endpoint consistency; anchor mapping and geometry; byte-exact reversible replay; correction impact; extraction conjunction; review scope and file bindings; complete status derivation; and publication rights boundaries.

**BPK-R048.** The conformance suite MUST retain each regression's expected cause, including negative review, unknown extraction, restricted licence bypass, arbitrary rendering, Markdown structure injection, stale correction, rejected endpoint and obsolete profile.

Its status-table test enumerates 3,240 input combinations; enumeration tests the decision table, not 3,240 historical book experiments. Structural incoherence is tested separately.

The package does not establish source fidelity, truth, real reviewer independence, unseen source geometry, authentic licence ownership or downstream admission. Generated descriptions are separate from the media they describe. The linked [transcription study](../../studies/source-transcription-and-uncertainty/STUDY.md) reports historical evidence; it is not validation of the new wire profile.

## 13. Compatibility and migration

Version 1 is preserved at immutable [source revision ed2e188c](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e). Version 2 is intentionally stricter and adds observations, scoped review, the readable package identifier, explicit validation profile and semantic vocabularies.

**BPK-R049.** Existing record tags MUST NOT simply be rewritten: missing observations remain missing, unsupported edits remain unsupported, and review of old bytes does not establish review of migrated bytes.

**BPK-R050.** A migration MUST create a new package release, retain the original revision, identify every mapping or dropped unsupported field, revalidate digests and edits, and obtain any newly required review.

**BPK-R051.** It MUST NOT invent integrity observations, reviewer identities or author attribution.

V2 builders emit empty semantic layers until interpretation is actually performed. The publication edition, package profile, validator build and admission-runtime version remain distinct identities.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [attribution](../../../ATTRIBUTION.md).
