---
title: "开始阅读：面向人类与代理的知识契约"
sources: ["Knowledge Contract project corpus and publication edition"]
language: zh-Hans
status: localized reader guide; no native-speaker certification
updated: 2026-11-14
---

# 开始阅读：面向人类与代理的知识契约

[English](../READING.md) · [Русский](READING.ru.md) · [全部文档名称](../DOCUMENTS.md) · [路线图](../ROADMAP.md)

**知识契约把知识与其解释、检验和使用条件联系起来。** 有来源的引文并不自动为真；相关段落未必构成充分语境；检查通过也不等于获得执行行动的权限。本项目为人类读者与人工智能代理明确这些区别。

## 选择阅读路径

初次了解项目，可先读明确标为研究草稿的[《意义桥接》](../papers/human-meaning-and-computable-knowledge/PAPER.md)，再读[《意义与语境》](../papers/semantic-objects-and-context/PAPER.md)。[《意义几何》](../papers/geometry-of-semantic-representations/PAPER.md)是有限数学比较的英文研究草稿，不是已发布的中文全文。[《知识变换》](../papers/constrained-transformations/PAPER.md)讨论信息保留，[《语境组装》](../papers/retrieval-and-context-composition/PAPER.md)讨论所选内容与实际交付内容的充分性。

要检查论证，可阅读[《证据与证伪》](../papers/evidence-and-falsification/PAPER.md)和[《知识修订》](../papers/revision-and-governance/PAPER.md)。要开展实现，可从[《契约核心》](../engineering/specifications/knowledge-contract-core/SPECIFICATION.md)、[《知识操作》](../engineering/specifications/contract-family/SPECIFICATION.md)和[《状态模型》](../engineering/specifications/status-model/SPECIFICATION.md)开始。

实际观察记录见[工程研究](../engineering/studies/README.md)，断言与证据的对应关系见[证据索引](../engineering/studies/evidence-index.json)。机器访问说明见[《发布接口》](../appendices/api-integration/APPENDIX.md)。接口说明本身不是执行能力已经实现的证明。

## 阅读与获取来源

[项目网站](https://contract.place/)提供阅读界面。仓库保存原文、证据和版本历史。[历史版本的31项文档目录](https://github.com/Arcanada-one/knowledge-contract/blob/6a6f202f7f70be2ad3aea3369e45409761708596/DOCUMENTS.md)对应不可变来源快照`6a6f202f7f70be2ad3aea3369e45409761708596`：十篇科学论文、十一份规范、六项研究、术语表、参考文献以及两个附录。上述文档链接指向规范英文来源；中文链接文字本身不表示正文已经翻译。

[当前集成候选版本的文档目录](../DOCUMENTS.md)包含33项，其中新增了 Agent Situation 研究草稿和 Context Controls 有限研究。目录收录不等于独立科学审查通过、全文翻译完成、生产部署或 KC2 准入。

通过文档链接可以阅读完整Markdown，并使用GitHub的Raw功能获取相应原文。引用或归档时应选择具体commit，而不是不断变化的分支。未声明的PDF或尚未发布的译文，不应被宣传为已经可供下载。

网站界面语言与正文语言是两回事。译文缺失或过期时，页面应明确说明显示的是英文来源。[翻译清单](../roadmap/TRANSLATIONS.md)列出精确来源快照中存在与缺失的正文文件，并将文件统计与审查记录分开。[简体中文来源文本](https://github.com/Arcanada-one/knowledge-contract/tree/6a6f202f7f70be2ad3aea3369e45409761708596/translations/zh-Hans)可以在该修订版直接阅读。此前的[翻译提案](https://github.com/Arcanada-one/knowledge-contract/pull/76)仍保留为历史记录。仓库中存在文件，并不证明网站已提供该译文。本中文读者指南也不声称获得母语编辑认证。

## 理解不同的检查

论文可以给出条件证明，规范规定义务，研究报告实际观察，部署记录说明读者真正取得的版本。失败案例、与简单基线的平局以及未知量，都是出版内容的一部分，不能被笼统的“完成”掩盖。

[《知识检验》](../reference/document-naming/CHECKS.md#knowledge-checks-mandatory-requirements-and-evidence-assessment)是强制要求与证据评估包的可读名称。场景代码只用于精确追踪，不代替名称。[《执行检验》](../reference/document-naming/CHECKS.md#execution-checks-authorization-budget-and-result-integrity)则单独检查授权、预算和实际行动。

## 参与改进

人类和代理均可依照[贡献规则](../CONTRIBUTING.md)提交具体意见、反例、复现结果、说明改进或翻译。请标明文档、精确版本、章节、待检验主张及其证据。反驳条件命题需要满足全部前提；超出前提的示例检验的是适用边界。

同意的代理数量不能替代证据。作者检查、另一角色的内部代理审查、外部同行评审以及母语编辑审查是不同观察。敏感发现应通过[安全报告途径](../SECURITY.md)提交。

发布是持续研究中的一个有限、可检查状态。[路线图](../ROADMAP.md)说明后续发展，而不是要求未来研究全部完成之后才允许读者使用已经接受的版本。
