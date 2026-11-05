---
name: "source-transcription-and-uncertainty"
title: "Reproducible transcription is not preservation of uncertainty"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Retained generated descriptions, lost uncertainty and a reproducible synthetic projection counterexample."
study_type: "corpus-and-projection-audit"
review_state: "internally-reviewed"
---

# Reproducible transcription is not preservation of uncertainty

## Abstract

An audit of three book-export packages found that their readable Markdown could be reconstructed byte for byte while omitting every one of 153 explicitly recorded uncertainty fields attached to generated illustration descriptions. The underlying structured records remained intact. A separate derivative projection preserved all 153 fields and labeled all 917 descriptions as generated and unreviewed; removing only the recorded insertions restored the original readable bytes. This is a completed finite demonstration of a representation defect and its local correction. It does not measure OCR accuracy, validate the descriptions, or establish a benefit of graph storage over a serializer implementing the same rule. This report separates the corpus observations, later export integration, unresolved trace defects, and a small public synthetic illustration of the projection rule.

## Question and source scope

The question is whether a transformation delivers the qualifications attached to the content a reader actually receives. Preserving the source archive is necessary for audit, but it does not make an omitted qualification visible in a derived document. The scientific distinction is developed in [Semantic objects and context](../../../papers/semantic-objects-and-context/PAPER.md) and [Constrained transformations](../../../papers/constrained-transformations/PAPER.md).

The studied corpus covered cooking, marine navigation, and electrical automation. The retained source audit identifies a 1952 edition of *Книга о вкусной и здоровой пище*, G. I. Fain's 1977 *Навигация, лоция и мореходная астрономия*, and V. A. Timofeev's 1964 *Сто схемных задач по автоматике*. Dates and page counts describe the observed editions. They do not establish present applicability of advice or authorize practical use.

| Export family | Page anchors | Imported generated descriptions | Nonempty uncertainty fields |
| --- | ---: | ---: | ---: |
| Cooking | 456 | 374 | 111 |
| Navigation | 289 | 319 | 16 |
| Electrical automation | 154 | 224 | 26 |
| Total | 899 | 917 | 153 |

The [structural corpus report](evidence/structural-corpus-report.json) supports the counts. Pages, descriptions, and uncertainty fields are different units. They are not 1,969 independently verified observations, and a page anchor is not an expert judgment on a page.

The structural builder and its validator shared a lexical table detector. Agreement on its table counts is therefore not independent validation of table recognition. The report also records zero image-byte checks in this structural pass; consistency of declared image hashes is a metadata observation.

## Audit and transformation method

The [corpus audit](evidence/corpus-audit-source.json) examined 39 files, thirteen per export. For 33, the export receipt contained expected sizes and hashes, all of which matched. The remaining README and receipt files were pinned by the observer; no receipt was treated as authenticating its own bytes.

The observer reconstructed the readable output from the source document, editing ledger, and structured illustration records. The target readable text was used for comparison rather than inserted into the generated output. The reconstruction covered 174 recorded edits, seven italic-wrapper mappings in the navigation export, three caption-to-image-alt copies, and the generated descriptions. All three readable files matched the retained targets byte for byte.

The mapping was developed after inspecting the available examples. It is a known-data reconstruction, not a blind qualification of the producer. Every replayed editing operation retained its unreviewed status. Reversibility established what the operation did to the representation; it did not establish that the editorial change was linguistically correct.

The important counterexample appeared in the illustration projection. The readable template emitted description, purpose where present, and recognized image text. It did not emit the separately stored `uncertain` field. All 153 nonempty values were absent from the corresponding readable descriptions. This finding concerns that exact field and projection. It does not assert that every description lacked all cautious wording, or that the JSON source had been destroyed.

## Preserving uncertainty as a testable obligation

For a record \(r\) with an explicit qualification \(u(r)\), the relevant requirement is that the delivered projection contain the qualification, or explicitly declare the permitted loss. Byte identity of a different object does not satisfy that requirement. A projection can be perfectly reproducible and consistently omit the same field.

The corrective derivative therefore introduced a narrow rule. After each generated description, it inserted the declared generated/unreviewed status. When `uncertain` was nonempty, it inserted the exact field value with an explicit label. Every insertion carried an input row, record hash, asset identity, anchor, and output range. The source text and original readable files were preserved.

The transformation profile and expected counts were fixed before generation, after the audit had revealed the defect. The [derivative report](evidence/uncertainty-projection-source.json) records the outcome:

| Obligation | Observed result | Boundary |
| --- | --- | --- |
| Preserve generated/unreviewed status | 917/917 descriptions labeled | The labels do not independently assess the description |
| Preserve each nonempty uncertainty value | 153/153 exact values delivered | These are unreviewed model statements, not calibrated probabilities |
| Preserve the previous readable representation | Removing only declared insertions restores all three original files | The experiment concerns this specified transformation |
| Keep source inputs unchanged | All 39 retained source-file hashes unchanged | Integrity is distinct from source correctness |

No new OCR, subject model call, or human domain review occurred in this transformation. Imported model descriptions were already present in the exports. The zero new-call count must not be read as a claim that the corpus contains no model-produced material.

## Domain-specific consequences

The three domains exposed different dependencies. In a cooking instruction, a qualification can belong to one ingredient branch or a later serving operation. Merging branches or moving an action can alter the procedure even if familiar words survive. In navigation, a table or diagram can depend on a legend, a sign convention, a preceding page, and applicability to a particular instrument. Exact numerical transcription alone does not deliver those conditions. In an electrical diagram, visible connections can support a qualitative description while numerical outputs remain unknown without input values and operating context.

These examples motivated engineering obligations; they are not new cooking, navigation, or circuit-design recommendations. The later [projection study](../executable-projections-and-revision/STUDY.md) evaluates selected tasks involving such dependencies. Neither study treats a historical book's age as an automatic proof of error, or as an adequate reason to authorize contemporary action.

## Trace defects and later integration

The audit also found unresolved addressability. Of 5,538 quality flags, the observed mapping addressed 5,518; sixteen table or formula offsets and four orphan flags remained unresolved. A disappearing flag was not counted as repaired OCR. It could reflect changed text, changed diagnostics, or missing provenance.

A separate raw-to-document analysis reproduced all recorded correction rows in the cooking and automation exports. For navigation, 53 of 58 rows were reproduced, leaving five rows in two blocks without a unique raw-serialization binding. Those rows were not labeled five OCR errors. The evidence was insufficient to reconstruct the producer's transformation, which is a different finding.

The twenty unresolved quality flags plus these five correction rows are the 25 unresolved coordinate traces named in the later integration summary. This reconciles its inventory; it does not turn two different kinds of trace defect into a single OCR error rate.

Later local integration processed the same 917 description records in two runs. Each recorded 19,305 satisfied field checks and no violated field checks, preserving 153 nonempty and 764 empty uncertainty values. The [integration summary](evidence/local-export-integration-report.json) also preserves the initial control result of fifteen expected outcomes out of sixteen. One authored control supplied pretty JSON where JSONL was required, causing an earlier-than-intended rejection. Its separately retained correction exercised the intended missing-uncertainty case. A post-replacement control distinguished visibility of a validated new snapshot from unconfirmed durability.

This integration occurred after export. It was not installed in the upstream OCR producer. Physical power-loss durability was not tested. Seven truncated descriptions formed a targeted review queue; the other nonempty uncertainty fields were not automatically equated with defective or truncated outputs.

## Public illustration and retained evidence

The source books, OCR transcriptions, extracted illustrations, and full generated book descriptions are not redistributed here. Project-authored reports and aggregate metadata are provided under readable filenames, with exact JSON identities and separate rendered-prose provenance in [origin.json](evidence/origin.json). Full replay of the original corpus audit requires the specified source packages and original runner closure; the reports alone do not supply them.

A [corrected public illustration](checks/demonstrate_uncertainty_projection.py) uses the four invented records from the preserved edition-1.0 program, two with nonempty uncertainty. It compares the base serializer against a [separately stored literal target](checks/synthetic-base.txt), rather than comparing an expression with itself. A changed-description mutation fails that comparison. The projection preserves both fields, marks all four records, records insertion ranges and rejects an absent uncertainty field; removing exactly those insertions restores the stored target, while damaging an insertion range breaks restoration. These are finite checks of the invented projection rule, not a reconstruction of the historical source-plus-editing-ledger pipeline. Run:

```bash
python3 checks/demonstrate_uncertainty_projection.py
```

The [saved corrected demonstration](checks/uncertainty-projection-check.json) is a new synthetic illustration. The [earlier program](evidence/replay_uncertainty_projection.py) and [earlier result](evidence/public-projection-demonstration.json) are retained unchanged; their `base_reconstruction_exact` predicate compared the same construction with itself and supplied no independent reconstruction evidence. The corrected harness removes that inference. Its four records are not substituted for the 917 historical descriptions, and its checks are not added to historical corpus totals. The [correction record](../review-corrections.json) binds the new fixture, code and result separately.

The corpus audit and derivative report are Russian prose views. The methods, missing-field finding, coordinate counts and qualification limits above are English summaries of their relevant passages; the raw sources have not been translated or rewritten in place. The [evidence language index](../evidence-language-index.json) records the language of every file.

## Limits and conclusion

The corpus's character error rate (CER) and word error rate (WER) remained unmeasured. With a declared alignment and reference unitization, each counts substitutions, deletions and insertions divided by reference characters or words; the historical audit supplied neither a complete ground-truth transcript nor that measurement protocol. `null` therefore does not mean zero error. The [evaluation-method note](../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods) identifies the scoring background.

Image checks belong to different stages and denominators. The earlier reader source reports three selected PNGs checked out of 918 described images. The later 917-description corpus/structural audit checked no image bytes. A separate addressability experiment checked three selected JPEGs, as its [retained source](../executable-projections-and-revision/evidence/addressability-study-source.json) states. None is a byte audit of the whole image collection, and the earlier three-of-918 observation cannot be reassigned to the later 917-record pass. Neither every OCR passage nor the calibration of model uncertainty was assessed. Structural graph construction created addressable source structure; it did not thereby extract a verified semantic knowledge graph.

The established engineering result is precise: the chosen readable template lost an explicitly represented qualification field; a declared and reversible projection preserved it on the inspected finite corpus. A simple serializer can implement that rule. The evidence supports an explicit preservation obligation and supplies a concrete counterexample to equating hashes with meaning preservation. It does not establish superiority of the larger architecture. Related terms are defined in the [glossary](../../../reference/glossary/GLOSSARY.md).
