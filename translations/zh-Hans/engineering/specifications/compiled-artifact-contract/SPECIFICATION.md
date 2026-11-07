---
name: "compiled-artifact-contract"
title: "编译知识制品与可复现派生"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "保存的派生结果，包含精确输入、配方、依赖清单、模板和输出证据。"
translation_of: "engineering/specifications/compiled-artifact-contract/SPECIFICATION.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "feef304cc65842e6ed9851fa9278ff30602c4a3d"
translation_status: "author-draft"
---

# 编译知识制品与可复现派生 {#compiled-knowledge-artifacts-and-reproducible-derivation}

**作者：**Pavel Valentov · **出版版本：**1.1

## 1. 目的与符合性 {#1-purpose-and-conformance}

本文是一组架构要求。互操作性需要具名的表示配置；已实现的交换子集仅限于[观察、变更事件和配置通告](../status-model/SPECIFICATION.md#8-bounded-exchange-profile)，而[书籍包配置](../book-package/SPECIFICATION.md)具有自己的模式。这并不意味着已有完整契约的传输格式或已部署的运行时。

编译知识制品是由声明的提取、选择、变换或组合产生并保存的派生结果。它将结果连接到输入、配方、依赖、要求、输出表示和证据。它的可用性可以避免重复工作，但仅有可用性并不能证明复用合理。

大写要求用语遵循 [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。

**CKA-R001.** 符合性声明必须（MUST）指明制品类别、表示配置和已经执行的检查。[受控知识复用](../../../papers/controlled-knowledge-reuse/PAPER.md)提供模型；[缓存身份](../cache-identity-and-invalidation/SPECIFICATION.md)和[复用政策](../reuse-policy/SPECIFICATION.md)约束后续应用。

## 2. 结果类别与最少信息 {#2-result-kinds-and-minimum-information}

| 结果类别 | 额外的最低义务 |
| --- | --- |
| 检索结果 | 查询语义、被搜索快照、程序限制和候选项身份 |
| 所选上下文 | 要求覆盖、强制闭包、投影和资源核算 |
| 派生解释或答案 | 被支持的断言、预期受众、损失和必需的不确定性 |
| 依赖闭包 | 根节点、关系政策、精确图快照和未解决的边 |
| 参数化模板 | 允许的替换、定义域限制和实例验证规则 |
| 有界否定结果 | 精确否定断言、有限范围、完整性前提以及使其失效的条件 |

这些类别并未穷尽所有可能的派生结果。

**CKA-R002.** 扩展必须（MUST）声明其额外义务和兼容性规则。

## 3. 制品记录与构建记录 {#3-artifact-and-build-records}

**CKA-R003.** 制品必须（MUST）标识不可变输出字节或经过精确定义的规范化处理的结构化值、其哈希域、表示配置、内容身份、来源和规则集修订版、配方身份以及生成该制品的尝试。

内容摘要在编码假设范围内确立相等性；它不认证作者，也不确立来源内容为真。

**CKA-R004.** 构建配方必须（MUST）包括精确的输入引用、变换定义版本、相关参数，以及能够改变所声称结果的环境依赖。

构建身份记录这一声明。可复现性还需要按明确的等价标准实际成功重跑。配方哈希相同，不能证明配方已经执行，也不能证明非确定性输出相等。

**CKA-R005.** 尝试记录必须（MUST）区分[状态模型](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies)中的 `planned`、`ready`、`running`、`paused` 和 `finished` 执行阶段，以及结果、停止原因、存在时的输出引用和已观察效果。

**CKA-R006.** 失败的尝试不得（MUST NOT）创建虚构的成功制品。

部分输出可以保留为部分结果，并说明其限制。

## 4. 依赖清单 {#4-dependency-manifest}

**CKA-R007.** 清单必须（MUST）包括每项声明依赖的身份、修订版、角色、必需状态、相关有效条件和对变化的敏感性。

依赖可以包括来源、选择器、配置、规则、编译器版本、权限代次、查询和要求。遗漏相关依赖，会使“该清单对该用途是完整的”这一声明失去依据。

**CKA-R008.** 基于不存在或穷尽枚举的结果必须（MUST）绑定全集或索引快照，以及完整性程序。

即使此前读取的所有正向输入都未改变，加入一个新的匹配条目仍可能使否定结果失效。

**CKA-R009.** 清单必须（MUST）区分导航性引用与操作依赖。

**CKA-R010.** 清单应该（SHOULD）解释每项操作依赖为何具有实质相关性，使审查者既能识别缺失依赖，也能识别缺乏理由的过度失效处理。

## 5. 模板与实例 {#5-templates-and-instances}

模板定义允许的替换、受保护结构以及可以生成实例的条件。每个实例获得自己的身份、绑定参数、要求和准入决定。模板的年龄或此前的接受状态不会自动转移到实例。

**CKA-R011.** 没有明确规则，参数替换不得（MUST NOT）删除范围、改变受保护的量词，或将权限从一个接收者转移给另一个接收者。

未经验证的参数产生未决或被拒绝的实例。如果实例化改变的含义超出模板声明的定义域，则结果是一次新的派生，而不是有效实例。

## 6. 证据与发布边界 {#6-evidence-and-publication-boundary}

**CKA-R012.** 证据必须（MUST）绑定精确制品和检查。

结构有效性、重构相等、任务充分性、当前适用性和执行成功仍是不同观察。一个制品可以不可变且字节正确，却不具备新请求的使用资格。

**CKA-R013.** 发布可变的当前指针必须（MUST）遵循[缓存身份第5节](../cache-identity-and-invalidation/SPECIFICATION.md#5-guarded-publication-and-serving)规定的完整原子谓词，在更新当前指针的同一决定中纳入依赖代次和权限代次。

**CKA-R014.** 在旧代次下成功完成的构建不得（MUST NOT）覆盖更新的或已经撤销的当前指针。

**CKA-R015.** 最终准入决定必须（MUST）在实际交付边界上有效，而不仅是在构建开始时有效。

## 7. 验收用例与限制 {#7-acceptance-cases-and-limits}

**CKA-R016.** 符合性测试集必须（MUST）覆盖以下情况：输入已变但查找键未变、配方变化、构建不成功、模板参数超出定义域、过时的发布代次、因语料增长而失效的否定结果，以及指向错误输出的证据。

**CKA-R017.** 预期结果必须（MUST）是明确的新构建、拒绝、未决状态，或在具名政策下有效的受保护复用。

[复用准入研究](../../studies/reuse-admission-and-cost-controls/STUDY.md)区分分析性政策、有限检查和测量结果。[投影研究](../../studies/executable-projections-and-revision/STUDY.md)报告有限变换和修订行为。二者都不能确立已经部署了分布式缓存，也不能确立存在通用语义等价求解器。

## 8. 兼容性与迁移 {#8-compatibility-and-migration}

**CKA-R018.** 迁移必须（MUST）保留旧制品及其哈希域、标识映射及其损失，并创建新的表示记录。

新的文档版本不改变现有二进制或传输协议。[兼容性附录](../../../appendices/source-map/APPENDIX.md#4-protocol-compatibility)列明了早期有限配置；声称具备额外行为的实现，需要相应证据。
