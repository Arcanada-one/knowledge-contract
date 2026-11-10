---
title: "知识契约：意义、知识与使用条件"
language: "zh-Hans"
license: "CC-BY-4.0"
author: "Pavel Valentov"
sources: none
status: "作者批准的研究计划与阅读地图；不是计划论文已完成的声明"
updated: 2026-11-09
---

# 知识契约：意义、知识与使用条件

[English](../PROGRAMME.md) · [Русский](programme.ru.md) · [现有文档](../DOCUMENTS.md) · [路线图](../ROADMAP.md)

Knowledge Contract 是一项开放的科学与工程研究计划，研究意义的表示以及在明确条件下使用知识。它连接问题、来源解释、形式表示、有依据的操作、实现和实际观察。来源说了什么、已经确立了什么、在当前语境中适用什么，以及代理获准做什么，是不同判断。

## 当前材料与目标结构

PR89提出的1.1版候选目录包含 **31项材料**：十篇科学稿件（包括研究草稿《意义桥接》和新撰写的《意义几何》）、十一份规范、六项研究及四份参考或附录文档。此前获接纳的目录仍为30项，直至另行完成整合决定。作者批准的目标结构为 **34项**：十篇科学工作、十三份规范、七项研究和四份参考文档。尚有三项工程工作处于规划阶段，并非已发布成果；另外两项基础工作沿用既有稿件继续发展。

本阅读地图公开研究结构，不修改科学命题、历史结果、出版目录、索引准入或执行任务状态。标题变化不能代替实质研究。下列链接指向现有来源，其标题可能仍为旧名称。中文指南未声称获得母语编辑认证或独立科学审查。

## 三项共同基础

**意义理论：表示、解释与使用条件。** 从[《意义桥接》](../papers/human-meaning-and-computable-knowledge/PAPER.md)发展共同框架，区分表达、解释、语义对象、语境、证据、知识和使用。[《意义与语境》](../papers/semantic-objects-and-context/PAPER.md)继续详细研究语境及适用性，而不是重复总论。目前是既有研究草稿的实质扩展，不是已经完成的人类理解普遍理论。

**意义代数：类型化操作、复合与区别的保留。** 在[《知识变换》](../papers/constrained-transformations/PAPER.md)的原规范路径上扩展载体、部分定义域、操作语义、复合、投影、残余、重建和迁移。定律属于明确配置，不能默默推广到任意自然语言操作。更名不代表扩展已完成。

**意义几何：表示空间、可区分性与相似性的局限。** [完整研究草稿](../papers/geometry-of-semantic-representations/PAPER.md)研究空间、表示映射、距离、语境相关比较与信息损失。Agent-Brain对该精确版本的有限数学结论给出了有范围的独立审查，但这不是外部同行评审、来源接纳或实测基准。几何接近不能自动确立逻辑蕴涵、适用性或权限。

理论提供对象和问题，代数研究有依据的操作，几何研究区别和比较。三个方向相互联系，但任何一个都不自动证明另一个，也不声称第一版涵盖全部人类意义。

## 科学工作：十项

| 目标名称 | 现有来源或计划 |
| --- | --- |
| **意义理论：表示、解释与使用条件** | 扩展[意义桥接](../papers/human-meaning-and-computable-knowledge/PAPER.md) |
| **意义代数：类型化操作、复合与区别的保留** | 扩展[知识变换](../papers/constrained-transformations/PAPER.md) |
| **意义几何：表示空间、可区分性与相似性的局限** | [完整研究草稿，尚未接纳](../papers/geometry-of-semantic-representations/PAPER.md) |
| **意义与语境：语义对象与适用条件** | [现有稿件](../papers/semantic-objects-and-context/PAPER.md) |
| **语境组装：检索、要求覆盖与资源限制** | [现有稿件](../papers/retrieval-and-context-composition/PAPER.md) |
| **交互与记忆：对话、文档与修订边界** | [现有稿件](../papers/interaction-and-memory/PAPER.md) |
| **证据与证伪：断言依据与检查边界** | [现有稿件](../papers/evidence-and-falsification/PAPER.md) |
| **知识修订：版本、评估与变更采纳** | [现有稿件](../papers/revision-and-governance/PAPER.md) |
| **知识复用：已准备知识的应用条件** | [现有稿件](../papers/controlled-knowledge-reuse/PAPER.md) |
| **知识效用：结果、成本与生命周期决策** | [现有稿件](../papers/knowledge-utility/PAPER.md) |

## 工程规范：十三项

规范陈述义务，其存在不证明已部署实现符合义务。

| 目标名称 | 来源或计划 |
| --- | --- |
| **契约核心：知识模型与准入要求** | [现有规范](../engineering/specifications/knowledge-contract-core/SPECIFICATION.md) |
| **语义类型：表示、归属与作用范围** | [现有规范](../engineering/specifications/semantic-types/SPECIFICATION.md) |
| **意义形式化：从来源解释到可计算表示** | 计划中的语义桥接规范；复用语义类型，保留歧义、否定、单位、归属及损失 |
| **知识操作：前置条件、结果与变换义务** | [现有规范](../engineering/specifications/contract-family/SPECIFICATION.md) |
| **语境包：要求覆盖、依赖与交付** | [现有规范](../engineering/specifications/context-package/SPECIFICATION.md) |
| **派生知识：可复现派生与结果保留** | [现有规范](../engineering/specifications/compiled-artifact-contract/SPECIFICATION.md) |
| **制品登记：身份、可读名称与格式** | [现有规范](../engineering/specifications/artifact-registry/SPECIFICATION.md) |
| **状态模型：评估、执行与发布** | [现有规范](../engineering/specifications/status-model/SPECIFICATION.md) |
| **断言验证：证明、测试与反例协议** | 计划中的语义验证规范，落实证据与证伪的方法 |
| **缓存有效性：结果身份与依赖变化** | [现有规范](../engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) |
| **复用政策：时间、权限与决策** | [现有规范](../engineering/specifications/reuse-policy/SPECIFICATION.md) |
| **知识演化：修订规则与一致更新** | [现有规范](../engineering/specifications/knowledge-evolution/SPECIFICATION.md) |
| **图书包：来源、语义层与验证** | [现有规范](../engineering/specifications/book-package/SPECIFICATION.md) |

两份新规范已包含在基础计划中。可读名称不会创建新的执行任务。在确定实际接口之前，不另行添加几何引擎规范。

## 研究与检查：七项

| 目标名称 | 来源或计划 |
| --- | --- |
| **契约检验：配置符合性与信任边界** | [现有研究](../engineering/studies/contract-profile-conformance/STUDY.md) |
| **依赖闭包：强制关系与包交付检查** | [现有研究](../engineering/studies/dependency-closure-and-package-delivery/STUDY.md) |
| **不确定性保留：来源变换中的限定丢失** | [现有研究](../engineering/studies/source-transcription-and-uncertainty/STUDY.md) |
| **可执行投影：部分提取与定址修订** | [现有研究](../engineering/studies/executable-projections-and-revision/STUDY.md) |
| **复用经济性：准入条件与保留结果的成本** | [现有研究](../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) |
| **编辑试验：单个科学章节的编辑比较** | [现有研究](../engineering/studies/editorial-skill-pilot/STUDY.md) |
| **意义操作：示例、反例与可复现检查** | 计划研究选定的理论、代数与几何断言 |

既有研究保留失败案例、比较平局和限制。计划研究从带例外及归属的规则、带单位及投影残余的量，以及语境或权限变化后的复用开始。数学推导、已执行合成检查与真实代理或服务观察分别报告，不把预期结果写成实际观察。

## 共同参考：四项

| 目标名称 | 来源 |
| --- | --- |
| **共同词汇：意义理论与知识工程术语** | [术语表](../reference/glossary/GLOSSARY.md) |
| **研究文献：原始来源与相关工作** | [参考文献](../reference/bibliography/BIBLIOGRAPHY.md)，不是第二份基础理论 |
| **来源历史：溯源与版本兼容性** | [来源映射](../appendices/source-map/APPENDIX.md) |
| **发布接口：文档访问与表示一致性** | [接口附录](../appendices/api-integration/APPENDIX.md) |

## 关系地图

| 科学说明 | 工程表达 | 有界检查 |
| --- | --- | --- |
| 意义理论；意义与语境 | 语义类型；意义形式化 | 不确定性保留；计划中的意义操作 |
| 意义代数 | 知识操作；派生知识 | 可执行投影；计划中的意义操作 |
| 意义几何；语境组装 | 语境包；未来明确的检索配置 | 计划几何案例；既有交付检查不认证几何 |
| 证据与证伪 | 断言验证；状态模型 | 每项研究的实际范围 |
| 交互与记忆；知识修订 | 制品登记；知识演化 | 定址修订与语境变化案例 |
| 知识复用；知识效用 | 缓存有效性；复用政策 | 复用经济性 |

关系应明确标为“使用定义”“在前提下证明”“落实为工程要求”“测试”“限制”或“替代先前版本”。阅读链接不等于证明依赖。实现失败、经验假设未获支持以及定理被反驳需要不同修复。

现有路线图与任务权威保持不变；本地图不是第二套任务跟踪器，也不宣布任务完成。读者界面使用“知识检查”和“执行检查”等名称，稳定案例编号仅保留在技术记录中。

## 发布与参与

已接受的有限阅读批次无需等待全部计划研究或实验。新稿件只有在完整文本存在且状态准确时才进入目录。保留旧路径、引用、锚点与审查历史；实质修改需要新版本和针对性审查，更名不能把旧接受结论转移到新字节。译文按明确来源变化更新，而不是重做所有未变译文。

项目作者为Pavel Valentov。本计划及其本地化指南由作者在KC-Brain协助下编写，不是独立科学审查。文本采用CC BY 4.0。请按[贡献流程](../CONTRIBUTING.md)提交更正、反例、可复现检查与实现，说明精确工作、版本、依据和限制。多个代理重复同一断言并不产生独立证据。

发布本地图确立的是公开的研究结构，不是四项计划工作完成、新定理成立、网站部署、服务索引更新或代理行动权限。
