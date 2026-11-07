---
name: "knowledge-evolution"
title: "知识演化与版本化规则"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "版本化创建规则、采纳、影响分析、重新评估、迁移和协调发布。"
translation_of: "engineering/specifications/knowledge-evolution/SPECIFICATION.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "3e87cf3c9d1e891e435e21f646a838e625c45511"
translation_status: "author-draft"
---

# 知识演化与版本化规则 {#knowledge-evolution-and-versioned-rules}

**作者：**Pavel Valentov · **出版版本：**1.1

## 1. 目的与符合性 {#1-purpose-and-conformance}

本文是一组架构要求。互操作性需要具名的表示配置；已实现的交换子集仅限于[观察、变更事件和配置通告](../status-model/SPECIFICATION.md#8-bounded-exchange-profile)，而[书籍包配置](../book-package/SPECIFICATION.md)具有自己的模式。这并不意味着已有完整契约的传输格式或已部署的运行时。

**EVO-R001.** 每个新的知识或决策制品必须（MUST）记录对其创建产生实质约束的精确契约、配置和规则。

按后来的规则重新评估，是一次新观察。原始派生过程和修订版仍可追溯。

大写要求用语遵循 [BCP 14](../../../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。本规范不仅治理软件版本，也治理解释和准入规则的变化。命名一个研究方向本身，不会确立已有实现的模式或可执行验证器。[修订论文](../../../papers/revision-and-governance/PAPER.md)提供底层模型。

## 2. 创建依据 {#2-creation-basis}

**EVO-R002.** 创建依据记录必须（MUST）标识制品修订版、实质相关的来源修订版、契约和配置定义、相关规则集版本、变换配方、责任主体、创建时间或区间，以及已知缺口。

**EVO-R003.** 引用必须（MUST）解析为不可变修订版，或记录无法解析的事实。

只有实际使用过的规则才列为创建输入。

**EVO-R004.** 后来采纳的规则不得（MUST NOT）被插入旧依据，伪装成它支配了原始工作。

当精确修订版具有实质意义时，“最新契约”等宽泛标签并不足够。

**EVO-R005.** 实现必须（MUST）区分内容变化、表示变化、评估变化和治理变化。

评估更新可以改变某项用途是否准入，而不修改来源字节。解释纠正会产生新的语义修订版，即使原始来源没有改变。

## 3. 变更提案与采纳 {#3-change-proposal-and-adoption}

**EVO-R006.** 每项提案必须（MUST）标识旧规则和建议规则的修订版、动机、受影响范围、预期兼容性、迁移影响、证据、反对意见，以及已知的未决问题。

采纳需要治理政策规定的决策者和权限。贡献者、编辑者或自动验证器不会仅因提出建议就获得该权限。

**EVO-R007.** 相互冲突的采纳决定必须（MUST）阻止受影响用途，直到具有经认证权限的决策者解决冲突，或明确采纳允许的更窄范围。

未解决的冲突具有 `unknown_impact`、未知使用资格和 `unresolved` 操作结果；独立的已知禁止则产生 `blocked` 和拒绝。预期测试结果是：冲突未解决时，不发布，也不进行获准交付。

采纳决定证明某项规范在其范围内被接受，但不证明促成该规范的每项事实性断言都为真。

**EVO-R008.** 决定必须（MUST）保留指向已评估提案的链接，以及任何限制或生效日期。

## 4. 影响分析与重新评估 {#4-impact-analysis-and-reassessment}

影响分析从声明的依赖关系开始。

**EVO-R009.** 必须（MUST）依据相关的新规则集和用途范围，对受影响制品分类。

影响词元为 `compatible`、`restricted`、`requires_review`、`blocked` 和 `unknown_impact`；资格与决定之间的映射见[状态模型](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies)。这些是单个观察的投影，而不是永久的全局真值标签。

**EVO-R010.** 兼容性结果必须（MUST）说明保留论证或测试。

依赖覆盖未知时，不能支持“找到了每个受影响制品”的声明。如果未跟踪依赖可能改变强制义务，就必须保守地重新评估。

重新评估记录旧制品、新规则集、相关当前状态、方法、结果和限制。通过更窄测试的重新评估，不能确立与更宽配置兼容。范围不同的多个评估可以共存。

## 5. 迁移 {#5-migration}

迁移创建新的表示或修订版，包含明确来源链接、映射、验证结果、损失和未决字段。

**EVO-R011.** 迁移必须（MUST）保留否定、条件、归属和适用约束，或者声明其损失。

**EVO-R012.** 缺失的能力或权限必须（MUST）保持未知。

迁移不能虚构执行尝试或成功结果。

**EVO-R013.** 如果语义等价尚未确立，即使新结构有效，迁移也必须（MUST）说明这一限制。

可逆字节变换仅确立所声明的表示性质。无损语义迁移需要在规定定义域内论证解释得以保留。

## 6. 可见性与回滚 {#6-visibility-and-rollback}

**EVO-R014.** 发布必须（MUST）选择协调一致的制品修订版、目录条目和渲染表示集合。

**EVO-R015.** 指针更新必须（MUST）具有已识别的采纳决定和完整原子的[发布守卫](../cache-identity-and-invalidation/SPECIFICATION.md#5-guarded-publication-and-serving)，包括当前权限和依赖代次。

**EVO-R016.** 网站、可下载语料和 API 索引必须（MUST）公开其实际来源修订版，使消费者能够检测差异。

回滚改变选定的当前修订版，不会抹去后来的修订版或其观察。

**EVO-R017.** 如果规则因已知缺陷或披露限制而被撤回，回滚必须（MUST）保留这一知识，并且不得（MUST NOT）默默重新授权此前阻止的用途。

## 7. 验收用例 {#7-acceptance-cases}

必需用例包括：内容未变但规则修订；通过间接依赖发现受影响制品；依赖不完整导致影响未决；丢失约束的无效迁移；冲突的采纳决定；延迟发布者；以及撤销之后的回滚。

**EVO-R018.** 每个用例必须（MUST）保留历史创建依据，以及独立的当前决定。

[投影与修订研究](../../../../../engineering/studies/executable-projections-and-revision/STUDY.md)提供有关可寻址变化和有限投影的有界证据。[符合性研究](../../../../../engineering/studies/contract-profile-conformance/STUDY.md)记录有限的迁移检查。其结果不确立任意知识图的自动迁移，也不确立已部署社区治理服务。

## 8. 出版与实现版本 {#8-publication-and-implementation-versions}

**EVO-R019.** 文档出版版本、序列化配置、验证器实现、证据协议、服务构建和索引快照必须（MUST）分别标识版本。

从手稿删除开发标签，不会改变已部署协议。反过来，服务功能未完成，也不妨碍发布具有明确假设的完整形式论证。

[来源映射和兼容性记录](../../../../../appendices/source-map/APPENDIX.md)标识本出版版本替代了什么，以及哪些历史传输版本保持不变。[API 集成附录](../../../../../appendices/api-integration/APPENDIX.md)定义可观察的发布边界，而不声称已有未经验证的契约组合端点。
