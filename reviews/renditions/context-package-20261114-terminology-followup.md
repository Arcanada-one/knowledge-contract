---
title: "Context Terminology: Russian and Chinese Draft Corrections"
sources: none
status: author-edit-record
language: en
license: CC-BY-4.0
---

# Context Terminology: Russian and Chinese Draft Corrections

This is an author response to the eight terminology findings in the [non-author reading of 13 November](https://github.com/Arcanada-one/knowledge-contract/pull/104#issuecomment-6857238752). It records a local candidate based on PR104 head `9978b215b9d026067b8b5ecbd9e0c10e250faf55`. It is not a new review, fidelity approval, native-speaker endorsement, publication decision or deployment record. Both renditions remain `author-draft`.

## Exact inputs and outputs

The English source is `engineering/specifications/context-package/SPECIFICATION.md` at commit `161a01afb1b756adf059ea2e1cbdd0dca29d83a2`, Git blob `30ca8d2e5b5dd0e38b30cdb46919f514771a01da`. It is unchanged.

| Rendition | Previous Git blob | Corrected Git blob | Corrected SHA-256 |
| --- | --- | --- | --- |
| Russian | `7db4c99c2e61f082f00223d19faa7de159465d51` | `7ca11d3f43091d6c312e05f400933e118a673c8e` | `f202f811e2a1567c8a9bbaf83621cefe10b448b8ed7d839bf5fc3dd88f0bf628` |
| Simplified Chinese | `4472d72bbfe9481bf7972da9a693391e61aa638a` | `7e2bdb1c5a65f963fbe7e276ee6fe8a68594bc92` | `11d1c28bdf78ebcb132f82dcb550d7cacf2f162f92335eb786704b35b0fd4319` |

## Disposition of the eight findings

| Finding | Previous wording | Corrected wording and scope |
| --- | --- | --- |
| RU-1: delivery | `контекст выдачи`; `Выдача и квитанция` | `контекст доставки`; `Доставка и квитанция`. These two occurrences now use the same term as the title and other delivery clauses. |
| RU-2: assurance | `объявленную область и полноту процедуры поиска`; `Покрытие и полнота процедуры поиска`; `Полнота процедуры поиска — отдельное измерение` | `объявленную область поиска и гарантии поиска`; `Покрытие и гарантии поиска`; `Гарантии поиска — отдельное измерение`. The dimension is distinguished from the completeness obligation. Its three literal values are unchanged. |
| RU-3: recipient | `что фактически получает адресат` | `что фактически получает получатель`, consistent with the remaining document. |
| RU-4: output allowance | `резерв для ответа` | `резерв для результата`, covering the answer, plan and execution stages already named by the source. |
| ZH-1: package name | Two body occurrences of `上下文包` alongside the title `语境包` | Both body occurrences become `语境包`, preserving the existing registered title and H1. Other occurrences of the generic word for context are unchanged. |
| ZH-2: subject and object | Both rendered as `对象` | The four source occurrences of subject become `所指对象`: the first, in R002, includes the disambiguator `（subject）`; R003, R009 and section 8 use the same Chinese term. The source occurrences of object remain `对象`. This avoids introducing an acting-agent meaning for subject. |
| ZH-3: illustrative examples | `早期示例` | `早期说明性示例`, preserving the distinction between illustrative examples and executed packages. |
| ZH-4: admitted conclusion | `一个可准入结论` | `一个已获准入的结论`, retaining the source's completed admission rather than mere admissibility. |

## Bounded verification

The complete English source, both previous renditions and the cited review were read before these edits. The existing [source-pin suite](../../tools/test_context_package_translation_pin.py) passed all nine tests locally:

```sh
python3 -B -m unittest tools.test_context_package_translation_pin -v
```

Additional comparisons against the exact previous target bytes established, for each language: all 20 requirement identifiers once and in order; 16 MUST, three MUST NOT (R008, R010, R016) and one MAY (R005); byte-identical front matter, source pins and author-draft status; all ten explicit anchors unchanged; all eight document destinations and fragments unchanged; unchanged coverage and assurance tokens; and preserved study quantities 4,096, 24,576, 12 and 110. The English source bytes are identical. Only the replacements listed above were applied to the two rendition bodies. The existing test module, earlier review records and publication-renditions sidecar are unchanged.

These are structural and edit-integrity observations, not a complete semantic verdict or the full repository CI. No rendered-page, PDF or production acceptance is claimed. The changed words require renewed non-author reading at the exact new blobs. The earlier review's disclosure of shared controller/model family and unverified independence/language competence remains in force; this author record does not upgrade it. Related glossary and Status Model draft terminology is outside this bounded correction and has not been silently reclassified as accepted.

The ordinary source CI, exact-source rendition review and existing admission process remain necessary before publishing these bodies. Prior review findings remain bound to their original source-target pairs.
