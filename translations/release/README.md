---
title: "Reviewed Translations: A Finite First Reading Release"
sources: ["Knowledge Contract project corpus and publication edition"]
status: prepared release inputs; not a served-publication receipt
updated: 2026-11-09
---

# Reviewed Translations: A Finite First Reading Release

This is the bounded release extraction from [the full translation proposal](https://github.com/Arcanada-one/knowledge-contract/pull/76), not another translation-authoring programme. It reuses twenty unchanged reviewed target blobs for ten works. Other authored translations and future papers remain in that existing proposal; no authored body is deleted or replaced there.

## Included works

| Work | Russian body | Simplified Chinese body |
| --- | --- | --- |
| Meaning in Context | [Смысл и контекст](../ru/papers/semantic-objects-and-context/PAPER.md) | [意义与语境](../zh-Hans/papers/semantic-objects-and-context/PAPER.md) |
| Contract Checks | [Проверки контрактов](../ru/engineering/studies/contract-profile-conformance/STUDY.md) | [契约检验](../zh-Hans/engineering/studies/contract-profile-conformance/STUDY.md) |
| Source History | [История источников](../ru/appendices/source-map/APPENDIX.md) | [来源历史](../zh-Hans/appendices/source-map/APPENDIX.md) |
| Publication Interfaces | [Интерфейсы публикации](../ru/appendices/api-integration/APPENDIX.md) | [发布接口](../zh-Hans/appendices/api-integration/APPENDIX.md) |
| Research Foundations | [Исследовательские основания](../ru/reference/bibliography/BIBLIOGRAPHY.md) | [研究基础](../zh-Hans/reference/bibliography/BIBLIOGRAPHY.md) |
| Editorial Pilot | [Редакторский пилот](../ru/engineering/studies/editorial-skill-pilot/STUDY.md) | [编辑试验](../zh-Hans/engineering/studies/editorial-skill-pilot/STUDY.md) |
| Dependency Closure | [Замыкание зависимостей](../ru/engineering/studies/dependency-closure-and-package-delivery/STUDY.md) | [依赖闭包](../zh-Hans/engineering/studies/dependency-closure-and-package-delivery/STUDY.md) |
| Uncertainty Preservation | [Сохранение неопределённости](../ru/engineering/studies/source-transcription-and-uncertainty/STUDY.md) | [不确定性保留](../zh-Hans/engineering/studies/source-transcription-and-uncertainty/STUDY.md) |
| Executable Projections | [Исполняемые проекции](../ru/engineering/studies/executable-projections-and-revision/STUDY.md) | [可执行投影](../zh-Hans/engineering/studies/executable-projections-and-revision/STUDY.md) |
| Reuse Economics | [Экономика повторного использования](../ru/engineering/studies/reuse-admission-and-cost-controls/STUDY.md) | [复用经济性](../zh-Hans/engineering/studies/reuse-admission-and-cost-controls/STUDY.md) |

The [recorded reviews](RECORDED-REVIEWS.md) identify five actual full-body review records, their dates, roles, exact subjects and limits. The [closed batch input](first-reviewed-batch.json) supplies the exact twenty target identities. It is not a sidecar admission and is not to be renamed `publication-renditions.json`.

## Reconcile the changed source names without rewriting the papers

The source and target pins originally reviewed are explicit. Current source names changed since that snapshot. The producer tool checks the entire source body after removing only its declared title mapping and exact compatibility-anchor addition. A changed scientific byte or unsupported metadata structure is a refusal, not automatic currency. It prepares current target titles and source pins while preserving the complete translated body, old anchor, formulas, tables, links and machine identifiers byte for byte. Original source and target identities remain in the proposal metadata.

```sh
python3 -B -m unittest tools.test_prepare_reviewed_publication -v
python3 -B tools/prepare_reviewed_publication.py \
  --repository . \
  --source-commit 2b5bcff544fea5d1752ff009933e4ce0305dad8b \
  --output /tmp/kc-reader-rendition-proposals
```

The output directory must be new and outside the checkout. The script has no network, Git mutation or credentials. It returns the exact proposed files, a reviewable patch and hashes; it does not apply them, create a release decision, change an index, or deploy anything. Eighteen synthetic tests passed in KC-Brain's local container before submission; the actual twenty-source Git comparison is a separate hosted/native run, not predeclared successful here. The workflow runs with read-only permissions and does not push its outputs.

The source alignment is a producer identity check, not a new independent fidelity verdict. Agent-Brain should review the actual bounded header/source/link/section delta, retaining the already completed full-body findings for unchanged content. Do not ask for another generic whole-corpus approval. Any additional body change goes back to KC-Brain, not to an engineer for authorship.

## Mechanical integration inputs and completion criteria

The existing publication owner receives this prepared finite batch, not a new task or worker. After actual checks, apply the generated content patch in this release line, record its exact commit and old/new target hashes, and complete the narrow delta review. Assemble the closed sidecar schema used by the existing site compiler from the final source/target identities and genuine in-repository review evidence. Do not put an older verdict on changed exact bytes. Source/target ancestry, hashes, real section maps and Link/Image parity must pass the actual compiler, not fixture mode.

If an original translated link needs a technical relative-path change to resolve to the same canonical work and anchor, show that exact link-only mapping. Preserve immutably cited historical evidence URLs. If link meaning or scientific prose changes, return it for content review. Do not weaken the compiler or fabricate locale pages to satisfy a check.

The deployment input is the ordinarily merged exact publication commit and sidecar, with no blanket admission of the other PR76 drafts or unmerged English PR83. The site owner updates reader cards, navigation, source-download labels, search aliases and roadmap entry links from the accepted names; regenerates committed output; runs existing build/link/mobile checks; uses the established production deployment and rollback process; and reads back the actual served identities and full locale bodies. English fallback must never be counted as a published translation. Backend index promotion is a distinct operation requiring its own existing decision and readback.

The ready English reading release and the newly merged Clear Names/reading guides are not blocked by these remaining rendition mechanics. Future scientific work and native-execution experiments are not prerequisites for this finite public-reading release.
